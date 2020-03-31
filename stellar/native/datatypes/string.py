from rocketClass import RocketCallable as _RocketCallable
from rocketClass import RocketInstance as _RocketInstance
from reporter import runtimeError as _RuntimeError
import array as _array


class String(_RocketCallable):
    def __init__(self):
        self.callee = 'String'
        self.nature = 'native'

    def arity(self):
        return 1

    def call(self, obj, args):
        return RocketString(args[0])

    def type(self):
        return self.__repr__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<native type 'String'>"


class RocketString(_RocketInstance):
    def __init__(self, value):
        self.value = value
        self.nature = 'Datatype'

    def get(self, name):
        # Note: 'edna' is what we use to manipulate arity for 'slice' function from '1' to '2'
        if name.lexeme == 'get':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                index = args[0]

                if index >= len(self.value):
                    raise _RuntimeError('String', "IndexError: string index out of range")

                return self.value[index]

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
                    if args[0] >= len(self.value) or args[1] >= len(self.value):
                        raise _RuntimeError('String', "IndexError: string index out of range")

                    else:
                        return self.stringifyList(self.value[args[0]:args[1]])

                return self.stringifyList(self.value[args[0]:])

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.nature = 'native'
            rocketCallable.signature = 'String'
            rocketCallable.toString = "<native method 'slice' of String>"
            rocketCallable.slice = True
            rocketCallable.inc = False

            return rocketCallable

        if name.lexeme == 'count':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                item = args[0]

                if item in self.value:
                    return self.value.count(args[0])

                else:
                    return 0

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'count' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'length':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    return len(self.value)
                else:
                    return 0

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'length' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'remove':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                if self.notEmpty():
                    if args[0] in self.value:
                        self.value.remove(args[0])
                        return None
                    else:
                        raise _RuntimeError('String', "IndexError: Item not in string")
                else:
                    raise _RuntimeError('String', "IndexError: cannot remove items from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'remove' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'sort':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    self.value.sort()
                    return None
                else:
                    return None

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'sort' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'reverse':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    self.value.reverse()
                    return None
                else:
                    return None

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
                        return self.value[0].upper() + self.value[1:]
                    else:
                        return self.value
                else:
                    raise _RuntimeError('String', "IndexError: cannot index from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'endsWith' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'upper':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    return self.value.upper()
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
                    return self.value.lower()
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
                    return self.value.isupper()
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
                    return self.value.islower()
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
                    return self.value.isalpha()
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
                    return self.value.isdecimal()
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
                    return self.value.center(args[0])
                else:
                    raise _RuntimeError('String', "IndexError: cannot index from an empty string")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'upper' of String>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'concat':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                new_list = args[0]

                if isinstance(new_list, RocketString):
                    self.value = self.value + new_list.elements
                    return None
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
                    if args[0] in self.value:
                        return self.value.index(args[0])
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
                    if args[0] in self.value:
                        return True
                    else:
                        return False
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
                    endlen = len(args[0])
                    index = -(endlen)
                    if args[0] == self.value[index:]:
                        return True
                    else:
                        return False
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
                    if args[0] in self.value:
                        # NOTE: Manually implement this later
                        count = self.value.count(args[0])
                        arr = _array.Array().call(interpreter, [count+1])

                        print(args[0], self.value.split(args[0]), arr)
                        tmp_array = self.value.split(args[0])

                        for i in range(count+1):
                            arr.elements[i] = tmp_array[i]

                        return arr
                    else:
                        arr = _array.Array().call(interpreter, [0])
                        arr.elements[0] = self.value

                        return arr
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

    def __repr__(self):
        return f'\033[32m{self.value}\033[0m'

    def __str__(self):
        return self.__repr__()
