from utils.tokens import Token as _Token
from utils.reporter import runtimeError as _RuntimeError

class Environment:
    def __init__(self, enclosing=None):
        self.values = {} # To store re-assignable variables
        self.statics = {} # To store all constant values
        self.enclosing = enclosing


    def decl(self, name: str, val: object):
        self.statics[name] = val

    def define(self, name: str, val: object):
        # Variables declared 'var' don't get checks because they are redifined
        # FIX: #20 check if 'name' taken in 'const' scope
        if name in self.statics.keys():
            raise _RuntimeError(name, "already declared as 'const'")

        self.values[name] = val


    def isTaken(self, name: _Token):
        if name.lexeme in self.statics.keys() or name.lexeme in self.values.keys():
            return True;

        return False


    def get(self, name: _Token):
        # Recursively check for variable in the blocks scope(s) and global scope
        if (name.lexeme in self.values):
            return self.values[name.lexeme]

        if (name.lexeme in self.statics):
            return self.statics[name.lexeme]

        if (self.enclosing is not None):
            return self.enclosing.get(name)

        raise _RuntimeError(name, f"ReferenceError: Undefined variable '{name.lexeme}'")


    def assign(self, name: _Token, val: object):
        # recursively check for variable in scope(s) before assigning
        if (name.lexeme in self.values.keys()): # or name.lexeme in self.values
            self.values[name.lexeme] = val
            return

        if (name.lexeme in self.statics.keys()):
            raise _RuntimeError(name, f"ConstReassignmentError: 'const' variables can't be re-assigned")

        elif (self.enclosing is not None):
            self.enclosing.assign(name, val)
            return

        raise _RuntimeError(name, f"ReferenceError: Undefined variable '{name.lexeme}'.")
