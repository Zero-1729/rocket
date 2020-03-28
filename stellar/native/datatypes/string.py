from rocketClass import RocketCallable as _RocketCallable
from rocketClass import RocketInstance as _RocketInstance
from reporter import runtimeError as _RuntimeError

class Array(_RocketCallable):
    def __init__(self):
        self.callee = 'Array'
        self.nature = 'native'

    def arity(self):
        return 1

    def call(self, obj, args):
        size = int(args[0])

        return RocketArray(size)

    def type(self):
        return self.__repr__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<native type 'Array'>"


class RocketArray(_RocketInstance):
    def __init__(self, size):
        self.elements = ['nin' for i in range(size)]
        self.nature = 'Datatype'

    def get(self, name):
        # Note: 'edna' is what we use to manipulate arity for 'slice' function from '1' to '2'
        if name.lexeme == 'get':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                index = args[0]

                if index >= len(self.elements):
                    raise _RuntimeError('Array', "IndexError: list index out of range")

                return self.elements[index]

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'get' of array>"
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
                    if args[0] >= len(self.elements) or args[1] >= len(self.elements):
                        raise _RuntimeError('Array', "IndexError: list index out of range")

                    else:
                        return self.stringifyList(self.elements[args[0]:args[1]])

                return self.stringifyList(self.elements[args[0]:])

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.nature = 'native'
            rocketCallable.signature = 'Array'
            rocketCallable.toString = "<native method 'slice' of Array>"
            rocketCallable.slice = True
            rocketCallable.inc = False

            return rocketCallable

        if name.lexeme == 'append':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                item = args[0]
                self.elements.append(item)

                return None

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'append' of Array>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'clear':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                self.elements = []

                return None

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'clear' of Array>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'length':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    return len(self.elements)
                else:
                    return 0

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'length' of Array>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'pop':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    last = self.elements[-1]
                    self.elements.remove(last)
                    return last
                else:
                    raise _RuntimeError('Array', "IndexError: cannot pop empty list")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'pop' of Array>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'remove':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                if self.notEmpty():
                    if args[0] in self.elements:
                        self.elements.remove(args[0])
                        return None
                    else:
                        raise _RuntimeError('Array', "IndexError: Item not in list")
                else:
                    raise _RuntimeError('Array', "IndexError: cannot remove items from an empty list")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'remove' of Array>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'sort':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    self.elements.sort()
                    return None
                else:
                    return None

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'sort' of Array>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'reverse':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                if self.notEmpty():
                    self.elements.reverse()
                    return None
                else:
                    return None

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'reverse' of Array>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'concat':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                new_list = args[0]

                if isinstance(new_list, RocketArray):
                    self.elements = self.elements + new_list.elements
                    return None
                else:
                    raise _RuntimeError('Array', "IndexError: can only concatenate 'Array' native type with another 'Array'.")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'concat' of Array>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'indexOf':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                if self.notEmpty():
                    if args[0] in self.elements:
                        return self.elements.index(args[0])
                    else:
                        raise _RuntimeError('Array', "IndexError: Item not in list")
                else:
                    raise _RuntimeError('Array', "IndexError: cannot index from an empty list")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'indexOf' of Array>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'includes':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                if self.notEmpty():
                    if args[0] in self.elements:
                        return True
                    else:
                        return False
                else:
                    raise _RuntimeError('Array', "IndexError: cannot index from an empty list")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'includes' of Array>"
            rocketCallable.nature = 'native'

            return rocketCallable


        if name.lexeme == 'forEach':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                if self.notEmpty():
                    print(args[0])
                    for item in self.elements:
                        pass
                else:
                    raise _RuntimeError('Array', "IndexError: cannot run function on an empty list")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'forEach' of Array>"
            rocketCallable.nature = 'native'

            return rocketCallable

        else:
            raise _RuntimeError(name, f"'Array' has no method '{name.lexeme}'.")


    def set(self, name, value):
        raise _RuntimeError(name, "Cannot mutate an Array's props")


    def notEmpty(self):
        if len(self.elements) == 0:
            return False

        return True

    def stringify(self, elm):
        if type(elm) == int or type(elm) == float:
            return f'\033[36m{elm}\033[0m'

        if type(elm) == str:
            if elm == 'nin':
                return '\033[1mnin\033[0m'

            else:
                return f'\033[32m{elm}\033[0m'

        if type(elm) == bool and (type(elm) == True or type(elm) == False):
            return f'\033[1m{elm}\033[0m'

        if type(elm) == None:
            return '\033[1mnin\033[0m'

        return elm


    def stringifyList(self, array):
        result = '[ '

        if len(array) != 1:
            for elm in array[0:-1]:
                result += self.stringify(elm) + ", "

            result += f"{self.stringify(array[-1])} ]"

        else:
            result += self.stringify(array[0]) + ' ]'

        return result

    def __repr__(self):
        if len(self.elements) >= 1:
            return self.stringifyList(self.elements)

        else:
            return '[]'

    def __str__(self):
        return self.__repr__()


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
                        arr = Array().call(interpreter, [count+1])

                        print(args[0], self.value.split(args[0]), arr)
                        tmp_array = self.value.split(args[0])

                        for i in range(count+1):
                            arr.elements[i] = tmp_array[i]

                        return arr
                    else:
                        arr = Array().call(interpreter, [0])
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
