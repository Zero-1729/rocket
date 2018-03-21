# Author: Abubakar NK (Zero-1729)
# LICENSE: MIT
# Rocket Lang (Stellar) Parser (C) 2018

from utils.expr import Variable as _Variable, Assign as _Assign, Binary as _Binary, Unary as _Unary, Logical as _Logical, Grouping as _Grouping, Literal as _Literal
from utils.tokens import Token as _Token, TokenType as _TokenType, Keywords as _Keywords
from utils.reporter import ParseError as _ParseError
from utils.stmt import If as _If, Block as _Block, Print as _Print, Expression as _Expression, Var as _Var, Const as _Const, While as _While, Break as _Break


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.errors = []
        self.loopDepth = 0


    def parse(self):
        statements = []
        while not (self.isAtEnd()):
            statements.append(self.decleration())

        return statements


    def expression(self):
        return self.assignment()


    def decleration(self):
        try:
            if (self.match(_TokenType.VAR)):
                return self.varDecleration()

            elif (self.match(_TokenType.CONST)):
                return self.constDecleration()

            return self.statement()

        except _ParseError:
            self.synchronize()
            return None


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

        while (self.match(_TokenType.DIV, _TokenType.FLOOR, _TokenType.MOD, _TokenType.MULT, _TokenType.EXP)):
            operator = self.previous()

            right = self.unary()
            expr = _Binary(expr, operator, right)

        return expr


    def unary(self):
        if (self.match(_TokenType.BANG, _TokenType.MINUS, _TokenType.TILDE)):
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

        if (self.match(_TokenType.IDENTIFIER)):
            return _Variable(self.previous())

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
            self.addition()
            return None

        # '/', '//', '%', '*', '**'
        if (self.match(_TokenType.DIV, _TokenType.FLOOR, _TokenType.MOD, _TokenType.MULT, _TokenType.EXP)):
            self.error(self.previous(), "Left-hand operand missing.")
            self.mult()
            return None

        self.error(self.peek(), "Expected expression.").report()


    def statement(self):
        if (self.match(_TokenType.IF)):
            return self.ifStmt()
        
        if (self.match(_TokenType.WHILE)):
            return self.whileStmt()

        if (self.match(_TokenType.FOR)):
            return self.forStmt()

        if (self.match(_TokenType.BREAK)):
            return self.breakStmt()

        if (self.match(_TokenType.PRINT)):
            return self.printStmt()

        if (self.match(_TokenType.LEFT_BRACE)):
            return _Block(self.block())

        return self.expressionStmt()



    def OR(self):
        expr = self.AND()

        while (self.match(_TokenType.OR)):
            operator = self.previous()
            right = self.AND()

            expr = _Logical(expr, operator, right)

        return expr


    def AND(self):
        expr = self.equality()

        while (self.match(_TokenType.AND)):
            operator = self.previous()
            right = self.equality()

            expr = _Logical(expr, operator, right)

        return expr


    def ifStmt(self):
        self.consume(_TokenType.LEFT_PAREN, "Expected '(' after 'if'.")
        condition = self.expression()
        self.consume(_TokenType.RIGHT_PAREN, "Expected ')' after 'if' condition.")

        thenBranch = self.statement()

        # Predifine 'else' and 'elif' methods
        elifCondition = None
        elifThenBranch = None
        elseBranch = None

        #if (self.match(_TokenType.ELIF)):
        #    self.consume(_TokenType.LEFT_PAREN, "Expected '(' after 'elif'.")
        #    elifCondition = self.expression()
        #    self.consume(_TokenType.RIGHT_PAREN, "Expected ')' after 'elif' condition.")
        
        #    elifThenBranch = self.statement()

        if (self.match(_TokenType.ELSE)):
            elseBranch = self.statement()

        return _If(condition, thenBranch, elifCondition, elifThenBranch, elseBranch)


    def whileStmt(self):
        self.consume(_TokenType.LEFT_PAREN, "Expected '(' after 'while'")
        condition = self.expression()
        self.consume(_TokenType.RIGHT_PAREN, "Expected ')' after 'while' condition")

        try:
            self.loopDepth = self.loopDepth - 1
            body = self.statement()

            return _While(condition, body)
        
        finally:
            self.loopDepth = self.loopDepth - 1


    def forStmt(self):
        self.consume(_TokenType.LEFT_PAREN, "Expected '(' after 'for'.")

        initializer = None
        if (self.match(_TokenType.SEMICOLON)):
            initializer = None

        elif (self.match(_TokenType.VAR)):
            initializer = self.varDecleration()

        else:
            initializer = self.expressionStmt()

        condition = None
        if (self.check(_TokenType.SEMICOLON) == False):
            condition = self.expression()

        self.consume(_TokenType.SEMICOLON, "Expected ';' after loop confition.")

        increment = None
        if (self.check(_TokenType.RIGHT_PAREN) == False):
            increment = self.expression()

        self.consume(_TokenType.RIGHT_PAREN, "Expected ')' after 'for' clause.")

        try:
            self.loopDepth = self.loopDepth + 1
            body = self.statement()
        
            if (increment != None):
                body = _Block([body, increment])

            if (condition == None):
                condition = _Literal(True)

            body = _While(condition, body)

            if (initializer != None):
                body = _Block([initializer, body])

            return body

        finally:
            self.loopDepth = self.loopDepth - 1


    def breakStmt(self):
        if self.loopDepth == 0:
            self.error(_TokenType.BREAK, "'break' used outside loop")

        self.consume(_TokenType.SEMICOLON, "Expected ';' after 'break'")
        return _Break()
    
    
    def printStmt(self):
        value = self.expression()

        self.consume(_TokenType.SEMICOLON, "Expected ';' after expression.")
        return _Print(value)


    def varDecleration(self):
        name = self.consume(_TokenType.IDENTIFIER, "Expected variable name.")

        initializer = None
        if (self.match(_TokenType.EQUAL)):
            initializer = self.expression()

        self.consume(_TokenType.SEMICOLON, "Expected ';' after decleration.")
        return _Var(name, initializer)

    
    def constDecleration(self):
        name = self.consume(_TokenType.IDENTIFIER, "Expected variable name.")
        initializer = '' # To avoid Python reference errors

        if (self.match(_TokenType.EQUAL)):
            initializer = self.expression()
        
        else:
            self.consume(_TokenType.EQUAL, "Const variables require initializers.")

        self.consume(_TokenType.SEMICOLON, "Expected ';' after decleration.")

        # BUG #19: 'Const' are re-assignable using 'const' decl
        # E.g const y = 9; // Perfectly legit
        # y = 8; // This is detected and reported 
        # But this is allowed 'const y = 10;' 
        # Maybe leaving bug is good??

        return _Const(name, initializer)


    def expressionStmt(self):
        value = self.expression()
        self.consume(_TokenType.SEMICOLON, "Expected ';' after expression.")
        return _Expression(value)


    def assignment(self):
        # Short circuit
        expr = self.OR()# self.equality()

        if (self.match(_TokenType.EQUAL)):
            equals = self.previous()
            value = self.assignment()

            if (isinstance(expr, _Variable)):
                name = expr.name
                return _Assign(name, value)

            self.error(equals, "Invalid assignment target.") # E.g a + b = 1

        return expr


    def block(self):
        statements = []

        # Grab enclosed statements in block
        while not self.check(_TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.decleration())

        self.consume(_TokenType.RIGHT_BRACE, "Expected matching '}' after block")

        return statements


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
                _TokenType.CONST,
                _TokenType.FOR,
                _TokenType.IF,
                _TokenType.WHILE,
                _TokenType.PRINT,
                _TokenType.WHILE
            ]

            if self.peek().type in starters:
                return

            self.advance()
