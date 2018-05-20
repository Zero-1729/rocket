import time as _time

from rocketClass import RocketCallable as _RocketCallable

class Clock(_RocketCallable):
    def __init__(self):
        self.callee = "Clock"
        self.nature = "native"

    def arity(self):
        return 0

    def call(self, obj: object, args: list):
        return _time.clock()

    def type(self):
        return self.__repr__()

    def __repr__(self):
        return "<built-in fn 'Clock'>"

    def __str__(self):
        return "<built-in fn 'Clock'>"
