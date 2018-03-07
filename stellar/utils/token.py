TokenType = {
    # Single character tokens
    "LEFT_PAREN": "(",
    "RIGHT_PAREN": ")",
    "LEFT_BRACE": "{",
    "RIGHT_BRACE": "}",
    "COMMA": ",",
    "DOT": ".",
    "PLUS": "+",
    "MINUS": "-",
    "SEMICOLON": ";",
    "DIV": "/",
    "MULT": "*",
    "MOD": "%",

    # NOTE:Floor division
    # Yes floor division is detected only if left operand is a number
    "FLOOR": "//",

    # One or Two character tokens
    "BANG": "!",
    "BANG_EQUAL": "!=",
    "EQUAL": "=",
    "EQUAL_EQUAL": "==",
    "GREATER": ">",
    "GREATER_EQUAL": ">=",
    "LESS": "<",
    "LESS_EQUAL": "<=",

    # literals
    "IDENTIFIER": "",
    "STRING": "",
    "NUMBER": "",

    # Keywords
    "Keyword": ["AND",
                "CLASS",
                "ELSE",
                "FALSE",
                "FUNC",
                "FOR",
                "IF",
                "NIN",
                "OR",
                "PRINT",
                "RETURN",
                "SUPER",
                "THIS",
                "TRUE",
                "VAR",
                "WHILE"
    ],

    # EOF
    "EOF": ""
}

class Token:
    def __init__(self, lex_type, text, literal, line):
        self.lex_type = lex_type
        self.text = text
        self.literal = literal
        self.line = line

    def toString(self):
        return f"[{self.line}] <'{self.lex_type}', '{self.text}', '{self.literal}'>"
