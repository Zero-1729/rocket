# Author: Abubakar NK (Zero-1729)
# LICENSE: MIT
# Rocket Lang (Stellar) Parser (C) 2018

from utils.expr import Variable as _Variable, Assign as _Assign, Binary as _Binary, Call as _Call, Get as _Get, Set as _Set, Super as _Super, This as _This, Unary as _Unary, Logical as _Logical, Grouping as _Grouping, Literal as _Literal
from utils.tokens import Token as _Token, TokenType as _TokenType, Keywords as _Keywords
from utils.reporter import ParseError as _ParseError
from utils.stmt import If as _If, Func as _Func, Class as _Class, Block as _Block, Print as _Print, Expression as _Expression, Var as _Var, Const as _Const, While as _While, Break as _Break, Return as _Return, Del as _Del


class Parser:
    def __init__(self, tokens, ksl):
        self.tokens = tokens
        self.ksl = ksl
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

        while (self.match(_TokenType.PLUS, _TokenType.MINUS, _TokenType.LESS_LESS, _TokenType.GREATER_GREATER)):
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

        return self.call()


    def call(self):
        expr = self.primary()

        while True:
            if self.match(_TokenType.LEFT_PAREN):
                expr = self.finishCall(expr)

            elif (self.match(_TokenType.DOT)):
                name = self.consume(_TokenType.IDENTIFIER, "Expected property name after '.'.")
                expr = _Get(expr, name)

            else:
                break

        return expr


    def primary(self):
        if (self.match(_TokenType.FALSE)): return _Literal(False)
        if (self.match(_TokenType.TRUE)): return _Literal(True)
        if (self.match(_TokenType.NIN)): return _Literal(None)

        if (self.match(_TokenType.NUMBER, _TokenType.STRING)):
            return _Literal(self.previous().literal)

        if (self.match(_TokenType.THIS)):
            return _This(self.previous())

        if (self.match(_TokenType.SUPER)):
            super_lexeme = self.ksl[_TokenType.SUPER.value]

            keyword = self.previous()
            self.consume(_TokenType.DOT, f"Expected '.' after '{super_lexeme}'")

            method = self.consume(_TokenType.IDENTIFIER, "Expected superclass method name.")

            return _Super(keyword, method)

        if (self.match(_TokenType.IDENTIFIER)):
            return _Variable(self.previous())

        if (self.match(_TokenType.LEFT_PAREN)):
            expr = self.expression()
            self.consume(_TokenType.RIGHT_PAREN, "Expected closing ')' after expression")
            return _Grouping(expr)


        if (self.match(_TokenType.RIGHT_PAREN)):
            self.error(self.previous(), "Expected matching '(' before closing ')'.")


        if (self.match(_TokenType.RIGHT_BRACE)):
            self.error(self.previous(), "Expected matching '{' before closing '}'.")

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

        # '<<', '>>' bitshifters
        if (self.match(_TokenType.LESS_LESS, _TokenType.GREATER_GREATER)):
            self.error(self.previous(), "Left-hand operand missing.")
            self.addition()
            return None

        if (self.match(_TokenType.GREATER_GREATER)):
            self.error(self.previous(), "Left-hand operand missing.")
            self.addition()
            return None

        self.error(self.peek(), "Expected expression.").report()



    def statement(self):
        if (self.match(_TokenType.IF)):
            return self.ifStmt()

        # To sew bug #555
        # Bug #555: `if (true) {print 0; else` causes forever loop here.
        if (self.match(_TokenType.ELSE)):
            if_lexeme = self.ksl[_TokenType.IF.value].lower()
            else_lexeme = self.ksl[_TokenType.ELSE.value].lower()

            self.error(self.peek(), f"Can't use '{else_lexeme}' without beginning '{if_lexeme}'.")

        if (self.match(_TokenType.WHILE)):
            return self.whileStmt()

        if (self.match(_TokenType.FOR)):
            return self.forStmt()

        if (self.match(_TokenType.BREAK)):
            return self.breakStmt()

        if (self.match(_TokenType.RETURN)):
            return self.returnStmt()

        if (self.match(_TokenType.DEL)):
            return self.delStmt()

        if (self.match(_TokenType.PRINT)):
            return self.printStmt()

        if (self.match(_TokenType.CLASS)):
            return self.classDecleration()

        if (self.match(_TokenType.FUNC)):
            return self.function("function")

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
        if_lexeme = self.ksl[_TokenType.IF.value].lower()
        self.consume(_TokenType.LEFT_PAREN, f"Expected '(' after '{if_lexeme}'.")
        condition = self.expression()
        self.consume(_TokenType.RIGHT_PAREN, f"Expected ')' after '{if_lexeme}' condition.")

        thenBranch = self.statement()

        # Predifine 'else' methods
        elseBranch = None

        if (self.match(_TokenType.ELSE)):
            elseBranch = self.statement()

        return _If(condition, thenBranch, elseBranch)


    def whileStmt(self):
        while_lexeme = self.ksl[_TokenType.WHILE.value].lower()
        self.consume(_TokenType.LEFT_PAREN, f"Expected '(' after '{while_lexeme}'")
        condition = self.expression()
        self.consume(_TokenType.RIGHT_PAREN, f"Expected ')' after '{while_lexeme}' condition")

        try:
            self.loopDepth = self.loopDepth - 1
            body = self.statement()

            return _While(condition, body)

        finally:
            self.loopDepth = self.loopDepth - 1


    def forStmt(self):
        for_lexeme = self.ksl[_TokenType.FOR.value].lower()
        self.consume(_TokenType.LEFT_PAREN, f"Expected '(' after '{for_lexeme}'.")

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

        self.consume(_TokenType.RIGHT_PAREN, f"Expected ')' after '{for_lexeme}' clause.")

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
        break_lexeme = self.ksl[_TokenType.BREAK.value].lower()
        if self.loopDepth == 0:
            self.error(_TokenType.BREAK, f"'{break_lexeme}' used outside loop")

        self.consume(_TokenType.SEMICOLON, f"Expected ';' after '{break_lexeme}'")
        return _Break()


    def returnStmt(self):
        return_lexeme = self.ksl[_TokenType.RETURN.value].lower()
        keyword = self.previous()
        value = None

        # IF stmt hasn't ended set return val to the expression
        if not self.check(_TokenType.SEMICOLON):
            value = self.expression()

        self.consume(_TokenType.SEMICOLON, f"Expected ';' after {return_lexeme} value")
        return _Return(keyword, value)


    def delStmt(self):
        del_lexeme = self.ksl[_TokenType.DEL.value].lower()

        names = []

        if not self.check(_TokenType.SEMICOLON) and not self.isAtEnd():

            name = self.consume(_TokenType.IDENTIFIER, f"'{del_lexeme}' expected identifier name")

            # Name sometimes skipped when comma is after del keyword
            # So we check for that here
            if name == None:
                self.error(del_lexeme, f"'{del_lexeme}' detected trailing comma before any names")

            else:
                names.append(name.lexeme)


            while self.match(_TokenType.COMMA):
                # Fully patch this 'del p, ' edge case
                if self.peek().type != _TokenType.EOF and self.peek().type != _TokenType.SEMICOLON:
                    name = self.consume(_TokenType.IDENTIFIER, f"'{del_lexeme}' expected identifier name")
                    names.append(name.lexeme)

                else:
                    self.error(del_lexeme, "Detected incomplete statememt.")

        self.consume(_TokenType.SEMICOLON, f"'{del_lexeme}' expected ';' after names")

        if self.tokens[-1].type != _TokenType.DEL:
            return _Del(names)

        if len(names) == 0:
            self.error(_TokenType.DEL, f"'{del_lexeme}' requires atleast one identifier")

        return _Del(names)


    def printStmt(self):
        print_lexeme = self.ksl[_TokenType.PRINT.value].lower()
        value = self.expression()

        self.consume(_TokenType.SEMICOLON, f"'{print_lexeme}' expected ';' after expression.")
        return _Print(value)


    def varDecleration(self):
        var_lexeme = self.ksl[_TokenType.VAR.value].lower()
        initializer = None
        name = None

        # perform little peep to destroy bug; [FIXED] var t(0, 9) = 8; or just var t(0, 9);
        # Uncle bug is now: var t(0, or var t(0,) or t(0, 0) or var t(0, 0);, etc.
        # Fix: we only consume name of var only whence the next token is not SEMICOLON
        # same fix is applied to patch 'const' below

        if (self.peekNext().type != _TokenType.LEFT_PAREN):
            name = self.consume(_TokenType.IDENTIFIER, f"'{var_lexeme}' expected variable name.")

        else:
            self.error(self.peek(), f"'{var_lexeme}' can't declare class instance.")


        if (self.match(_TokenType.EQUAL)):
            initializer = self.expression()

        self.consume(_TokenType.SEMICOLON, f"'{var_lexeme}' expected ';' after decleration.")
        return _Var(name, initializer)


    def constDecleration(self):
        const_lexeme = self.ksl[_TokenType.CONST.value].lower()

        name = None
        initializer = '' # To avoid Python reference errors


        if (self.peekNext().type != _TokenType.LEFT_PAREN):
            name = self.consume(_TokenType.IDENTIFIER, f"'{const_lexeme}' expected variable name.")

        else:
            self.error(self.peek(), f"'{const_lexeme}' can't declare class instance.")

        if (self.match(_TokenType.EQUAL)):
            initializer = self.expression()

        else:
            self.consume(_TokenType.EQUAL, f"'{const_lexeme}' variables require initializers.")

        self.consume(_TokenType.SEMICOLON, f"'{const_lexeme}' expected ';' after decleration.")

        # BUG #19: 'Const' are re-assignable using 'const' decl
        # E.g const y = 9; // Perfectly legit
        # y = 8; // This is detected and reported
        # But this is allowed 'const y = 10;'
        # Maybe leaving bug is good??

        return _Const(name, initializer)


    def classDecleration(self):
        class_lexeme = self.ksl[_TokenType.CLASS.value].lower()
        name = self.consume(_TokenType.IDENTIFIER, f"Expected '{class_lexeme}' name.")

        superclass = None
        if (self.match(_TokenType.LESS)):
            self.consume(_TokenType.IDENTIFIER, "Expected superclass name after '<'.")
            superclass = _Variable(self.previous())

        self.consume(_TokenType.LEFT_BRACE, "Expected '{' before " + class_lexeme + " body.")

        methods = []

        while (not self.check(_TokenType.RIGHT_BRACE)) and (not self.isAtEnd()):
            methods.append(self.function("method"))

        self.consume(_TokenType.RIGHT_BRACE, "Expected closing '}' after " + class_lexeme + " body.")

        return _Class(name, superclass, methods)


    def expressionStmt(self):
        value = self.expression()

        # '<keyword> <expr> ;,' causes loop. So we check for any trailing commas after ';'
        self.consume(_TokenType.SEMICOLON, "Expected ';' after expression.")
        self.consume(_TokenType.COMMA, "Expected ';' after expression.")

        return _Expression(value)


    def assignment(self):
        # Short circuit
        expr = self.OR()

        if (self.match(_TokenType.EQUAL)):
            equals = self.previous()
            value = self.assignment()

            if (isinstance(expr, _Variable)):
                name = expr.name
                return _Assign(name, value)

            if (isinstance(expr, _Get)):
                return _Set(expr.object, expr.name, value)

            self.error(equals, "Invalid assignment target.") # E.g a + b = 1

        return expr


    def block(self):
        statements = []

        # Grab enclosed statements in block
        while not self.check(_TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.decleration())

        self.consume(_TokenType.RIGHT_BRACE, "Expected matching '}' after block")

        return statements


    def finishCall(self, callee: _Call):
        # Rocket should be able to parse unlimited args
        args = []
        # Find better implementation of 'do while'
        if not self.check(_TokenType.RIGHT_PAREN):
            args.append(self.expression())
            while self.match(_TokenType.COMMA):
                args.append(self.expression())

        paren = self.consume(_TokenType.RIGHT_PAREN, "Expected ')' after function arguments")

        return _Call(callee, paren, args)


    def function(self, kind):
        func_lexeme = self.ksl[_TokenType.FUNC.value].lower()
        # Fix this !!!
        name = self.consume(_TokenType.IDENTIFIER, f"'{func_lexeme}' expected '{kind}' name")

        self.consume(_TokenType.LEFT_PAREN, f"'{func_lexeme}' expected '(' after '{kind}' name")
        params = []

        if not self.check(_TokenType.RIGHT_PAREN):
            params.append(self.consume(_TokenType.IDENTIFIER, f"'{func_lexeme}' expected param name"))

            while self.match(_TokenType.COMMA):
                if len(params) >= 32:
                    self.error(self.peek(), f"'{func_lexeme}' cannot have more tan 32 params")

                params.append(self.consume(_TokenType.IDENTIFIER, f"'{func_lexeme}' expected param name"))

        self.consume(_TokenType.RIGHT_PAREN, f"'{func_lexeme}' expected ')' after params")

        # chew '{' to indecate start block
        self.consume(_TokenType.LEFT_BRACE, f"'{func_lexeme}'" + " expected '{' to indicate start of '" + kind + "' body")

        body = self.block()

        return _Func(name, params, body)


    def peek(self):
        return self.tokens[self.current]


    def peekNext(self):
        if not self.isAtEnd():
            return self.tokens[self.current + 1]

        return "\0"


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

        # Right, so the KSL hack is easier when the _TokenType's 'values' are compared and not the object themselves
        # Should still be consostent since the fake 'Enum's are uniquely identified with numbers
        return self.peek().type.value == type.value


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
