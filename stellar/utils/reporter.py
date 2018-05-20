from tokens import TokenType as _TokenType, Token as _Token


class ScanError(Exception):
    def __init__(self, line: int, message: str):
        self.line = line
        self.message = message

    def report(self):
        return f"\033[93m[ScanError on line {self.line}]\033[0m {self.message}"

    def __str__(self):
        return self.report()

    def __repr__(self):
        return self.__str__()


class ParseError(Exception):
    def __init__(self, token: _Token, message: str):
        self.token = token
        self.message = message

    def report(self):
        if self.token.type.value == _TokenType.EOF.value:
            return f"\033[91m[ParseError on line {self.token.line}]\033[0m \033[89mError at end: {self.message}\033[0m"

        else:
            place = self.token.lexeme
            return f"\033[91m[ParseError on line {self.token.line}]\033[0m \033[89mError at '{place}':  {self.message}\033[0m"

    def __str__(self):
        return self.report()

    def __repr__(self):
        return self.__str__()


class runtimeError(RuntimeError):
    def __init__(self, token: _Token, msg: str):
        self.token = token
        self.msg = msg

    def returnable(self):
        return False

    def __str__(self):
        return f"\033[93m[RuntimeError]\033[0m '{self.msg}'"

    def __repr__(self):
        return self.__str__()


class BreakException(Exception):
    def returnable(self):
        return False


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

    def returnable(self):
        return True


class ResolutionError(RuntimeError):
    def __init__(self, token: _TokenType, message: str):
        self.token = token
        self.message = message

    def report(self):
        return f"\033[93m[ResolutionError on line {self.token.line}]\033[0m: {self.message}"

    def returnable(self):
        return False

    def __str__(self):
        return self.report()

    def __repr__(self):
        return self.__str__()
