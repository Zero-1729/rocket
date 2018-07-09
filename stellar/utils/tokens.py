import enum as _enum


# Fake C enum type
@_enum.unique
class TokenType(_enum.Enum):
        # Single character tokens
        LEFT_PAREN       = 1  # '('
        RIGHT_PAREN      = 2  # ')'
        LEFT_BRACE       = 3  # '{'
        RIGHT_BRACE      = 4  # '}'
        DOT              = 5  # '.'
        COMMA            = 6  # ','
        PLUS             = 7  # '+'
        MINUS            = 8  # '-'
        SEMICOLON        = 9  # ';'
        DIV              = 10 # '/'
        MULT             = 11 # '*'
        MOD              = 12 # '%'
        EXP              = 13 # '**'

        # NOTE: floor division is detected only if 'RIGHT' operand is a number
        FLOOR            = 14 # '//'

        # One or Two character tokens
        BANG             = 15 # '!'
        BANG_EQUAL       = 16 # '!='
        EQUAL            = 17 # '='
        EQUAL_EQUAL      = 18 # '=='
        GREATER          = 19 # '>'
        GREATER_EQUAL    = 20 # '>='
        LESS             = 21 # '<'
        LESS_EQUAL       = 22 # '<='

        # Bitshifter operators
        LESS_LESS        = 200 # '<<'
        GREATER_GREATER  = 201 # '>>'

        # Arithmetic increment oprands
        # rocket v0.7.1
        PLUS_INC         = 1111, # '+='
        MINUS_INC        = 1112, # '-='
        MULT_INC         = 1113, # '*='
        DIV_INC          = 1114, # '/='
        MOD_INC          = 1115, # '%='
        FLOOR_INC        = 1116, # '//='
        EXP_INC          = 1117, # '**='

        # Unary prefix
        TILDE             = 112  # '~'

        # For arrow functions
        ARROW             = 9999 # '=>'

        # literals
        IDENTIFIER        = 23
        STRING            = 24
        NUMBER            = 25

        # Keywords
        AND               = 26   # 'and'
        CLASS             = 27   # 'class'
        ELSE              = 28   # 'else'
        #ELIF              = 29
        FALSE             = 30   # 'false'
        FUNC              = 31   # 'func'
        FOR               = 32   # 'for'
        BREAK             = 99   # 'break'
        IF                = 33   # 'if'
        NIN               = 34   # 'nin'
        OR                = 35   # 'or'
        PRINT             = 36   # 'print'
        RETURN            = 37   # 'return'
        SUPER             = 38   # 'super'
        THIS              = 39   # 'this'
        TRUE              = 40   # 'true'
        CONST             = 41   # 'const'
        VAR               = 42   # 'var'
        WHILE             = 43   # 'while'

        Q_MARK            = 66   # '?'

        DEL               = 0    # 'del'

        # EOF
        EOF               = 44


Keywords = {
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "func": TokenType.FUNC,
        "for": TokenType.FOR,
        "break": TokenType.BREAK,
        "if": TokenType.IF,
        "nin": TokenType.NIN,
        "and": TokenType.AND,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "const": TokenType.CONST,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
        "del": TokenType.DEL,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE

        # Rocket v0.2.0+
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
