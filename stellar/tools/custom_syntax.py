import sys

from tokens import Token as _Token, TokenType as _TokenType, Keywords as _Keywords


class Scanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []
        self.current = 0
        self.line = 1


    def scan(self):
        while (not self.isAtEnd()):
            c = self.advance()

            if c == "?":
                self.addSingleToken(_TokenType.Q_MARK)
                continue

            if c == "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.isAtEnd():
                        self.advance()
                continue

            if c == "\n":
                self.line += 1

            if c == " " or c == "\n" or c == "\t" or c == "\r":
                continue

            if (self.isAlpha(c)):
                self.indentifier()

            else:
                print(f"[line {self.line}]: Unregocnized symbol '{c}'")
                sys.exit(9) # yep don't run program just exit if there is error in 'config.rckt'

        self.addToken(_TokenType.EOF, "", None)
        return self.tokens


    def indentifier(self):
        start = self.current

        while (self.isAlpha(self.peek())):
            self.advance()

        value = self.source[start - 1:self.current]

        if value.upper() in _Keywords:
            keyword = _Keywords[value.upper()]
            self.addToken(keyword, value, None)

        else:
            self.addToken(_TokenType.IDENTIFIER, value, None)


    def advance(self):
        self.current += 1
        return self.previous()


    def peek(self):
        if self.isAtEnd():
            return "\0"

        return self.source[self.current]


    def previous(self):
        return self.source[self.current - 1]


    def match(self, c):
        if not self.isAtEnd():
            if not self.source[self.current] != c or self.isAtEnd():
                return False

            else:
                self.current += 1
                return True


    def isAlpha(self, c):
        between_lower_case = c >= 'a' and c <= 'z'
        between_upper_case = c >= 'A' and c <= 'Z'
        is_underscore = c == "_"

        return between_lower_case or between_upper_case or is_underscore


    def addSingleToken(self, lex_type):
        text = self.source[self.current - 1:self.current]
        self.addToken(lex_type, text, None)


    def addToken(self, lex_type, text, literal):
        token = _Token(lex_type, text, literal, self.line)
        self.tokens.append(token)


    def isAtEnd(self):
        if self.current > len(self.source) - 1:
            return True
        else:
            return False


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.customs = []
        self.defaults = []
        self.keywords = {}


    def parse(self):
        while not self.isAtEnd():
            tok = self.advance()

            if tok.lexeme in ['', '?']:
                continue

            elif tok.type in list(_Keywords.values()):
                self.defaults.append(tok)

            elif tok.type not in list(_Keywords.values()):
                self.customs.append(tok.lexeme)

        # How we parse the tokens in binary form allow for them to be of the same height
        for cust in self.customs:
            self.defaults.reverse() # Because of poping

            default_name = self.defaults.pop()
            self.keywords[cust] = default_name.type

        return self.keywords


    def advance(self):
        self.current += 1
        return self.previous()


    def previous(self):
        return self.tokens[self.current - 1]


    def isAtEnd(self):
        if self.current == len(self.tokens) - 1:
            return True

        else:
            return False
