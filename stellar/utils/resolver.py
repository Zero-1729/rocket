from tokens import Token as _Token, TokenType as _TokenType

from expr import ExprVisitor as _ExprVisitor
from stmt import StmtVisitor as _StmtVisitor

from utils.expr import Expr as _Expr, Assign as _Assign, Variable as _Variable, ExprVisitor as _ExprVisitor, Binary as _Binary, Call as _Call, Logical as _Logical, Grouping as _Grouping, Unary as _Unary, Literal as _Literal
from utils.stmt import Stmt as _Stmt, Var as _Var, Const as _Const, If as _If, While as _While, Break as _Break, Func as _Func, Block as _Block, Return as _Return, StmtVisitor as _StmtVisitor, Del as _Del, Print as _Print, Expression as _Expression

from reporter import  ResolutionError as _ResolutionError

import enum as _enum

# Fake C enum type for function type
@_enum.unique
class FunctionType(_enum.Enum):
    NONE = 0
    FUNCTION = 1


class Stack(list):
    def __init__(self):
        # For REPL sakes a pre-defined scope should be used for global vars
        self.stack = [{}]


    def push(self, item):
        self.stack.append(item)


    def pop(self):
        # return and remove last elm
        if not self.isEmpty():
            last = self.stack[-1]
            del self.stack[-1]
            return last


    def peek(self):
        if not self.isEmpty(): return self.stack[-1]


    def isEmpty(self):
        if len(self.stack) == 0:
            return True

        return False


    def __str__(self):
        return str(self.stack)


    def __repr__(self):
        return str(self.stack)


class Resolver(_ExprVisitor, _StmtVisitor):
    def __init__(self, interpreter: object, ksl: dict):
        self.currentFunction = FunctionType.NONE
        self.interpreter = interpreter
        self.scopes = Stack()
        self.ksl = ksl
        self.errors = []


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


    def visitFuncStmt(self, stmt: _Func):
        self.declare(stmt.name)
        self.define(stmt.name)

        self.resolveFunc(stmt, FunctionType.FUNCTION)

        return None


    def visitExpressionStmt(self, expression: _Expression):
        # To avoid expression ping pong
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
        return_lexeme = self.ksl[_TokenType.RETURN.value].lower()
        if self.currentFunction == FunctionType.NONE:
            err = _ResolutionError(stmt.keyword, f"Cannot return from top-level code.").report()
            self.errors.append(err)

        if (stmt.value != None):
            self.resolveStmt(stmt.value)

        return None


    def visitVariableExpr(self, expr: _Variable):
        if (self.scopes.isEmpty()) and (self.scopes.peek()[expr.name.lexeme] == False):
            err = _ResolutionError(expr.name, "Cannot read local variable in its own initializer. I.e 'Can't var a = a;'")
            self.errors.append(err)

        self.resolveLocal(expr, expr.name)

        return None


    def visitAssignExpr(self, expr: _Assign):
        self.resolveExpr(expr.value)
        self.resolveLocal(expr, expr.name)

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


    def visitGroupingExpr(self, expr: _Grouping):
        self.resolveExpr(expr.expression)

        return None


    def visitLiteralExpr(self, expr: _Literal):
        return None


    def visitLogicalExpr(self, expr: _Logical):
        self.resolveExpr(expr.left)
        self.resolveEXpr(expr.right)

        return None


    def visitUnaryExpr(self, expr: _Unary):
        self.resolveExpr(expr.right)

        return None


    def beginScope(self):
        self.scopes.push(dict())
        #print("Scope at begin: ", self.scopes.peek())


    def endScope(self):
        #print("Scope at end: ", self.scopes.peek())
        self.scopes.pop()


    # Similar to evaluate
    def resolveStmts(self, stmts: list):
        # Loop 'n' resolve
        for stmt in stmts:
            self.resolveStmt(stmt)

        return None


    # Similar to execute in interpreter
    def resolveStmt(self, stmt: _Stmt):
        #print("state of scopes in res stmt: ", self.scopes)
        stmt.accept(self)


    def resolveExpr(self, expr: _Expr):
        expr.accept(self)


    def resolveLocal(self, expr: _Expr, name: _Token):
        for i in range(len(self.scopes), 0, -1):
            if (name.lexeme in self.scopes[i]):
                self.interpreter.resolve(expr, (len(self.scopes) - 1 - i))
                return

        # Pretend its global if its not found


    def resolveFunc(self, func: _Func, type: FunctionType):
        #print("in func resolve")
        enclosingFunction = self.currentFunction
        self.currentFunction = type

        # Declare and define each param to avoid param redefinition in func body
        self.beginScope()

        for param in func.params:
            self.declare(param)
            self.define(param)

        self.resolveStmts(func.body)

        self.endScope()

        self.currentFunction = enclosingFunction


    def declare(self, name: _Token):
        #print("State of scopes in decl: ", self.scopes)
        scope = self.scopes.peek()

        try:
            if (name.lexeme in scope):
                err = _ResolutionError(name, f"Variable with the name {name.lexeme} already declared in this scope.").report()
                self.errors.append(err)

        except TypeError:
            pass

        # Mark shadow var as not ready yet
        scope[name.lexeme] = False
        #print("State of scopes in decl end: ", self.scopes)


    def define(self, name: _Token):
        if (self.scopes.isEmpty()): return

        # Mark var as live and kicking.
        self.scopes.peek()[name.lexeme] = True
