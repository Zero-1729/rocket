import time

from rocketClass import RocketCallable as _RocketCallable

class Copyright(_RocketCallable):
    def __init__(self):
        self.callee = "Copyright"
        self.nature = "native"
        self.kind = "<native function type>"

    def arity(self):
        return 0

    def call(self, obj: object, args: list):
        info = """
        Copyright (c) Abubakar NK 2018
        Copyright (c) Rocket Labs 2018
        """

        return info

    def __repr__(self):
        return "<built-in fn 'copyright'>"

    def __str__(self):
        return "<built-in fn 'copyright'>"
