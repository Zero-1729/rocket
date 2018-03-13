# Author: Abubakar NK (Zero-1729)
# LICENSE: MIT
# Rocket Lang (Stellar) Parser (C) 2018

from utils.expr import Binary as _Binary, Unary as _Unary, Grouping as _Grouping, Literal as _Literal
from utils.tokens import Token as _Token, TokenType as _TokenType, Keywords as _Keywords
from utils.reporter import ParseError as _ParseError


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.statements = []
        self.errors = []


    def parse(self):
        try:
            return self.expression()

        except _ParseError:
            return None


    def expression(self):
        return self.equality()


    def equality(self):
        expr = self.comparison() # Type: Expr

        while (self.match(_TokenType.BANG_EQUAL, _TokenType.EQUAL_EQUAL)):
            operator = self.previous() # Type: Token

            right = self.comparison()
            expr = _Binary(expr, operator, right)

        return expr


    def comparison(self):
        expr = self.addition()

        while (self.match(_TokenType.GREATER, _TokenType.GREATER_EQUAL, _TokenType.LESS, _TokenType.LESS_EQUAL)):
            operator = self.previous()

            right = self.addition()
            expr = _Binary(expr, operator, right)

        return expr


    def addition(self):
        expr = self.mult()

        while (self.match(_TokenType.PLUS, _TokenType.MINUS)):
            operator = self.previous()

            right = self.mult()
            expr = _Binary(expr, operator, right)

        return expr


    def mult(self):
        expr = self.unary()

        while (self.match(_TokenType.DIV, _TokenType.FLOOR, _TokenType.MOD, _TokenType.MULT)):
            operator = self.previous()

            right = self.unary()
            expr = _Binary(expr, operator, right)

        return expr


    def unary(self):
        if (self.match(_TokenType.BANG, _TokenType.MINUS)):
            operator = self.previous()

            right = self.unary()

            return _Unary(operator, right)

        return self.primary()


    def primary(self):
        if (self.match(_TokenType.FALSE)): return _Literal(False)
        if (self.match(_TokenType.TRUE)): return _Literal(True)
        if (self.match(_TokenType.NIN)): return _Literal(None)

        if (self.match(_TokenType.NUMBER, _TokenType.STRING)):
            return _Literal(self.previous().literal)

        if (self.match(_TokenType.LEFT_PAREN)):
            expr = self.expression()
            self.consume(_TokenType.RIGHT_PAREN, "Expected closing ')' after expression")
            return _Grouping(expr)

        # Error productions
        # for '!=', '=='
        if (self.match(_TokenType.BANG_EQUAL, _TokenType.EQUAL_EQUAL)):
            self.error(self.previous, "Left-hand operand missing.")
            self.equality()
            return None

        # '>', '<', '>=', '<='
        if (self.match(_TokenType.GREATER, _TokenType.LESS, _TokenType.GREATER_EQUAL, _TokenType.LESS_EQUAL)):
            self.error(self.previous(), "Left-hamd operand missing.")
            self.comparison()
            return None

        # '+', '-'
        if (self.match(_TokenType.PLUS)): # _TokenType.MINUS
            self.error(self.previous(), "Left-hand operand missing.")
            self.additon()
            return None

        # '/', '//', '%', '*'
        if (self.match(_TokenType.DIV, _TokenType.FLOOR, _TokenType.MOD, _TokenType.MULT)):
            self.error(self.previous(), "Left-hand operand missing.")
            self.mult()
            return None

        self.error(self.peek(), "Expected expression.").report()


    def peek(self):
        return self.tokens[self.current]


    def previous(self):
        return self.tokens[self.current - 1]


    def isAtEnd(self):
        return self.peek().type == _TokenType.EOF


    def advance(self):
        if not self.isAtEnd():
            self.current += 1

        return self.previous()


    def match(self, *types: _TokenType):
        for type in types:
            if self.check(type):
                self.advance()
                return True

        return False


    def check(self, type: _TokenType):
        if self.isAtEnd():
            return False

        return self.peek().type == type


    def consume(self, toke_type, err):
        if (self.check(toke_type)): return self.advance()

        self.error(self.peek(), err).report()


    def error(self, token: _Token, message: str):
        err = _ParseError(token, message)
        self.errors.append(err)

        return err


    def synchronize(self):
        self.advance()

        while not self.isAtEnd():
            if (self.previous().type == _TokenType.SEMICOLON):
                return

            starters = [
                _TokenType.CLASS,
                _TokenType.FUNC,
                _TokenType.VAR,
                _TokenType.FOR,
                _TokenType.IF,
                _TokenType.WHILE,
                _TokenType.PRINT,
                _TokenType.WHILE
            ]

            if self.peek().type in starters:
                return

            self.advance()
