import enum as _enum


# Fake C enum type
@_enum.unique
class TokenType(_enum.Enum):
        # Single character tokens
        LEFT_PAREN       = 1
        RIGHT_PAREN      = 2
        LEFT_BRACE       = 3
        RIGHT_BRACE      = 4
        COMMA            = 5
        DOT              = 6
        PLUS             = 7
        MINUS            = 8
        SEMICOLON        = 9
        DIV              = 10
        MULT             = 11
        MOD              = 12

        # rokcet v0.7.1
        EXP              = 13

        # NOTE: floor division is detected only if 'RIGHT' operand is a number
        FLOOR            = 14

        # One or Two character tokens
        BANG             = 15
        BANG_EQUAL       = 16
        EQUAL            = 17
        EQUAL_EQUAL      = 18
        GREATER          = 19
        GREATER_EQUAL    = 20
        LESS             = 21
        LESS_EQUAL       = 22

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
        IDENTIFIER        = 23
        STRING            = 24
        NUMBER            = 25

        # Keywords
        AND               = 26
        CLASS             = 27
        ELSE              = 28
        FALSE             = 29
        FUNC              = 30
        FOR               = 31
        IF                = 32
        NIN               = 33
        OR                = 34
        PRINT             = 35
        RETURN            = 36
        SUPER             = 37
        THIS              = 38
        TRUE              = 39
        CONST             = 40
        VAR               = 41
        WHILE             = 42

        # EOF
        EOF               = 43


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
        "CONST": TokenType.CONST,
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
