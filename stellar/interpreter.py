# Author: Abubakar NK (Zero-1729)
# LICENSE: MIT
# Rocket Lang (Stellar) Interpreter (C) 2018

from utils.expr import Expr as _Expr, Assign as _Assign, Variable as _Variable, ExprVisitor as _ExprVisitor, Binary as _Binary, Logical as _Logical, Grouping as _Grouping, Unary as _Unary, Literal as _Literal
from utils.reporter import runtimeError as _RuntimeError, BreakException as _BreakException
from utils.tokens import Token as _Token, TokenType as _TokenType
from utils.stmt import Stmt as _Stmt, Var as _Var, Const as _Const, If as _If, While as _While, Break as _Break, Block as _Block, StmtVisitor as _StmtVisitor, Print as _Print, Expression as _Expression
from env import Environment as _Environment


class Interpreter(_ExprVisitor, _StmtVisitor):
    def __init__(self):
	    self.environment = _Environment()
	    self.errors = []


    def interpret(self, statements: list):
        try:
            for stmt in statements:
                self.execute(stmt)

        except _RuntimeError as error:
            self.errors.append(error)


    def visitLiteralExpr(self, expr: _Literal):
        return expr.value


    def visitGroupingExpr(self, expr: _Grouping):
        return self.evaluate(expr.expression)


    def visitUnaryExpr(self, expr: _Unary):
        right = self.evaluate(expr.right)

        # Handle '~' bit shifter
        if (expr.operator.type == _TokenType.TILDE):
            self.checkNumberOperand(expr.operator, right)
            return (-float(right) - 1)

        if (expr.operator.type == _TokenType.MINUS):
            self.checkNumberOperand(expr.operator, right)
            return -float(right)

        if (expr.operator.type == _TokenType.BANG):
            return not (self.isTruthy(right))

        # If can't be matched return nothing
        return None


    def visitBinaryExpr(self, expr: _Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        # string concatination and arithmetic operator '+'
        if (expr.operator.type == _TokenType.PLUS):
            if (isinstance(left, float) and isinstance(right, float)):
                return left + right

            if (isinstance(left, str) and isinstance(right, str)):
                return left + right

            # To support implicit string concactination
            # E.g "Hailey" + 4 -> "Hailey4"
            if ((isinstance(left, str)) or (isinstance(right, str))):
                return str(left) + str(right)

            raise _RuntimeError(expr.operator.lexeme, "Operands must be either both strings or both numbers.")

        # Arithmetic operators "-", "/", "%", "//", "*", "**"
        if (expr.operator.type == _TokenType.MINUS):
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) - float(right)

        if (expr.operator.type == _TokenType.DIV):
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) / float(right)

        if (expr.operator.type == _TokenType.MOD):
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) % float(right)

        if (expr.operator.type == _TokenType.FLOOR):
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) // float(right)

        if (expr.operator.type == _TokenType.MULT):
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) * float(right)

        if (expr.operator.type == _TokenType.EXP):
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) ** float(right)

        # Comparison operators ">", "<", ">=", "<=", "!=", "=="
        if (expr.operator.type == _TokenType.GREATER):
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) > float(right)

        if (expr.operator.type == _TokenType.LESS):
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) < float(right)

        if (expr.operator.type == _TokenType.GREATER_EQUAL):
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) >= float(right)

        if (expr.operator.type == _TokenType.LESS_EQUAL):
            self.checkNumberOperands(expr.operator, left, right)
            return float(left) <= float(right)

        if (expr.operator.type == _TokenType.BANG_EQUAL):
            self.checkNumberOperands(expr.operator, left, right)
            return not (self.isEqual(left, right))

        if (expr.operator.type == _TokenType.EQUAL_EQUAL):
            self.checkNumberOperands(expr.operator, left, right)
            return self.isEqual(left, right)

        # TODO: Maybe add exp operator like Python's "**"

        # If can't be matched return None
        return None


    def visitExpressionStmt(self, stmt: _Expression):
        self.evaluate(stmt.expression)
        return None


    def visitLogicalExpr(self, expr: _Logical):
        left = self.evaluate(expr.left)

        if (expr.operator.type == _TokenType.OR):
            if (self.isTruthy(left)): return left
        
        else:
            if not self.isTruthy(left): return left

        return self.evaluate(expr.right)


    def visitIfStmt(self, stmt: _If):
         if (self.isTruthy(self.evaluate(stmt.condition))):
             self.execute(stmt.thenBranch)
         
         #if (stmt.elifCondition != None):
         #    if (self.isTruthy(self.evaluate(stmt.elifCondition))):
         #        self.execute(stmt.elifThenBranch)

         elif (stmt.elseBranch != None):
             self.execute(stmt.elseBranch)

         return None


    def visitWhileStmt(self, stmt: _While):
        try:
            while (self.isTruthy(self.evaluate(stmt.condition))):
                self.execute(stmt.body)

            # TODO: Add support to cover Python's stack trace when CTRL-C is used to exit REPL
        except _BreakException:
            pass

        return None


    def visitBreakStmt(self, stmt: _Break):
        # Just raises 'BreakExveption' to signal 'break'
        raise _BreakException()


    def visitPrintStmt(self, stmt: _Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None


    def visitVarStmt(self, stmt: _Var):
        if (stmt.initializer is not None):
            value = self.evaluate(stmt.initializer)
        else:
            value = None

        self.environment.define(stmt.name.lexeme, value)


    def visitConstStmt(self, stmt: _Const):
        value = self.evaluate(stmt.initializer)

        # NOTE: Fix for #19 
        # check for variable before definition to avoid passing in 'const' redefinitions
        if self.environment.isTaken(stmt.name):
            raise _RuntimeError(stmt.name.lexeme, "Name already used as 'const'.")

        # Use different decleration function for consts
        self.environment.decl(stmt.name.lexeme, value)


    def visitBlockStmt(self, stmt: _Block):
        self.executeBlock(stmt.statements, _Environment(self.environment))
        return None


    def visitAssignExpr(self, expr: _Assign):
        value = self.evaluate(expr.value)

        self.environment.assign(expr.name, value)
        return value


    def visitVariableExpr(self, expr: _Variable):
        # NOTE: 'const' variables get retrieved from this call also
        return self.environment.get(expr.name)


    def execute(self, stmt: _Stmt):
        stmt.accept(self)


    def executeBlock(self, stmts: list, env: _Environment):
        # Save global environment state
        previous = self.environment

        try:
            self.environment = env

            for stmt in stmts:
                self.execute(stmt)

        finally:
            # Resume global environment state
            self.environment = previous


    def evaluate(self, stmt: _Stmt):
        return stmt.accept(self)


    def isTruthy(self, obj: object):
        if (obj == None):
            return False

        if (isinstance(obj, bool)):
            return obj # I.e if "True" return it

        # If its neight false or "bool" type then it is truthy
        return True


    def isEqual(self, left_obj: object, right_obj: object):
        if ((left_obj == None) and (right_obj == None)):
            return True

        # Nothing but "nin" (None) is equal to it
        if (left_obj == None):
            return False

        return left_obj == right_obj


    def checkNumberOperand(self, opetator: _Token, right: object):
        if (isinstance(right, float)): return

        raise _RuntimeError(operator.lexeme, "Operand must be number.")


    def checkNumberOperands(self, operator: _Token, left: object, right: object):
        if ((isinstance(left, float)) and (isinstance(right, float))): return

        raise _RuntimeError(operator.lexeme, "Operands must be numbers.")


    def stringify(self, value: object):
        # Customize literals
        if (value == None): return "nin"

        # HACK: Against bug #28 'print 0;' -> false && 'print 1;' -> true
        if (value == True and not isinstance(value, float)): return "true"
        if (value == False and not isinstance(value, float)): return "false"

        # check for ints to avoid '1' -> '1.0'
        if (isinstance(value, float)): return str(value)[0:-2]

        return value
