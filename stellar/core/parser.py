# Author: Abubakar Nur Kahlil (Zero-1729)
# LICENSE: RLOL
# Rocket Lang (Stellar) Parser (C) 2018

from utils.expr import Variable      as _Variable
from utils.expr import Assign        as _Assign
from utils.expr import Binary        as _Binary
from utils.expr import Call          as _Call
from utils.expr import Get           as _Get
from utils.expr import Set           as _Set
from utils.expr import Function      as _Function
from utils.expr import Conditional   as _Conditional
from utils.expr import Super         as _Super
from utils.expr import This          as _This
from utils.expr import Unary         as _Unary
from utils.expr import Logical       as _Logical
from utils.expr import Grouping      as _Grouping
from utils.expr import Literal       as _Literal

from utils.tokens import Token       as _Token
from utils.tokens import TokenType   as _TokenType

from utils.reporter import ParseError  as _ParseError

from utils.stmt import If            as _If
from utils.stmt import Func          as _Func
from utils.stmt import Class         as _Class
from utils.stmt import Block         as _Block
from utils.stmt import Import        as _Import
from utils.stmt import Print         as _Print
from utils.stmt import Expression    as _Expression
from utils.stmt import Var           as _Var
from utils.stmt import Const         as _Const
from utils.stmt import While         as _While
from utils.stmt import Break         as _Break
from utils.stmt import Return        as _Return
from utils.stmt import Del           as _Del


class Parser:
    def __init__(self, tokens, vw_Dict):
        self.tokens = tokens
        self.vw_Dict = vw_Dict
        self.current = 0
        self.errors = []
        self.loopDepth = 0

    def parse(self):
        statements = []
        while not (self.isAtEnd()):
            statements.append(self.declaration())

        return statements

    def expression(self):
        return self.assignment()

    def declaration(self):
        try:
            if (self.checkNext(_TokenType.IDENTIFIER) and self.match(_TokenType.FUNC)):
                return self.function('function')

            if (self.match(_TokenType.VAR)):
                return self.varDeclaration()

            if (self.match(_TokenType.CONST)):
                return self.constDeclaration()

            return self.statement()

        except _ParseError:
            self.synchronize()
            return None

    def statement(self):
        if (self.match(_TokenType.IF)):
            return self.ifStmt()

        # To sew bug #555
        # Bug #555: `if (true) {print 0; else` causes forever loop here.
        if (self.match(_TokenType.ELSE)):
            if_lexeme = self.vw_Dict[_TokenType.IF.value]
            else_lexeme = self.vw_Dict[_TokenType.ELSE.value]

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

        if (self.match(_TokenType.IMPORT)):
            return self.importStmt()

        if (self.match(_TokenType.PRINT)):
            if self.peek().type.value == _TokenType.LEFT_PAREN.value:
                print_lexeme = self.vw_Dict[_TokenType.PRINT.value]

                self.error(self.peek(), f"'{print_lexeme}' is a keyword 'Print' is the native Function. Use 'Print' instead.")

            else: return self.printStmt()

        if (self.match(_TokenType.CLASS)):
            return self.classDeclaration()

        if (self.match(_TokenType.LEFT_BRACE)):
            return _Block(self.block())

        return self.expressionStmt()

    def conditional(self):
        expr = self.equality()

        if self.match(_TokenType.Q_MARK):
            thenExpr = self.expression()
            self.consume(_TokenType.COLON, "Expected ':' after then expression branch of the conditional expression")

            elseExpr = self.conditional()
            expr = _Conditional(expr, thenExpr, elseExpr)

        return expr

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

        if isinstance(expr, _Variable):
            if self.peek().type.value == _TokenType.PLUS.value and self.peekNext().type.value == _TokenType.PLUS.value:
                expr = _Assign(expr.name, [expr.name, 1, 'inc'])

                # Continue parsing after post inc expr '++'
                self.advance()
                self.advance()

            if self.peek().type.value == _TokenType.MINUS.value and self.peekNext().type.value == _TokenType.MINUS.value:
                expr = _Assign(expr.name, [expr.name, -1, 'dec'])

                # Continue parsing after post inc expr '--'
                self.advance()
                self.advance()

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

        if (self.match(_TokenType.FUNC)):
            return self.anonFunction('function')

        if (self.match(_TokenType.THIS)):
            return _This(self.previous())

        if (self.match(_TokenType.SUPER)):
            super_lexeme = self.vw_Dict[_TokenType.SUPER.value]

            keyword = self.previous()
            self.consume(_TokenType.DOT, f"Expected '.' after '{super_lexeme}'")

            method = self.consume(_TokenType.IDENTIFIER, "Expected superclass method name.")

            return _Super(keyword, method)

        if (self.match(_TokenType.IDENTIFIER)):
            return _Variable(self.previous())

        if (self.match(_TokenType.LEFT_PAREN)):
            # Branch to handle Js (ES6) styled fn lambdas
            # I.e `var connect = (addr, callback) => {...}`

            # So we assume its an arrow function we are parsing...
            # Until we get a 'parseError' from our 'arrowFunc' function
            # Then we proceed to parsing it as a 'braced' expression
            try:
                return self.arrowFunc('function')
            except _ParseError:
                pass

            if self.previous().type.value == _TokenType.LEFT_PAREN.value and self.peek().type.value == _TokenType.RIGHT_PAREN.value:
                self.current += 1
                return _Literal(None)

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
            self.error(self.previous(), "Left-hand operand missing.")
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

        # The mother of all bugs!!
        # The source of all our problems
        # This is what was causing problems
        raise self.error(self.peek(), "Expected expression.")

    def OR(self):
        expr = self.AND()

        while (self.match(_TokenType.OR)):
            operator = self.previous()
            right = self.AND()
            expr = _Logical(expr, operator, right)

        return expr

    def AND(self):
        expr = self.conditional() # self.equality()

        while (self.match(_TokenType.AND)):
            operator = self.previous()
            right = self.conditional() # self.equality()

            expr = _Logical(expr, operator, right)

        return expr

    def ifStmt(self):
        if_lexeme = self.vw_Dict[_TokenType.IF.value]
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
        while_lexeme = self.vw_Dict[_TokenType.WHILE.value]
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
        for_lexeme = self.vw_Dict[_TokenType.FOR.value]
        self.consume(_TokenType.LEFT_PAREN, f"Expected '(' after '{for_lexeme}'.")

        initializer = None
        if (self.match(_TokenType.SEMICOLON)):
            initializer = None

        elif (self.match(_TokenType.VAR)):
            initializer = self.varDeclaration()

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
        break_lexeme = self.vw_Dict[_TokenType.BREAK.value]
        if self.loopDepth == 0:
            self.error(_TokenType.BREAK, f"'{break_lexeme}' used outside loop")

        self.consume(_TokenType.SEMICOLON, f"Expected ';' after '{break_lexeme}'")
        return _Break()

    def returnStmt(self):
        return_lexeme = self.vw_Dict[_TokenType.RETURN.value]
        keyword = self.previous()
        value = None

        # IF stmt hasn't ended set return val to the expression
        if not self.check(_TokenType.SEMICOLON):
            value = self.expression()

        self.consume(_TokenType.SEMICOLON, f"Expected ';' after {return_lexeme} value")

        return _Return(keyword, value)

    def delStmt(self):
        del_lexeme = self.vw_Dict[_TokenType.DEL.value]

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

    def importStmt(self):
        import_lexeme = self.vw_Dict[_TokenType.IMPORT.value]

        modules = []

        isFull = False
        shift = False

        if not self.check(_TokenType.SEMICOLON) and not self.isAtEnd():
            if self.check(_TokenType.IDENTIFIER) or self.check(_TokenType.STRING):
                modules.append(self.peek())
                self.advance()

            if self.check(_TokenType.LEFT_PAREN):
                isFull = True

                while not self.check(_TokenType.RIGHT_PAREN) and not self.isAtEnd():
                    if self.check(_TokenType.IDENTIFIER) or self.check(_TokenType.STRING):
                        modules.append(self.peek())

                    self.advance()

        if self.peek() == _TokenType.RIGHT_PAREN:
            shift = True

        if isFull:
            self.consume(_TokenType.RIGHT_PAREN, f"'(' expected closing ')' in {import_lexeme} statement")

        if shift:
            # Move beyond the ')' or only identifier
            self.advance()

        # NOTE: including ending semicolon ';' in single or multi import decleration is optional

        # We skip over the only module name parsed and the semi-colon
        # This is what enables ';' to be optional in single-module definitions
        if self.peek().type == _TokenType.SEMICOLON:
            # If the current token after
            # ... the ')' is a semi-colon (;)
            # ... we skip the semicolon itself
            # allowing for ';' after the multi-module definition to be optional
            self.advance()

        else:
            # Otherwise, we simply skip over only the single-module name
            pass

        return _Import(modules)

    def printStmt(self):
        print_lexeme = self.vw_Dict[_TokenType.PRINT.value]
        value = self.expression()

        self.consume(_TokenType.SEMICOLON, f"'{print_lexeme}' expected ';' after expression.")
        return _Print(value)

    def parseVarDecl(self, var_lexeme):
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

        self.consume(_TokenType.SEMICOLON, f"'{var_lexeme}' expected ';' after declaration.")

        return _Var(name, initializer)

    def parseConstDecl(self, const_lexeme):
        name = None
        initializer = None # To avoid Python reference errors

        if (self.peekNext().type != _TokenType.LEFT_PAREN):
            name = self.consume(_TokenType.IDENTIFIER, f"'{const_lexeme}' expected variable name.")

        else:
            self.error(self.peek(), f"'{const_lexeme}' can't declare class instance.")

        if (self.match(_TokenType.EQUAL)):
            initializer = self.expression()

        else:
            self.consume(_TokenType.EQUAL, f"'{const_lexeme}' variables require initializers.")

        self.consume(_TokenType.SEMICOLON, f"'{const_lexeme}' expected ';' after declaration.")

        # BUG #19: 'Const' are re-assignable using 'const' decl
        # E.g const y = 9; // Perfectly legit
        # y = 8; // This is detected and reported
        # But this is allowed 'const y = 10;'
        # Maybe leaving bug is good??

        return _Const(name, initializer)

    def varDeclaration(self):
        var_lexeme = self.vw_Dict[_TokenType.VAR.value]
        vars = []

        if self.match(_TokenType.LEFT_BRACE):
            # The following symbols keep giving us a hard time, so we only proceed if they aren't next:
            # '}', '{', '~', ')'
            # the combination specifically is:
            # var { [name] = [value][symbol]
            # e.g.:
            # var { n = 0~
            # NOTE: The same solution is used for const multi-var decls below
            # ... we only allow identifiers and equal sign to trigger pass
            while (self.peek().type in [_TokenType.IDENTIFIER,  _TokenType.EQUAL]):
                vars.append(self.parseVarDecl(var_lexeme))

            self.consume(_TokenType.RIGHT_BRACE, "'{}' expected closing '{}' after multi-variable declaration".format(var_lexeme, '}'))

            # This check ensures that const multi-variable declarations can end with ';'.
            # Since all statements end with ';', though it is optional for the import stmt and in multi-variable defintions
            # So both 'var {...};' and 'var {...}' are valid
            if self.peek().type == _TokenType.SEMICOLON:
                self.advance()

            # Returns a list of 'vars' if we indeed detected multi-variable declaration (i.e var {...})
            return vars


        else:
            # We simply return a single parsed variable
            return self.parseVarDecl(var_lexeme)

    def constDeclaration(self):
        const_lexeme = self.vw_Dict[_TokenType.CONST.value]
        consts = []

        if self.match(_TokenType.LEFT_BRACE):
            while (self.peek().type in [_TokenType.IDENTIFIER,  _TokenType.EQUAL]):
                consts.append(self.parseConstDecl(const_lexeme))

            self.consume(_TokenType.RIGHT_BRACE, "'{}' expected closing '{}' after multi-variable declaration".format(const_lexeme, '}'))

            # This check ensures that const multi-variable declarations can end with ';'.
            # Since all statements end with ';', though it is optional for the import stmt and in multi-variable defintions
            # So both 'const {...};' and 'const {...}' are valid
            if self.peek().type == _TokenType.SEMICOLON:
                self.advance()

        else:
            # We simply return a single parsed variable
            return self.parseConstDecl(const_lexeme)

        # Returns a list of 'vars' if we indeed detected multi-variable declaration (i.e var {...})
        return consts

    def classDeclaration(self):
        class_lexeme = self.vw_Dict[_TokenType.CLASS.value]
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

        self.consume(_TokenType.SEMICOLON, "Expected ';' after expression.")

        return _Expression(value)

    def assignment(self):
        # Short circuit
        expr = self.OR()

        # Were we handle our arithmetic assignment ops
        # I.e:- '+=', '-=', '*=', '/=', '%=', '//=', '**='
        if self.match(_TokenType.PLUS_INC):
            value = self.assignment()
            name = expr.name

            if isinstance(expr, _Variable):
                return _Assign(name, [name, value, 'add'])

            self.error(self.previous(), 'Invalid assignment target') # E.g '9 += 1'

        if self.match(_TokenType.MINUS_INC):
            value = self.assignment()
            name = expr.name

            if isinstance(expr, _Variable):
                if not isinstance(value, _Variable) and type(value.value) == str:
                    self.error(self.previous(), 'Invalid assignment target for string concatenation') # E.g 'home -= "/Github";'

                return _Assign(name, [name, value, 'sub'])

            self.error(self.previous(), 'Invalid assignment target') # E.g '9 -= 1'

        if self.match(_TokenType.MULT_INC):
            value = self.assignment()
            name = expr.name

            if isinstance(expr, _Variable):
                if not isinstance(value, _Variable) and type(value.value) == str:
                    self.error(self.previous(), 'Invalid assignment target for string concatenation') # E.g 'home *= "/Github";'

                return _Assign(name, [name, value, 'mul'])

            self.error(self.previous(), 'Invalid assignment target') # E.g '9 *= 1'

        if self.match(_TokenType.DIV_INC):
            value = self.assignment()
            name = expr.name

            if isinstance(expr, _Variable):
                if not isinstance(value, _Variable) and type(value.value) == str:
                    self.error(self.previous(), 'Invalid assignment target for string concatenation') # E.g 'home/-= "/Github";'

                return _Assign(name, [name, value, 'div'])

            self.error(self.previous(), 'Invalid assignment target') # E.g '9 /= 1'

        if self.match(_TokenType.MOD_INC):
            value = self.assignment()
            name = expr.name

            if isinstance(expr, _Variable):
                if not isinstance(value, _Variable) and type(value.value) == str:
                    self.error(self.previous(), 'Invalid assignment target for string concatenation') # E.g 'home %= "/Github";'

                return _Assign(name, [name, value, 'mod'])

            self.error(self.previous(), 'Invalid assignment target') # E.g '9 %= 1'

        if self.match(_TokenType.FLOOR_INC):
            value = self.assignment()
            name = expr.name

            if isinstance(expr, _Variable):
                if not isinstance(value, _Variable) and type(value.value) == str:
                    self.error(self.previous(), 'Invalid assignment target for string concatenation') # E.g 'home //= "/Github";'

                return _Assign(name, [name, value, 'flo'])

            self.error(self.previous(), 'Invalid assignment target') # E.g '9 //= 1'

        if self.match(_TokenType.EXP_INC):
            value = self.assignment()
            name = expr.name

            if isinstance(expr, _Variable):
                if not isinstance(value, _Variable) and type(value.value) == str:
                    self.error(self.previous(), 'Invalid assignment target for string concatenation') # E.g 'home **= "/Github";'

                return _Assign(name, [name, value, 'exp'])

            self.error(self.previous(), 'Invalid assignment target') # E.g '9 **= 1'

        # END

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
            statements.append(self.declaration())

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

    def arrowFunc(self, kind):
        func_lexeme = self.vw_Dict[_TokenType.FUNC.value]
        lockedIndex = self.current

        params = []

        if not self.check(_TokenType.RIGHT_PAREN):
            params.append(self.consume(_TokenType.IDENTIFIER, f"'{func_lexeme}' expected param name", 'silent'))

            while self.match(_TokenType.COMMA):
                if len(params) >= 32:
                    self.error(self.peek(), f"'{func_lexeme}' cannot have more than 32 params")

                params.append(self.consume(_TokenType.IDENTIFIER, f"'{func_lexeme}' expression expected param name", 'silent'))

        if self.peek().type.value != _TokenType.RIGHT_PAREN.value:
            self.advance()

        self.consume(_TokenType.RIGHT_PAREN, f"'{func_lexeme}' expression expected ')' after params", 'silent')

        if self.peek().type.value != _TokenType.ARROW.value:
            # Reset pointer
            self.current = lockedIndex
            raise _ParseError(None, None)

        self.consume(_TokenType.ARROW, None)

        # chew '{' to indecate start block
        self.consume(_TokenType.LEFT_BRACE, f"'{func_lexeme}'" + " expected '{' to indicate start of '" + kind + "' body")

        body = self.block()

        return _Function(params, body)

    def anonFunction(self, kind):
        func_lexeme = self.vw_Dict[_TokenType.FUNC.value]

        self.consume(_TokenType.LEFT_PAREN, f"'{func_lexeme}' expected '(' after '{kind}' name")
        params = []

        if not self.check(_TokenType.RIGHT_PAREN):
            params.append(self.consume(_TokenType.IDENTIFIER, f"'{func_lexeme}' expected param name"))

            while self.match(_TokenType.COMMA):
                if len(params) >= 32:
                    self.error(self.peek(), f"'{func_lexeme}' cannot have more than 32 params")

                params.append(self.consume(_TokenType.IDENTIFIER, f"'{func_lexeme}' expression expected param name"))

        self.consume(_TokenType.RIGHT_PAREN, f"'{func_lexeme}' expression expected ')' after params")

        # chew '{' to indecate start block
        self.consume(_TokenType.LEFT_BRACE, f"'{func_lexeme}'" + " expected '{' to indicate start of '" + kind + "' body")

        body = self.block()

        return _Function(params, body)

    def function(self, kind):
        func_lexeme = self.vw_Dict[_TokenType.FUNC.value]

        name = self.consume(_TokenType.IDENTIFIER, f"'{func_lexeme}' expected '{kind}' name")

        return _Func(name, self.anonFunction(kind))

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

    def checkNext(self, type: _TokenType):
        if self.isAtEnd(): return False

        if self.peekNext().type.value == _TokenType.EOF.value:
            return False

        return self.peekNext().type.value == type.value

    def consume(self, toke_type, err, form='loud'):
        if (self.check(toke_type)): return self.advance()

        if (form == 'loud'):
            self.error(self.peek(), err).report()
        else:
            self.advance()

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
                _TokenType.SUPER,
                _TokenType.OR,
                _TokenType.AND,
                _TokenType.FOR,
                _TokenType.IF,
                _TokenType.WHILE,
                _TokenType.PRINT,
                _TokenType.WHILE
            ]

            if self.peek().type in starters:
                return

            self.advance()
