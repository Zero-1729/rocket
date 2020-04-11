from native.datastructs.rocketClass import RocketCallable as _RocketCallable

from utils.tokens import TokenType as _TokenType


class Type(_RocketCallable):
    def __init__(self):
        self.callee = "Type"
        self.nature = "native"
        self.kind = "<native function type>"

    def arity(self):
        return 1

    def call(self, obj: object, args: list):
        # We directly check for 'None'
        nin_lexeme = obj.KSL[1][_TokenType.NIN.value]

        if args[0] == None:
            return f"<{nin_lexeme} type>"

        # For datatypes, classes, and functions
        if hasattr(args[0], 'nature'):
            return args[0].kind

        try:
            # Likely a native fn
            return args[0]().kind
        except:
            # TODO: Check all other edge cases
            return "<unknown type>"

    def __repr__(self):
        return "<native fn 'Type'>"

    def __str__(self):
        return "<native fn 'Type'>"
