from utils.tokens import Token as _Token
from utils.reporter import runtimeError as _RuntimeError

class Environment:
    def __init__(self, enclosing=None):
        self.values = {}
        self.enclosing = enclosing


    def define(self, name: str, val: object):
        # TODO: Add checks for variables declared with 'const'
        # Variables declared 'var' don't get checks because they are redifined
        self.values[name] = val


    def get(self, name: _Token):
        # Recursively check for variable in the blocks scope(s) and global scope
        if (name.lexeme in self.values):
            return self.values[name.lexeme]

        if (self.enclosing is not None):
            return self.enclosing.get(name)

        raise _RuntimeError(name, f"ReferenceError: Undefined variable '{name.lexeme}'")


    def assign(self, name: _Token, val: object):
        # recursively check for variable in scope(s) before assigning
        if (name.lexeme in self.values.keys()): # or name.lexeme in self.values
            self.values[name.lexeme] = val
            return

        elif (self.enclosing is not None):
            self.enclosing.assign(name, val)
            return

        raise _RuntimeError(name, f"ReferenceError: Undefined variable '{name.lexeme}'.")
