from utils.tokens import Token as _Token, TokenType as _TokenType

from utils.expr import ExprVisitor as _ExprVisitor
from utils.stmt import StmtVisitor as _StmtVisitor

from utils.expr import Expr as _Expr, Assign as _Assign, Variable as _Variable, Binary as _Binary, Call as _Call, Get as _Get, Set as _Set, Function as _Function, This as _This, Super as _Super, Conditional as _Conditional, Logical as _Logical, Grouping as _Grouping, Unary as _Unary, Literal as _Literal
from utils.stmt import Stmt as _Stmt, Var as _Var, Const as _Const, If as _If, While as _While, Import as _Import, Func as _Func, Class as _Class,  Block as _Block, Return as _Return, Del as _Del, Print as _Print, Expression as _Expression

from utils.reporter import  ResolutionError as _ResolutionError

import enum as _enum

# Fake C enum type for function type
@_enum.unique
class FunctionType(_enum.Enum):
    NONE = 0
    FUNCTION = 1
    METHOD = 2
    INIT = 3


@_enum.unique
class VariableState(_enum.Enum):
    DECLARED = 1001
    DEFINED = 1011
    READ = 1111


@_enum.unique
class ClassType(_enum.Enum):
    NONE = 44
    CLASS = 45
    SUB = 46

class Variable:
    def __init__(self, name, state):
        self.name = name
        self.state = state


class Stack(list):
    def __init__(self):
        # For REPL sakes a pre-defined scope should be used for global vars
        self.stack = [{}]
        self.lines = [{}]


    def push(self, item):
        self.stack.append(item)


    def pop(self):
        # return and remove last elm
        if not self.isEmpty():
            last = self.stack[-1]
            del self.stack[-1]
            return last

    def popLine(self):
        if not self.isEmptyLines():
            last = self.lines[-1]
            del self.lines[-1]
            return last


    def peek(self):
        if not self.isEmpty(): return self.stack[-1]

    def peekLine(self):
        if not self.isEmptyLines(): return self.lines[-1]


    def isEmpty(self):
        if len(self.stack) == 0: return True
        return False


    def isEmptyLines(self):
        if len(self.lines) == 0: return True
        return False


    def __str__(self):
        return str(self.stack)


    def __repr__(self):
        return str(self.stack)


class Resolver(_ExprVisitor, _StmtVisitor):
    def __init__(self, interpreter: object, vw_Dict: dict):
        self.currentFunction = FunctionType.NONE
        self.currentClass = ClassType.NONE
        self.interpreter = interpreter
        self.scopes = Stack()
        self.vw_Dict = vw_Dict
        self.errors = []


    def visitImportStmt(Self, stmt: _Import):
        return None


    def visitBlockStmt(self, stmt: _Block):
        self.beginScope()
        self.resolveStmts(stmt.statements)
        self.endScope()

        return None


    def visitVarStmt(self, stmt: _Var):
        self.declare(stmt.name)

        if (stmt.initializer != None):
            self.resolveStmt(stmt.initializer)

        self.define(stmt.name)

        return None


    def visitConstStmt(self, stmt: _Const):
        self.declare(stmt.name)
        self.resolveStmt(stmt.initializer)
        self.define(stmt.name)

        return None


    def visitClassStmt(self, stmt: _Class):
        super_lexeme = self.vw_Dict[_TokenType.SUPER.value]
        this_lexeme = self.vw_Dict[_TokenType.THIS.value]

        self.declare(stmt.name)
        self.define(stmt.name)

        enclosingClass = self.currentClass
        self.currentClass = ClassType.SUB

        # resolve super class if any
        if (stmt.superclass != None): self.resolveExpr(stmt.superclass)

        self.beginScope()

        # fake tokens
        this_tok = _Token(_TokenType.THIS, this_lexeme, None, 0)

        self.scopes.peek()[this_tok.lexeme] = Variable(this_tok, VariableState.DECLARED)

        super_tok = _Token(_TokenType.SUPER, super_lexeme, None, 0)

        self.scopes.peek()[super_tok.lexeme] = Variable(super_tok, VariableState.DECLARED)

        for method in stmt.methods:
            decleration = FunctionType.METHOD

            if (method.name.lexeme.__eq__("init")):
                decleration = FunctionType.INIT

            self.resolveFunc(method, decleration)

        self.endScope()

        self.currentClass = enclosingClass

        return None


    def visitFuncStmt(self, stmt: _Func):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolveFunc(stmt, FunctionType.FUNCTION)

        return None


    def visitExpressionStmt(self, stmt: _Expression):
        self.resolveStmt(stmt.expression)
        return None


    def visitIfStmt(self, stmt: _If):
        self.resolveStmt(stmt.condition)
        self.resolveStmt(stmt.thenBranch)

        if (stmt.elseBranch != None):
            self.resolveStmt(stmt.elseBranch)

        return None


    def visitPrintStmt(self, stmt: _Print):
        self.resolveStmt(stmt.expression)

        return None


    def visitWhileStmt(self, stmt: _While):
        self.resolveStmt(stmt.condition)
        self.resolveStmt(stmt.body)

        return None


    def visitDelStmt(self, stmt: _Del):
        # No checks here yet!
        return None


    def visitReturnStmt(self, stmt: _Return):
        return_lexeme = self.vw_Dict[_TokenType.RETURN.value]
        if self.currentFunction == FunctionType.NONE:
            err = _ResolutionError(return_lexeme, f"Cannot return from top-level code.").report()
            self.errors.append(err)

        if (stmt.value != None):
            if (self.currentFunction == FunctionType.INIT):
                err = _ResolutionError(stmt.keyword, "Cannot return a value from an initializer")
                self.errors.append(err)

            self.resolveStmt(stmt.value)

        return None


    def visitVariableExpr(self, expr: _Variable):
        if (self.scopes.isEmpty()) and (self.scopes.peek()[expr.name.lexeme] == False) and (self.scopes.peek()[expr.name.lexeme].state == VariableState.DECLARED):
            err = _ResolutionError(expr.name, "Cannot read local variable in its own initializer. I.e 'Can't var a = a;'")
            self.errors.append(err)

        # Every call obviously suggests a read
        self.resolveLocal(expr, expr.name, True)

        return None


    def visitAssignExpr(self, expr: _Assign):
        if type(expr.value) != list:
            self.resolveExpr(expr.value)
            # Not read yet
            self.resolveLocal(expr, expr.name, False)

            return None

        else:
            return None


    def visitBinaryExpr(self, expr: _Binary):
        self.resolveExpr(expr.left)
        self.resolveExpr(expr.right)

        return None


    def visitCallExpr(self, expr: _Call):
        #print("visiting call")
        self.resolveExpr(expr.callee)

        for arg in expr.args:
            self.resolveExpr(arg)

        return None


    def visitGetExpr(self, expr: _Get):
        self.resolveExpr(expr.object)
        return None


    def visitSetExpr(self, expr: _Set):
        self.resolveExpr(expr.value)
        self.resolveExpr(expr.value)

        return None


    def visitThisExpr(self, expr: _This):
        this_lexeme = self.vw_Dict[_TokenType.THIS.value]

        if (self.currentClass == ClassType.NONE):
            err = _ResolutionError(expr.keyword, f"Cannot use '{this_lexeme}' outside of class")
            self.errors.append(err)

            return None

        self.resolveLocal(expr, expr.keyword, True)
        return None


    def visitSuperExpr(self, expr: _Super):
        super_lexeme = self.vw_Dict[_TokenType.SUPER.value]

        if self.currentClass == ClassType.NONE:
            err = _ResolutionError(expr.keyword, f"Cannoy use '{super_lexeme}' outside of a class.")
            self.errors.append(err)

        if self.currentClass != ClassType.SUB:
            err = _ResolutionError(expr.keyword, f"Cannot use '{super_lexeme}' in class without a superclass")
            self.errors.append(err)

        self.resolveLocal(expr, expr.keyword, True)
        return None


    def visitFunctionExpr(self, expr: _Function):
        return None


    def visitGroupingExpr(self, expr: _Grouping):
        self.resolveExpr(expr.expression)
        return None


    def visitLiteralExpr(self, expr: _Literal):
        return None

    def visitConditionalExpr(self, expr: _Conditional):
        return None


    def visitLogicalExpr(self, expr: _Logical):
        self.resolveExpr(expr.left)
        self.resolveExpr(expr.right)

        return None


    def visitUnaryExpr(self, expr: _Unary):
        self.resolveExpr(expr.right)

        return None


    def beginScope(self):
        self.scopes.push(dict())
        #print("Scope at begin: ", self.scopes.peek())


    def endScope(self):
        #print("Scope at end: ", self.scopes.peek())
        scope = self.scopes.pop()
        lines = self.scopes.popLine()

        # walk variables in scope and check unused ones to report
        for entry in scope:
            if (scope[entry].state == VariableState.DEFINED) and not self.currentFunction == FunctionType.FUNCTION:
                line = lines[entry]
                err = _ResolutionError(line, f"Local variable '{entry}' is declared but unused.")
                self.errors.append(err)


    # Similar to evaluate
    def resolveStmts(self, stmts: list):
        # Loop 'n' resolve
        for stmt in stmts:
            # I.e when multi-variable/const declerations are made
            if type(stmt) == list:
                for decl in stmt:
                    self.resolveStmt(decl)

            else:
                self.resolveStmt(stmt)

        return None


    # Similar to execute in interpreter
    def resolveStmt(self, stmt: _Stmt):
        #print("state of scopes in res stmt: ", self.scopes)
        stmt.accept(self)


    def resolveExpr(self, expr: _Expr):
        expr.accept(self)


    def resolveLocal(self, expr: _Expr, name: _Token, isRead: bool):
        #print(f"inside resolveLocal with params expr: '{expr}', Name: '{name}', IsRead: '{isRead}'")
        for i in range(len(self.scopes.stack), 0, -1):
            if (name.lexeme in self.scopes.stack[i - 1]):
                self.interpreter.resolve(expr, (len(self.scopes.stack) - 1 - i))

                if (isRead):
                    self.scopes.stack[i - 1][name.lexeme].state = VariableState.READ
                    return

        # Pretend its global if its not found


    def resolveFunc(self, func: _Func, functype: FunctionType):
        #print("in func resolve")
        enclosingFunction = self.currentFunction
        self.currentFunction = functype

        # Declare and define each param to avoid param redefinition in func body
        self.beginScope()

        for param in func.function.params:
            self.declare(param)
            self.define(param)

        self.resolveStmts(func.function.body)
        self.endScope()

        self.currentFunction = enclosingFunction


    def declare(self, name: _Token):
        #print("State of scopes in decl: ", self.scopes)
        if (self.scopes.isEmpty()): return

        scope = self.scopes.peek()

        try:
            if (name.lexeme in scope):
                err = _ResolutionError(name, f"Variable with the name {name.lexeme} already declared in this scope.").report()
                self.errors.append(err)

        except TypeError:
            pass

        # Mark shadow var as not ready yet
        scope[name.lexeme] = Variable(name, VariableState.DECLARED)
        #print("State of scopes in decl end: ", self.scopes)


    def define(self, name: _Token):
        if (self.scopes.isEmpty()): return

        # Mark var as live and kicking.
        self.scopes.peek()[name.lexeme].state = VariableState.DEFINED

        # TODO: Find better solution for noting lines
        try: self.scopes.peekLine()[name.lexeme] = name.line
        except TypeError: pass
