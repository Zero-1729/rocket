# Author: Abubakar NK (Zero-1729)
# LICENSE: RLOL
# Rocket Lang (Stellar) Scanner (C) 2018

from utils.reporter import ScanError as _ScanError
from utils.tokens import Token as _Token, TokenType as _TokenType, Keywords as _Keywords

class Scanner:
    def __init__(self, source, wk_Dict):
        self.wk_Dict = wk_Dict
        self.source = source
        self.tokens = []
        self.current = 0
        self.line = 1
        self.errors = []

    def scan(self):
        while not (self.isAtEnd()):
            c = self.advance()

            # Check for lexemes
            # Starting with single character tokens
            if c == "(":
                tok_type = _TokenType.LEFT_PAREN # "LEFT_PAREN"
                self.addSingleToken(tok_type)

            elif c == ")":
                tok_type = _TokenType.RIGHT_PAREN # "RIGHT_PAREN"
                self.addSingleToken(tok_type)

            elif c == "{":
                tok_type = _TokenType.LEFT_BRACE # "LEFT_BRACE"
                self.addSingleToken(tok_type)

            elif c == "}":
                tok_type = _TokenType.RIGHT_BRACE # "RIGHT_BRACE"
                self.addSingleToken(tok_type)

            elif c == ";":
                tok_type = _TokenType.SEMICOLON # "SEMICOLON"
                self.addSingleToken(tok_type)

            elif c == ",":
                tok_type = _TokenType.COMMA # "COMMA"
                self.addSingleToken(tok_type)

            elif c == ".":
                tok_type = _TokenType.DOT # "DOT"
                self.addSingleToken(tok_type)

            elif c == "+":
                tok_type = _TokenType.PLUS # "PLUS"
                self.addSingleToken(tok_type)

            elif c == "-":
                tok_type = _TokenType.MINUS # "MINUS"
                self.addSingleToken(tok_type)

            elif c == "~":
                tok_type = _TokenType.TILDE # "TILDE" ~
                self.addSingleToken(tok_type)

            elif c == "*":
                if self.match("*"):
                    self.addDoubleToken(_TokenType.EXP)

                else:
                    tok_type = _TokenType.MULT # "MULT"
                    self.addSingleToken(tok_type)

            elif c == "%":
                tok_type = _TokenType.MOD # "MOD"
                self.addSingleToken(tok_type)

            # Yes, we use Pytjon styled single comments
            elif c == "#":
                while ((self.peek() != "\n") and not (self.isAtEnd())):
                    self.advance()

            # Double character tokens
            # check for div and comment
            # NOTE: single line comment can also begin with "///"
            elif c == "/":
                if self.match("/"):
                    if (self.futureNumberPeek()):
                        self.addDoubleToken(_TokenType.FLOOR) # "FLOOR"
                        # AddSingleToken can't do the job so we might aswell

                    if (self.peek() == '/'):
                        while ((self.peek() != "\n") and not (self.isAtEnd())):
                            self.advance()

                # C styled '/**/' multi-line comment
                elif self.match("*"):
                    while ((self.doublePeek() != "*/")):
                        if not self.isAtEnd():
                            self.advance()

                        else:
                            err = _ScanError(self.line, "Unterminated comment: couldn't find matching '*/' for '/*'").report()
                            self.errors.append(err)
                            break

                    # Continue ignoring comments
                    if self.doublePeek() == "*/":
                        # Adnavce twice to ignore '*/'
                        self.advance()
                        self.advance()

                else:
                    self.addSingleToken(_TokenType.DIV) # DIV


            # Comparison tokens
            elif c == "!":
                if not self.match("="):
                     self.addSingleToken(_TokenType.BANG) # "BANG"

                else:
                    self.addDoubleToken(_TokenType.BANG_EQUAL) # "BANG_EQUAL"

            elif c == "=":
                if not self.match("="):
                    self.addSingleToken( _TokenType.EQUAL) # "EQUAL"

                else:
                    self.addDoubleToken(_TokenType.EQUAL_EQUAL) # "EQUAL_EQUAL"

            elif c == "<":
                if self.match("="):
                    self.addDoubleToken(_TokenType.LESS_EQUAL) # "LESS_EQUAL"

                elif self.match("<"):
                    self.addDoubleToken(_TokenType.LESS_LESS) # "LESS_LESS" "<<" left bitshift

                else:
                    self.addSingleToken(_TokenType.LESS) # "LESS"

            elif c == ">":
                if self.match("="):
                    self.addDoubleToken(_TokenType.GREATER_EQUAL) # "GREATER_EQUAL"

                elif self.match(">"):
                    self.addDoubleToken(_TokenType.GREATER_GREATER) # "GREATER_GREATER" ">>" right bitshift

                else:
                    self.addSingleToken(_TokenType.GREATER) # "GREATER"

            # literals
            elif c == "":
                self.addSingleToken(_TokenType.IDENTIFIER) # "IDENTIFIER"

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
                    err = _ScanError(self.line, f"Unrecognized symbol '{c}'").report()
                    self.errors.append(err)

        self.addToken(_TokenType.EOF, '', None)
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
        short_future_character = self.source[self.source.index(doublePeeked)]

        if (self.isDigit(future_character) or self.isDigit(short_future_character)):
            return True

        else:
            return False


    def peekNext(self):
        if ((self.current + 1) >= (len(self.source) - 1)):
            return '\0'

        return self.source[self.current + 1]


    def match(self, symbol):
        if not self.isAtEnd():
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
            err = _ScanError(self.line, "Unterminated string").report()
            self.errors.append(err)
            return

        # seek next ' or "
        self.advance()

        value = self.source[start:self.current - 1]
        text = self.source[start:self.current - 1]

        self.addToken(_TokenType.STRING, text, value)


    def number(self):
        start = self.current
        value = float()

        while (self.isDigit(self.peek())):
            self.advance()

        # decimal part of number of any
        if ((self.peek() == '.') and (self.isDigit(self.peekNext()))):
            # chew the decimal point
            self.advance()

            # chew the rest
            while (self.isDigit(self.peek())):
                self.advance()

            # When we are done chewing through the float we grab its value from the source
            value = float(self.source[start - 1:self.current])

        elif ((self.peek() == '.') and not (self.isDigit(self.peekNext()))):
            err = _ScanError(self.line, "Expected number after '.'. Did you mean float or int?").report()
            self.errors.append(err)
            return

        else:
            # if not point found we know we have an 'int'
            value = int(self.source[start - 1:self.current])

        text = self.source[start - 1:self.current]

        self.addToken(_TokenType.NUMBER, text, value)

    def identifier(self):
        start = self.current
        wk_Dict = self.wk_Dict

        while (self.isAlphaNum(self.peek())):
            self.advance()

        value = self.source[start - 1:self.current]

        if value in wk_Dict:
            keyword = wk_Dict[value]
            self.addToken(keyword, value, None)

        else:
            self.addToken(_TokenType.IDENTIFIER, value, None)


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
        text = self.source[self.current-1:self.current]
        self.addToken(lex_type, text, None)


    def addDoubleToken(self, lex_type):
        text = self.source[self.current - 2:self.current]
        self.addToken(lex_type, text, None)


    def addToken(self, lex_type, text, literal):
        token = _Token(lex_type, text, literal, self.line)
        self.tokens.append(token)
