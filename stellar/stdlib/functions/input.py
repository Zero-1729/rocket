from rocketClass import RocketCallable as _RocketCallable

class Input(_RocketCallable):
    def __init__(self):
        self.callee = "Input"
        self.nature = "native"

    def arity(self):
        return 1

    def call(self, obj: object, args: list):
        return input(args[0])

    def __repr__(self):
        return "<built-in fn 'Input'>"

    def __str__(self):
        return "<built-in fn 'Input'>"
