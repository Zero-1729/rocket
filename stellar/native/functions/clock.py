import time as _time

from native.datastructs.rocketClass import RocketCallable as _RocketCallable


class Clock(_RocketCallable):
    def __init__(self):
        self.callee = "Clock"
        self.nature = "native"
        self.kind = "<native function type>"

    def arity(self):
        return 0

    def call(self, obj: object, args: list):
        return _time.clock()

    def __repr__(self):
        return "<native fn 'Clock'>"

    def __str__(self):
        return "<native fn 'Clock'>"
