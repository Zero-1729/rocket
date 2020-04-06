# Author: Abubakar Nur Kahlil (Zero-1729)
# LICENSE: RLOL
# Rocket Lang (Stellar) Scanner (C) 2018

import re as _re

from utils.reporter import ScanError    as _ScanError

from utils.tokens import Token          as _Token
from utils.tokens import TokenType      as _TokenType


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
                tok_type = _TokenType.LEFT_PAREN
                self.addSingleToken(tok_type)

            elif c == ")":
                tok_type = _TokenType.RIGHT_PAREN
                self.addSingleToken(tok_type)

            elif c == "{":
                tok_type = _TokenType.LEFT_BRACE
                self.addSingleToken(tok_type)

            elif c == "}":
                tok_type = _TokenType.RIGHT_BRACE
                self.addSingleToken(tok_type)

            elif c == ";":
                tok_type = _TokenType.SEMICOLON
                self.addSingleToken(tok_type)

            elif c == ",":
                tok_type = _TokenType.COMMA
                self.addSingleToken(tok_type)

            elif c == "?":
                tok_type = _TokenType.Q_MARK
                self.addSingleToken(tok_type)

            elif c == ':':
                tok_type = _TokenType.COLON
                self.addSingleToken(tok_type)

            elif c == ".":
                tok_type = _TokenType.DOT
                self.addSingleToken(tok_type)

            elif c == "+":
                if self.match("="):
                    self.addDoubleToken(_TokenType.PLUS_INC)

                else:
                    tok_type = _TokenType.PLUS
                    self.addSingleToken(tok_type)

            elif c == "-":
                if self.match("="):
                    self.addDoubleToken(_TokenType.MINUS_INC)

                else:
                    tok_type = _TokenType.MINUS
                    self.addSingleToken(tok_type)

            elif c == "~":
                tok_type = _TokenType.TILDE
                self.addSingleToken(tok_type)

            elif c == "*":
                if self.match("*"):
                    if self.peek() == '=':
                        self.addTripleToken(_TokenType.EXP_INC)
                        self.advance()

                    else: self.addDoubleToken(_TokenType.EXP)

                else:
                    if self.match("="):
                        self.addDoubleToken(_TokenType.MULT_INC)

                    else:
                        tok_type = _TokenType.MULT
                        self.addSingleToken(tok_type)

            elif c == "%":
                if self.match("="):
                    self.addDoubleToken(_TokenType.MOD_INC)

                else:
                    tok_type = _TokenType.MOD
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
                    if self.peek() == '=':
                        self.addTripleToken(_TokenType.FLOOR_INC)
                        self.advance()

                    elif (self.futureNumberPeek()):
                        self.addDoubleToken(_TokenType.FLOOR) # "FLOOR"
                        # AddSingleToken can't do the job so we might aswell

                    elif (self.peek() == '/'):
                        while ((self.peek() != "\n") and not (self.isAtEnd())):
                            self.advance()

                elif self.match("="):
                    self.addDoubleToken(_TokenType.DIV_INC)

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

                elif self.match("="):
                    self.addDoubleToken(_TokenType.DIV_INC)

                else:
                    self.addSingleToken(_TokenType.DIV) # DIV


            # Comparison tokens
            elif c == "!":
                if not self.match("="):
                     self.addSingleToken(_TokenType.BANG) # "BANG"

                else:
                    self.addDoubleToken(_TokenType.BANG_EQUAL) # "BANG_EQUAL"

            elif c == "=":
                if self.match('='):
                    self.addDoubleToken(_TokenType.EQUAL_EQUAL) # "EQUAL_EQUAL"

                else:
                    if self.match(">"):
                        self.addDoubleToken(_TokenType.ARROW)

                    else:
                        self.addSingleToken( _TokenType.EQUAL) # "EQUAL"



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


    def fromBase(self, val: str, base=16):
        alphas = {
                'A': 10,
                'B': 11,
                'C': 12,
                'D': 13,
                'E': 14,
                'F': 15
        }

        val = val [2:]
        enig = len(val)
        total = 0

        for i in range(enig):
            if val[i].isalpha():
                total += alphas[val[i].upper()] * (base ** (enig - 1))

            else:
                total += int(val[i]) * (base ** (enig - 1))

            enig -= 1

        return total


    def number(self):
        start = self.current
        value = float()
        is_seperated = False

        # Lets scan and transform 'HEX' into an int
        if self.peek().lower() == 'x' or self.peek().lower() == 'o' or self.peek().lower() == 'b':
            # We continue along and transform it later
            self.advance()

        while (self.isDigit(self.peek())):
            self.advance()

        while (self.isDigit(self.peek()) or self.peek() == '_'):
            is_seperated = True
            self.advance()

        # decimal part of number of any
        if ((self.peek() == '.') and (self.isDigit(self.peekNext()))):
            # chew the decimal point
            self.advance()

            # chew the rest
            while (self.isDigit(self.peek()) or self.peek() == '_'):
                self.advance()

            # When we are done chewing through the float we grab its value from the source
            value_str = self.source[start - 1:self.current]
            if '_' in value_str:
                value = float(''.join(value_str.split('_')))
            else: value = float(value_str)

        elif ((self.peek() == '.') and not (self.isDigit(self.peekNext()))):
            err = _ScanError(self.line, "Expected number after '.'. Did you mean float or int?").report()
            self.errors.append(err)
            return

        else:
            # Keep track of whether we have reached the end of the digit we are parsing
            # Inorder to aviod 'IndexError'
            atDigitEnd = True if len(self.source) == start else False

            # if no point found, we know we have an 'int'
            if not atDigitEnd and self.source[start].lower() == 'x':
                value = self.fromBase(self.source[start-1:self.current])

            elif not atDigitEnd and self.source[start].lower() == 'o':
                value = self.fromBase(self.source[start-1:self.current], 8)

            elif not atDigitEnd and self.source[start].lower() == 'b':
                # Our best would be to use regex
                match = re.compile('[0-1]*')
                isFull = match.fullmatch(self.source[start+1:self.current])

                if isFull:
                    value = self.fromBase(self.source[start-1:self.current], 2)
                else:
                    err = _ScanError(self.line, "Expected number to be complete base '2' number")
                    self.errors.append(err)

            elif is_seperated:
                value = int(''.join(self.source[start-1:self.current].split('_')))

            else:
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


    def addTripleToken(self, lex_type):
        text = self.source[self.current - 2:self.current + 1]
        self.addToken(lex_type, text, None)


    def addToken(self, lex_type, text, literal):
        token = _Token(lex_type, text, literal, self.line)
        self.tokens.append(token)
