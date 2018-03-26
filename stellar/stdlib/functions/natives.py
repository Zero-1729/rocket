from rocketClass import RocketCallable as _RocketCallable

class natives(_RocketCallable):
    def __init__(self):
        self.callee = "natives"
        self.nature = "native"

    def arity(self):
        return 0

    def call(self, obj: object, args: list):
        return ', '.join(list(obj.globals.values.keys()))

    def __repr__(self):
        return "<built-in fn natives>"

    def __str__(self):
        return "<built-in fn natives>"
