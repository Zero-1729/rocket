from rocketClass import RocketCallable as _RocketCallable
from rocketClass import RocketInstance as _RocketInstance
from reporter import runtimeError as _RuntimeError

class Bool(_RocketCallable):
    def __init__(self):
        self.callee = 'Bool'
        self.nature = 'native'

    def arity(self):
        return 1

    def call(self, obj, args):
        val = args[0]

        # 'None' aka 'nin' is false
        # All values (including empty objects) in Rocket are true except 'false' or 'nin'
        if (type(val) == type(None)) or (val == False):
            return RocketBool(False)

        if (hasattr(val, 'value')):
            # in case a RocketBool was passed

            # special case for '0' and '1'
            # REM: Python thinks they are false and true respectively
            # TODO: finalize whether to follow Python & JS in making '0' & '1' be special bitwise values
            # ... representing 'false' & 'true'
            if ((val.value == False) or (val.value == True)) and not ((val.value == 0) or (val.value == 1)):
                return RocketBool(val.value)

        return RocketBool(True)

    def type(self):
        return type(self)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<native type 'Bool'>"


class RocketBool(_RocketInstance):
    def __init__(self, value):
        self.value = value
        self.nature = 'Datatype'

    def get(self, name):
        raise _RuntimeError(name, f"'Bool' has no method '{name.lexeme}'.")

    def set(self, name, value):
        raise _RuntimeError(name, "Cannot mutate an Bool's props")

    def raw_string(self):
        return str(self.value)

    def __repr__(self):
        return f'\033[1m{str(self.value).lower()}\033[0m'

    def __str__(self):
        return self.__repr__()