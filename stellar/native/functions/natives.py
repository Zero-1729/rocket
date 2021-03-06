from native.datastructs.rocketClass import RocketCallable as _RocketCallable


class Natives(_RocketCallable):
    def __init__(self):
        self.callee = "Natives"
        self.nature = "native"
        self.kind = "<native function type>"

    def arity(self):
        return 0

    def call(self, obj: object, args: list):
        return ', '.join(list(obj.globals.values.keys()))

    def __repr__(self):
        return "<native fn 'Natives'>"

    def __str__(self):
        return "<native fn 'Natives'>"
