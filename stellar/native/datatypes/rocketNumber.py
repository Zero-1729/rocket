from utils.reporter    import runtimeError   as _RuntimeError

from native.datastructs.rocketClass import RocketCallable as _RocketCallable
from native.datastructs.rocketClass import RocketInstance as _RocketInstance

from native.datatypes  import rocketString   as _string

from utils.misc import isType as _isType


class Int(_RocketCallable):
    def __init__(self):
        self.callee = 'Int'
        self.nature = 'native'

    def arity(self):
        return 1

    def call(self, obj, args):
        if isNumber(args[0]):
            value = args[0]

            if (hasattr(args[0], 'value')):
                value = args[0].value

            return RocketInt(int(float(value)) if _isType(args[0], _string.RocketString) else int(value))

        raise _RuntimeError(obj, f"Type Mismatch: Cannot convert {args[0].kind} to Int.")

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
        if isNumber(args[0]):
            value = args[0]

            if hasattr(args[0], 'value'):
                value = args[0].value

            return RocketFloat(float(value))

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


def isNumber(n):
    if hasattr(n, 'value'):
        if (_isType(n, _string.RocketString)):
            return not (n.value.isalnum() and n.value.isalpha())

        return _isType(n, RocketInt) or _isType(n, RocketFloat)

    return _isType(n, int) or _isType(n, float)