# Author: Abubakar N K (Zero-1729)
# LICENSE: RLOL
# Rocket Lang (Stellar) KSL creator (C) 2018

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
                    if self.match("/"):
                        while self.peek() != "\n" and not self.isAtEnd(): self.advance()

                    else:
                        while self.peek() != "\n" and not self.isAtEnd():
                            self.advance()
                continue

            if c == "#":
                while self.peek() != "\n" and not self.isAtEnd(): self.advance()
                continue

            if c == "\n":
                self.line += 1

            if c == " " or c == "\n" or c == "\t" or c == "\r":
                continue

            if (self.isAlpha(c)):
                self.indentifier()

            else:
                print(f"\033[91m[ScanError on line {self.line} in config]:\033[0m Unregocnized symbol '{c}'")
                sys.exit(9) # yep don't run program just exit if there is error in 'config.rckt'

        self.addToken(_TokenType.EOF, "", None)
        return self.tokens


    def indentifier(self):
        start = self.current

        while (self.isAlpha(self.peek())):
            self.advance()

        value = self.source[start - 1:self.current]

        if value in _Keywords:
            # print(f"{value} is a keyword")
            keyword = _Keywords[value]
            self.addToken(keyword, value, None)

        else:
            # print(f"{value} not a keyword")
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
        self.vw_Dict = {}


    def parse(self):
        while not self.isAtEnd():
            tok = self.advance()

            if tok.lexeme in ['', '?']:
                continue

            elif tok.type in list(_Keywords.values()):
                self.defaults.append(tok)

            elif tok.type not in list(_Keywords.values()):
                self.customs.append(tok.lexeme)

        isEqualHeight = len(self.defaults) == len(self.customs)
        if not isEqualHeight:
            print(f"\033[93m[ParseError in config]:\033[0m Number of Defaults & Customs not equal.\n\033[1m[Note]:\033[0m Number of Keywords must equal number of Customs.")
            sys.exit(1)

        # How we parse the tokens in binary form allow for them to be of the same height
        for i in range(len(self.defaults)):
            self.keywords[self.customs[i]] = self.defaults[i].type
            self.vw_Dict[self.defaults[i].type.value] = self.customs[i]

        # fill in remaining item unassignd items in KSL
        self.fillKSL()

        return self.keywords, self.vw_Dict


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


    def fillKSL(self):
        self.fillKeywords()
        self.fillPKSL()


    def fillKeywords(self):
        tmp = _Keywords
        trash = []
        for name in tmp:
            if tmp[name] in self.keywords.values():
                trash.append(name)

            else:
                self.keywords[name] = tmp[name]

        del trash


    def fillPKSL(self):
        for keyword in _Keywords.values():
            if keyword.value not in self.vw_Dict:
                self.vw_Dict[keyword.value] = keyword.name.lower()
