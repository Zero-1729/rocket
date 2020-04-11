from utils.tokens import Token     as _Token
from utils.tokens import TokenType as _TokenType

from   utils.reporter    import runtimeError   as _RuntimeError

from   native.datastructs.rocketClass import RocketCallable as _RocketCallable
from   native.datastructs.rocketClass import RocketInstance as _RocketInstance

import native.datastructs.rocketList   as _list

import native.datatypes.rocketBoolean  as _boolean
import native.datatypes.rocketNumber   as _number


class String(_RocketCallable):
    def __init__(self):
        self.callee = 'String'
        self.nature = 'native'

    def arity(self):
        return 1

    def call(self, obj, args):
        # Remember we are storing the actual literal values
        # so we need to turn them to strings
        # but that is for the Rocket datatypes
        if (hasattr(args[0], 'nature')):
            if (args[0].nature == 'datatype'):
                    return RocketString(str(args[0].value))

        # however, for classes, fns, etc. '___str__' is enough
        return RocketString(args[0].__str__())

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<native type 'String'>"


class RocketString(_RocketInstance):
    def __init__(self, value):
        self.value = value
        self.nature = 'datatype'
        self.kind = "<native type 'String'>"

    def get(self, name):
        # Note: 'edna' is what we use to manipulate arity for 'slice' function from '1' to '2'
        if name.lexeme == 'get':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                index = args[0].value

                if index >= len(self.value):
                    raise _RuntimeError('String', "IndexError: string index out of range")

                return String().call(self, [self.value[index]])

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'get' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'slice':
            rocketCallable = _RocketCallable(self)

            def arity(inc=False):
                if inc:
                    return 2

                return 1

            def call(interpreter, args, inc=False):
                if inc:
                    if (args[0].value >= len(self.value)) or (args[1].value >= len(self.value)):
                        raise _RuntimeError('String', "IndexError: string index out of range")

                    # Special case
                    if (args[0].value >= args[1].value):
                        String().call(self, [''])

                    else:
                        return String().call(self, [self.value[args[0].value:args[1].value]])

                return self.value[args[0].value:]

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.nature = 'native'
            rocketCallable.signature = 'String'
            rocketCallable.toString = "<native method 'slice' of String>"
            rocketCallable.slice = True
            rocketCallable.inc = False

            return rocketCallable

        if name.lexeme == 'length':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    return _number.Int().call(self, [len(self.value)])
                else:
                    return 0

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'length' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'reverse':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    return String().call(self, [self.value[::-1]])

                else:
                    return String().call(self, [self.value['']])

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'reverse' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'capitalize':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    if len(self.value) >= 2:
                        return String().call(self, [self.value[0].upper() + self.value[1:]])

                    else:
                        return String().call(self, [self.value])
                else:
                    raise _RuntimeError('String', "IndexError: cannot index from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'capitalize' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'upper':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    return String().call(self, [self.value.upper()])

                else:
                    raise _RuntimeError('String', "IndexError: cannot index from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'upper' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'lower':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    return String().call(self, [self.value.lower()])

                else:
                    raise _RuntimeError('String', "IndexError: cannot index from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'lower' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'isupper':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    return _boolean.Bool().call(self, [self.value.isupper()])

                else:
                    raise _RuntimeError('String', "IndexError: cannot index from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'isupper' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'islower':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    return _boolean.Bool().call(self, [self.value.islower()])

                else:
                    raise _RuntimeError('String', "IndexError: cannot index from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'islower' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'isalpha':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    return _boolean.Bool().call(self, [self.value.isalpha()])

                else:
                    raise _RuntimeError('String', "IndexError: cannot index from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'isalpha' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'isnum':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    return _boolean.Bool().call(self, [self.value.isdecimal()])

                else:
                    raise _RuntimeError('String', "IndexError: cannot index from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'isnum' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'center':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                if self.notEmpty():
                    return String().call(self, [self.value.center(args[0].value)])

                else:
                    raise _RuntimeError('String', "IndexError: cannot index from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'center' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'concat':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                if isinstance(args[0], RocketString):
                    # We do not internally edit it, instead its returned
                    # self.value = self.value + new_list.elements
                    text = args[0].value

                    return String().call(self, [self.value + text])

                else:
                    raise _RuntimeError('String', "IndexError: can only concatenate 'String' native type with another 'String'.")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'concat' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'indexOf':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                if self.notEmpty():
                    if args[0].value in self.value:
                        return String().call(self, [self.value.index(args[0].value)])
                        
                    else:
                        raise _RuntimeError('String', "IndexError: Item not in string")
                else:
                    raise _RuntimeError('String', "IndexError: cannot index from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'indexOf' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'includes':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                if self.notEmpty():
                    if args[0].value in self.value:
                        return _boolean.Bool().call(self, [True])
                    else:
                        return _boolean.Bool().call(self, [False])
                else:
                    raise _RuntimeError('String', "IndexError: cannot index from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'includes' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'endsWith':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                if self.notEmpty():
                    endlen = len(args[0].value)
                    index = -(endlen)
                    if args[0] == self.value[index:]:
                        return _boolean.Bool().call(self, [True])
                    else:
                        return _boolean.Bool().call(self, [False])
                else:
                    raise _RuntimeError('String', "IndexError: cannot index from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'endsWith' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'split':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                if self.notEmpty():
                    if args[0].value in self.value:
                        # split it Python style
                        splitted_list = self.value.split(args[0].value)

                        # Create a Rocket List
                        arr = _list.List().call(self, [])

                        # Create fake token for getter
                        append_tok = _Token(_TokenType.STRING, 'append', 'append', 0)

                        # Add chunks to Rocket List
                        for i in range(len(splitted_list)):
                            arr.get(append_tok).call(self, [splitted_list[i]])

                        # return new rocket List with chunks
                        return arr

                    else:
                        return _list.List().call(self, [self.value])
                else:
                    raise _RuntimeError('String', "IndexError: cannot index from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'split' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        else:
            raise _RuntimeError(name, f"'String' has no method '{name.lexeme}'.")


    def set(self, name, value):
        raise _RuntimeError(name, "Cannot mutate an String's props")


    def notEmpty(self):
        if len(self.value) == 0:
            return False

        return True

    def raw_string(self):
        return self.value

    def __repr__(self):
        return f'\033[32m{self.value}\033[0m'

    def __str__(self):
        return self.__repr__()
