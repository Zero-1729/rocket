# Author: Abubakar NK (Zero-1729)
# License: GNU GPL V2

from utils.reporter import report
from utils.tokens import Token, TokenType, Keywords

class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.current = 0
        self.line = 1

    def scan(self):
        while not (self.isAtEnd()):
            c = self.advance()

            # Check for lexemes
            # Starting with single character tokens
            if c == "(":
                tok_type = TokenType.LEFT_PAREN # "LEFT_PAREN"
                self.addSingleToken(tok_type)

            elif c == ")":
                tok_type = TokenType.RIGHT_PAREN # "RIGHT_PAREN"
                self.addSingleToken(tok_type)

            elif c == "{":
                tok_type = TokenType.LEFT_BRACE # "LEFT_BRACE"
                self.addSingleToken(tok_type)

            elif c == "}":
                tok_type = TokenType.RIGHT # "RIGHT_BRACE"
                self.addSingleToken(tok_type)

            elif c == ";":
                tok_type = TokenType.SEMICOLON # "SEMICOLON"
                self.addSingleToken(tok_type)

            elif c == ",":
                tok_type = TokenType.COMMA # "COMMA"
                self.addSingleToken(tok_type)

            elif c == ".":
                tok_type = TokenType.DOT # "DOT"
                self.addSingleToken(tok_type)

            elif c == "+":
                tok_type = TokenType.PLUS # "PLUS"
                self.addSingleToken(tok_type)

            elif c == "-":
                tok_type = TokenType.MINUS # "MINUS"
                self.addSingleToken(tok_type)

            elif c == "*":
                tok_type = TokenType.MULT # "MULT"
                self.addSingleToken(tok_type)

            elif c == "%":
                tok_type = TokenType.M0D # "MOD"
                self.addSingleToken(tok_type)

            # Double character tokens
            # check for div and comment
            # NOTE: single line comment begin with "//"
            # Floor division '//' would be in 'Math' stdlib
            elif c == "/":
                if self.match("/"):

                    if (self.futureNumberPeek()):
                        tok_type = TokenType.FLOOR # "FLOOR"
                        self.addSingleToken(tok_type)

                    else:
                        while ((self.peek() != "\n") and not (self.isAtEnd())):
                            self.advance()

                # C styled '/**/' multi-line comment
                elif self.match("*"):
                    while ((self.doublePeek() != "*/")):
                        if not self.isAtEnd():
                            self.advance()

                        else:
                            ret = report(self.line, "Unterminated comment: couldn't find matching '*/' for '/*'")
                            break

                    # Continue ignoring comments
                    if self.doublePeek() == "*/":
                        # Adnavce twice to ignore '*/'
                        self.advance()
                        self.advance()

                else:
                    obj = "DIV"
                    self.addSingleToken(obj)


            # Comparison tokens
            elif c == "!":
                if not self.match("="):
                    tok_type = TokenType.BANG # "BANG"

                else:
                    tok_type = TokenType.BANG_EQUAL # "BANG_EQUAL"
                self.addSingleToken(tok_type)

            elif c == "=":
                if not self.match("="):
                    tok_type = TokenType.EQUAL # "EQUAL"

                else:
                    tok_type = TokenType.EQUAL_EQUAL # "EQUAL_EQUAL"
                self.addSingleToken(tok_type)

            elif c == "<":
                if not self.match("="):
                    tok_type = TokenType.LESS # "LESS"

                else:
                    tok_type = TokenType.LESS_EQUAL # "LESS_EQUAL"
                self.addSingleToken(tok_type)

            elif c == ">":
                if not self.match("="):
                    tok_type = TokenType.GREATER # "GREATER"

                else:
                    tok_type = TokenType.GREATER_EQUAL # "GREATER_EQUAL"

                self.addSingleToken(tok_type)

            # literals
            elif c == "":
                tok_type = TokenType.IDENTIFIER # "IDENTIFIER"
                self.addSingleToken(tok_type)

            # string
            # NOTE: strings start with double (") or single (') quotes
            elif c == '"' or c == "'":
                if c == '"': self.string('"')
                else: self.string("'")

            # Skip tabs, spaces, etc
            elif c == " " or c == "\t" or c == "\r":
                pass

            elif c == "\n":
                self.line += 1

            # Check for unhandled symbols
            else:
                if (self.isDigit(c)):
                    self.number()

                elif (self.isAlpha(c)):
                    self.identifier()

                else:
                    report(self.line, f"Unrecognized symbol '{c}'")

        self.addToken(TokenType.EOF, '', None)
        return self.tokens


    def advance(self):
        self.current += 1
        index = self.current - 1
        return self.source[index]


    def peek(self):
        if self.isAtEnd():
            return "\0"

        return self.source[self.current]

    def doublePeek(self):
        if self.wouldBeAtEnd():
            return "\0"

        return self.source[self.current:self.current + 2]

    def futureNumberPeek(self):
        doublePeeked = self.doublePeek()
        future_character = self.source[self.source.index(doublePeeked) + 1]

        if (self.isDigit(future_character)):
            return True

        else:
            return False


    def peekNext(self):
        if ((self.current + 1) >= (len(self.source) - 1)):
            return '\0'

        return self.source[self.current + 1]


    def match(self, symbol):
        if self.source[self.current] != symbol or self.isAtEnd():
            return False

        else:
            self.current += 1
            return True


    def string(self, beg):
        start = self.current

        while ((self.peek() != beg) and not self.isAtEnd()):
            if (self.peek() == '\n'):
                self.line += 1

            self.advance()

        if (self.isAtEnd()):
            err = report(self.line, "Unterminated string")
            return err

        # seek next ' or "
        self.advance()

        value = self.source[start:self.current - 1]

        self.addToken(TokenType.STRING, value, None)


    def number(self):
        start = self.current

        while (self.isDigit(self.peek())):
            self.advance()

        # decimal part of number of any
        if ((self.peek() == '.') and (self.isDigit(self.peekNext()))):
            # chew the decimal point
            self.advance()

            # chew the rest
            while (self.isDigit(self.peek())):
                self.advance()

        elif ((self.peek() == '.') and not (self.isDigit(self.peekNext()))):
            err = report(self.line, "Expected number after '.'. Did you mean float or int?")
            return err

        value = self.source[start - 1:self.current]
        self.addToken(TokenType.NUMBER, float(value), start)

    def identifier(self):
        start = self.current
        keywords = Keywords

        while (self.isAlphaNum(self.peek())):
            self.advance()

        value = self.source[start - 1:self.current]

        print(value)
        if (value.upper() in keywords):
            keyword = keywords[value.upper()]

            print(keyword, value)
            self.addToken(keyword, value, None)

        else:

            self.addToken(TokenType.IDENTIFIER, value, None)


    def isDigit(self, c):
        return ((c >= '0') and (c <= '9'))


    def isAlpha(self, c):
        between_lower_case = c >= 'a' and c <= 'z'
        between_upper_case = c >= 'A' and c <= 'Z'
        isUnderscore = c == '_'

        return between_lower_case or between_upper_case or isUnderscore


    def isAlphaNum(self, c):
        return self.isAlpha(c) or self.isDigit(c)


    def isAtEnd(self):
        if self.current > len(self.source) - 1:
            return True
        else:
            return False

    def wouldBeAtEnd(self):
        if self.current + 1 > len(self.source) - 1:
            return True
        else:
            return False


    def addSingleToken(self, lex_type):
        start = self.current - 1
        text = lex_type.name
        self.addToken(lex_type, text, start)


    def addToken(self, lex_type, text, literal):
        literal = self.source[literal:self.current] if literal != None else None
        token = Token(lex_type, text, literal, self.line)
        self.tokens.append(token)
