# Author: Abubakar NK (Zero-1729)
# License: GNU GPL V2

from utils.reporter import report
from utils.token import Token, TokenType

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
                obj = "LEFT_PAREN"
                self.addSingleToken(obj)

            elif c == ")":
                obj = "RIGHT_PAREN"
                self.addSingleToken(obj)

            elif c == "{":
                obj = "LEFT_BRACE"
                self.addSingleToken(obj)

            elif c == "}":
                obj = "RIGHT_BRACE"
                self.addSingleToken(obj)

            elif c == ";":
                obj = "SEMICOLON"
                self.addSingleToken(obj)

            elif c == ",":
                obj = "COMMA"
                self.addSingleToken(obj)

            elif c == ".":
                obj = "DOT"
                self.addSingleToken(obj)

            elif c == "+":
                obj = "PLUS"
                self.addSingleToken(obj)

            elif c == "-":
                obj = "MINUS"
                self.addSingleToken(obj)

            elif c == "*":
                obj = "MULT"
                self.addSingleToken(obj)

            elif c == "%":
                obj = "MOD"
                self.addSingleToken(obj)

            # Double character tokens
            # check for div and comment
            # NOTE: single line comment begin with "//"
            # Floor division '//' would be in 'Math' stdlib
            elif c == "/":
                if self.match("/"):

                    if (self.futureNumberPeek()):
                        obj = "FLOOR"
                        self.addSingleToken(obj)

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
                    obj = "BANG"

                else:
                    obj = "BANG_EQUAL"
                self.addSingleToken(obj)

            elif c == "=":
                if not self.match("="):
                    obj = "EQUAL"

                else:
                    obj = "EQUAL_EQUAL"
                self.addSingleToken(obj)

            elif c == "<":
                if not self.match("="):
                    obj = "LESS"

                else:
                    obj = "LESS_EQUAL"
                self.addSingleToken(obj)

            elif c == ">":
                if not self.match("="):
                    obj = "GREATER"

                else:
                    obj = "GREATER_EQUAL"

                self.addSingleToken(obj)

            # literals
            elif c == "":
                obj = "IDENTIFIER"
                self.addSingleToken(obj)

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

        self.addToken("EOF", '')
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

        self.addToken("STRING", value)


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
        self.addToken("NUMBER", float(value))

    def identifier(self):
        start = self.current
        keywords = TokenType['Keyword']

        while (self.isAlphaNum(self.peek())):
            self.advance()

        value = self.source[start - 1:self.current]

        if (value.upper() in keywords):
            index = keywords.index(value.upper())
            keyword = keywords[index]

            self.addToken('KEYWORD', keyword.lower())

        else:
            self.addToken("IDENTIFIER", value)


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
        text = TokenType[lex_type]
        self.addToken(lex_type, text)


    def addToken(self, lex_type, text):
        literal = None
        token = Token(lex_type, text, literal, self.line)
        self.tokens.append(token)
