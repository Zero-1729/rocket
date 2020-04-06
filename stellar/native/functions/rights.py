from native.datatypes.rocketClass import RocketCallable as _RocketCallable


class Copyright(_RocketCallable):
    def __init__(self):
        self.callee = "Copyright"
        self.nature = "native"
        self.kind = "<native function type>"

    def arity(self):
        return 0

    def call(self, obj: object, args: list):
        info = """
        Copyright (c) Abubakar Nur Khalil 2018 - present
        """

        return info

    def __repr__(self):
        return "<native fn 'copyright'>"

    def __str__(self):
        return "<native fn 'copyright'>"
