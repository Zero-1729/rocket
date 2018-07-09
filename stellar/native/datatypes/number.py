from rocketClass import RocketCallable as _RocketCallable
from rocketClass import RocketInstance as _RocketInstance
from reporter import runtimeError as _RuntimeError

class Int(_RocketCallable):
    def __init__(self):
        self.callee = 'Int'
        self.nature = 'native'

    def arity(self):
        return 1

    def call(self, obj, args):
        size = int(args[0])

        return RocketInt(size)

    def type(self):
        return self.__repr__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<native type 'Int'>"


class RocketInt(_RocketInstance):
    def __init__(self, value):
        self.value = value.__trunc__()
        self.nature = 'Datatype'

    def get(self, name):
        raise _RuntimeError(name, f"'Int' has no '{name.lexeme}' method.")

    def set(self, name, value):
        raise _RuntimeError(name, "Cannot mutate an Int's props")


    def __repr__(self):
        return f'\033[36m{self.value}\033[0m'

    def __str__(self):
        return self.__repr__()


class Float(_RocketCallable):
    def __init__(self):
        self.callee = 'Float'
        self.nature = 'native'

    def arity(self):
        return 1

    def call(self, obj, args):
        size = args[0]

        return RocketFloat(size)

    def type(self):
        return self.__repr__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<native type 'Float'>"


class RocketFloat(_RocketInstance):
    def __init__(self, value):
        self.value = value
        self.nature = 'Datatype'

    def get(self, name):
        if name.lexeme == 'toFixed':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                return self.value.__trunc__()

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'toFixed' of Float>"
            rocketCallable.nature = 'native'

            return rocketCallable

        else:
            raise _RuntimeError(name, f"'Float' has no '{name.lexeme}' method.")

    def set(self, name, value):
        raise _RuntimeError(name, "Cannot mutate an Float's props")


    def __repr__(self):
        return f'\033[36m{self.value}\033[0m'

    def __str__(self):
        return self.__repr__()
