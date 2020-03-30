from rocketClass import RocketCallable as _RocketCallable
import codecs

class Print(_RocketCallable):
    def __init__(self):
        self.callee = "Print"
        self.nature = "native"

    def arity(self):
        return 1

    def call(self, obj: object, args: list):
        # We will permit escsaped characters on user outputs, like '\n', '\t', etc
        # wrap it in 'utf-8' to decode escapes
        encoded_input = codecs.escape_decode(args[0], "utf-8")[0]
        print(encoded_input.decode("utf-8"))

    def type(self):
        return self.__repr__()

    def __repr__(self):
        return "<built-in fn 'Print'>"

    def __str__(self):
        return "<built-in fn 'Print'>"