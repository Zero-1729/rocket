from tokens import TokenType as _TokenType, Token as _Token


class ScanError(Exception):
    def __init__(self, line: int, message: str):
        self.line = line
        self.message = message

    def report(self):
        return f"[line {self.line}] Error: {self.message}"


class ParseError(Exception):
    def __init__(self, token: _Token, message: str):
        self.token = token
        self.message = message

    def report(self):
        if self.token.type == _TokenType.EOF:
            return f"[line {self.toke.line}]: Error at end: {self.message}"

        else:
            place = self.token.lexeme
            return f"[line {self.token.line}]: Error at '{place}':  {self.message}"


class runtimeError(RuntimeError):
    def __init__(self, token: _Token, message: str):
        self.token = token
        self.message = message


class BreakException(Exception):
    pass


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class ResolutionError(Exception):
    def __init__(self, token: _TokenType, message: str):
        self.token = token
        self.message = message

    def report(self):
        if self.token.type == _TokenType.EOF:
            return f"[line {self.toke.line}]: Error at end: {self.message}"

        else:
            place = self.token.lexeme
            return f"[line {self.token.line}]: Error at '{place}':  {self.message}"
