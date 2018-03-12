import enum as __enum


# Fake C enum type
@__enum.unique
class TokenType(__enum.Enum):
        # Single character tokens
        LEFT_PAREN       = 1,
        RIGHT_PAREN      = 2,
        LEFT_BRACE       = 3,
        RIGHT_BRACE      = 4,
        COMMA            = 5,
        DOT              = 6,
        PLUS             = 7,
        MINUS            = 8,
        SEMICOLON        = 9,
        DIV              = 10,
        MULT             = 11,
        MOD              = 12,

        # rokcet v0.7.1
        #"EXP": "**",

        # NOTE: floor division is detected only if 'RIGHT' operand is a number
        FLOOR             = 13,

        # One or Two character tokens
        BANG              = 14,
        BANG_EQUAL        = 15,
        EQUAL             = 16,
        EQUAL_EQUAL       = 17,
        GREATER           = 18,
        GREATER_EQUAL     = 19,
        LESS              = 20,
        LESS_EQUAL        = 21,

        # Arithmetic increment oprands
        # rocket v0.7.1
        # "PLUS_INC": "+=",
        #"MINUS_INC": "-=",
        #"MULT_INC": "*=",
        #"DIV_INC": "/=",
        #"MOD_INC": "%=",
        #"FLOOR_INC": "//=",
        #"EXP_INC": "**=",


        # literals
        IDENTIFIER        = 22,
        STRING            = 23,
        NUMBER            = 24,

        # Keywords
        AND               = 25,
        CLASS             = 26,
        ELSE              = 27,
        FALSE             = 28,
        FUNC              = 29,
        FOR               = 30,
        IF                = 31,
        NIN               = 32,
        OR                = 33,
        PRINT             = 34,
        RETURN            = 35,
        SUPER             = 36,
        THIS              = 37,
        TRUE              = 38,
        VAR               = 39,
        WHILE             = 40,

        # EOF
        EOF               = 41


Keywords = {
        "CLASS": TokenType.CLASS,
        "ELSE": TokenType.ELSE,
        "FALSE": TokenType.FALSE,
        "FUNC": TokenType.FUNC,
        "FOR": TokenType.FOR,
        "IF": TokenType.IF,
        "NIN": TokenType.NIN,
        "OR": TokenType.OR,
        "PRINT": TokenType.PRINT,
        "RETURN": TokenType.RETURN,
        "SUPER": TokenType.SUPER,
        "THIS": TokenType.THIS,
        "TRUE": TokenType.TRUE,
        "VAR": TokenType.VAR,
        "WHILE": TokenType.WHILE

        # Rocket 
        # Like Python's Try Except
        # LAUNCH 
        # ABORT
}


class Token:
    def __init__(self, type: TokenType, lexeme: str, literal, line: int):
        self.lexeme = lexeme
        self.type = type
        self.literal = literal
        self.line = line

    def toString(self):
        return f"[{self.line}] <'{self.type}', '{self.lexeme}', '{self.literal}'>"

    def __str__(self):
        return f"{self.type} {self.lexeme} {self.literal}"

    def __repr__(self):
        args = f"{self.type}, {self.lexeme}, {self.literal}, {self.line}"
        return f"{self.__class__.__name__}({args})"
