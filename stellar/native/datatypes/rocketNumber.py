from utils.reporter    import runtimeError   as _RuntimeError

from native.datastructs.rocketClass import RocketCallable as _RocketCallable
from native.datastructs.rocketClass import RocketInstance as _RocketInstance

from native.datatypes  import rocketString   as _string


class Int(_RocketCallable):
    def __init__(self):
        self.callee = 'Int'
        self.nature = 'native'

    def arity(self):
        return 1

    def call(self, obj, args):
        size = int(args[0]) if not (type(args[0]) in [RocketInt, RocketFloat]) else int(args[0].value)

        return RocketInt(size)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<native type 'Int'>"


class RocketInt(_RocketInstance):
    def __init__(self, value):
        self.value = value.__trunc__()
        self.nature = 'datatype'
        self.kind = "<native type 'Int'>"

    def get(self, name):
        raise _RuntimeError(name, f"'Int' has no method '{name.lexeme}'.")

    def set(self, name, value):
        raise _RuntimeError(name, "Cannot mutate an Int's props")

    def raw_string(self):
        return str(self.value)

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
        if (isinstance(args[0], RocketFloat) or isinstance(args[0], RocketInt)):
            return RocketFloat(float(args[0].value))
            
        if (type(args[0]) == int) or (type(args[0]) == float):
            return RocketFloat(float(args[0]))

        else:
            raise _RuntimeError(obj, f"'Float' accepts either Int or Float as an argument.")

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<native type 'Float'>"


class RocketFloat(_RocketInstance):
    def __init__(self, value):
        self.value = value
        self.nature = 'datatype'
        self.kind = "<native type 'Float'>"

    def get(self, name):
        if name.lexeme == 'toFixed':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                if (args[0].value > 0):
                    return _string.String().call(self, [str(self.value)[0:args[0].value + 2]])

                else:
                    return _string.String().call(self, [str(int(self.value))])

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'toFixed' of Float>"
            rocketCallable.nature = 'native'

            return rocketCallable

        else:
            raise _RuntimeError(name, f"'Float' has no method '{name.lexeme}'.")

    def set(self, name, value):
        raise _RuntimeError(name, "Cannot mutate an Float's props")

    def raw_string(self):
        return str(self.value)

    def __repr__(self):
        return f'\033[36m{self.value}\033[0m'

    def __str__(self):
        return self.__repr__()
