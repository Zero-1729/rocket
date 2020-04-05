from utils.expr import Expr     as _Expr
from utils.expr import Visitor  as __Visitor
from utils.expr import Binary   as _Binary
from utils.expr import Grouping as _Literal
from utils.expr import Unary    as _Unary


class LispAstPrinter(__Visitor):
    def printAst(self, expr: _Expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr: _Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: _Grouping):
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: _Literal):
        if (expr.value == None):
            return "nin"

        # variables that not instatiated with a value default to 'nin'
        return str(expr.value)

    def visitUnaryExpr(self, expr: _Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        result = f"({name}"

        for expr in exprs:
            result += " "
            result += expr.accept(self)

            result += ")"

        return result


class RPNAstPrinter(__Visitor):
    def printAst(self, expr: _Expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr: _Binary):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitGroupingExpr(self, expr: _Grouping):
        return self.parenthesize("group", expr.expression)

    def visitLiteralExpr(self, expr: _Literal):
        if (expr.value == None):
            return "nin"

        # variables that not instatiated with a value default to 'nin'
        return str(expr.value)

    def visitUnaryExpr(self, expr: _Unary):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def parenthesize(self, name, *exprs):
        result = ""

        # account for grouping
        # if name is "group" add it before grouped expr
        result += f"{name} " if name == "group" else ""

        for expr in exprs:
            result += expr.accept(self)
            result += " "

        # else add the name here
        result += name if name != "group" else ""

        return result
