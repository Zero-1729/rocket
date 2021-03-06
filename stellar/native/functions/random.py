import random as _random

from native.datastructs.rocketClass import RocketCallable as _RocketCallable


class Random(_RocketCallable):
    def __init__(self):
        self.callee = "Random"
        self.nature = "native"
        self.kind = "<native function type>"

    def arity(self):
        return 0

    def call(self, obj: object, args: list):
        return _random.random()

    def __repr__(self):
        return "<native fn 'Random'>"

    def __str__(self):
        return "<native fn 'Random'>"
