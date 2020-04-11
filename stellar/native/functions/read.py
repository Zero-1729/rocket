import codecs as _codecs

from native.datastructs.rocketClass import RocketCallable as _RocketCallable

from native.datatypes.rocketString import String as _String


class Input(_RocketCallable):
    def __init__(self):
        self.callee = "Input"
        self.nature = "native"
        self.kind = "<native function type>"

    def arity(self):
        return 1

    def call(self, obj: object, args: list):
        # We will permit escsaped characters on user inputs, like '\n', '\t', etc
        # wrap it in 'utf-8' to decode escapes
        encoded_input = _codecs.escape_decode(bytes(input(args[0]), "utf-8"))[0]

        # All calls to 'Input' return a rocketString
        return _String.call(self, None, [encoded_input.decode("utf-8")])

    def __repr__(self):
        return "<native fn 'Input'>"

    def __str__(self):
        return "<native fn 'Input'>"
