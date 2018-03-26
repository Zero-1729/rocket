import time

from rocketClass import RocketCallable as _RocketCallable

class clock(_RocketCallable):
    def __init__(self):
        self.callee = "clock"
        self.nature = "native"

    def arity(self):
        return 0

    def call(self, obj: object, args: list):
        return time.clock()

    def __repr__(self):
        return "<built-in fn clock>"

    def __str__(self):
        return "<built-in fn clock>"
