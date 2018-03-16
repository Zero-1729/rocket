# Author: Abubakar NK (Zero-1729)
# LICENSE: MIT
# Rocket Lang (Stellar) Interpreter (C) 2018

from utils.expr import Expr as _Expr, Visitor as _Visitor, Binary as _Binary, Grouping as _Grouping, Unary as _Unary, Literal as _Literal
from utils.reporter import runtimeError as _RuntimeError
from utils.tokens import Token as _Token, TokenType as _TokenType


class Interpreter(_Visitor):
    def __init__(self):
        self.errors = []

    
    def interpret(self, expr: _Expr):
        try:
            value = self.evaluate(expr)
            value = self.stringify(value)
            print(value)

        except _RuntimeError as error:
            self.errors.append(error)


    def visitLiteralExpr(self, expr: _Literal):
        return expr.value


    def visitGroupingExpr(self, expr: _Grouping):
        return self.evaluate(expr.expression)


    def visitUnaryExpr(self, expr: _Unary):
        right = self.evaluate(expr.right)

        if (expr.operator.type == _TokenType.MINUS):
            self.checkNumberOperand(expr.operator, right)
            return -float(right)

        if (expr.operator.type == _TokenType.BANG):
            return not (isTruthy(right))

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

            raise _RuntimeError(expr.operator.lexeme, "Operands must be either both strings or both numbers.")

        # Arithmetic operators "-", "/", "%", "//", "*"
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


    def evaluate(self, expr: _Expr):
        return expr.accept(self)


    def isTruthy(self, obj: object):
        if (obj == None):
            return false

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
        if (value == None): return "nin"
        if (isinstance(value, float)): return str(value)[0:-2]

        return value
