from utils.rocketClass import RocketCallable as _RocketCallable
from utils.rocketClass import RocketInstance as _RocketInstance
from utils.reporter import runtimeError as _RuntimeError

from utils.tokens import Token as _Token

from native.datatypes import rocketBoolean as _boolean
from native.datatypes import rocketNumber as _number


class Array(_RocketCallable):
    def __init__(self):
        self.callee = 'Array'
        self.nature = 'native'

    def arity(self):
        return 1

    def call(self, obj, args):
        return RocketArray(args)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<native type 'Array'>"


class RocketArray(_RocketInstance):
    def __init__(self, elms):
        self.elements = elms
        self.nature = 'datatype'
        self.kind = "<native type 'Array'>"

    def get(self, name: _Token):
        # Note: 'edna' is what we use to manipulate arity for 'slice' function from '1' to '2'
        if name.lexeme == 'get':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                index = args[0].value

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
                    if args[0].value >= len(self.elements) or args[1].value >= len(self.elements):
                        raise _RuntimeError('Array', "IndexError: list index out of range")

                    # Special case
                    if (args[0].value >= args[1].value):
                        return Array().call(self, [])

                    else:
                        return Array().call(self, self.elements[args[0].value:args[1].value])

                return Array().call(self, self.elements[args[0].value:])

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.nature = 'native'
            rocketCallable.signature = 'Array'
            rocketCallable.toString = "<native method 'slice' of Array>"
            rocketCallable.slice = True
            rocketCallable.inc = False

            return rocketCallable

        if name.lexeme == 'splice':
            rocketCallable = _RocketCallable(self)

            def arity(inc=False):
                if inc:
                    return 2

                return 1

            def call(interpreter, args, inc=False):
                # If initial index is beyond the limit then nothing is returned
                if args[0].value >= len(self.elements):
                        return Array().call(self, [])

                removed_array = []
                is_negative_index = False

                if inc:
                    if args[1].value >= len(self.elements):
                        raise _RuntimeError('Array', "IndexError: list index out of range")

                    # Please note, if the item count is zer then nothing is returned
                    if args[1] == 0:
                        return Array().call(self, [])

                    # Negative steps return nothing irrespective of the index
                    # ... so we need to perform a negativivty test on the input
                    # if p is negative then
                    # (p * -1) - p will be equal to twice the absolute value of p (aka |p| ** 2), where x != 0
                    #
                    # Proof:
                    #   Assume x = -x
                    #
                    #   (-x * -1) - (-x)
                    #   = x - (-x)
                    #   = x + x
                    #   2x (hence |x| * 2)
                    #
                    # Now assume x = x
                    #
                    #       (x * -1) - (x)
                    #       -x - x
                    #       -2x (hence -|x| * 2 and not |x| * 2)
                    #
                    # QED
                    if (((args[1] * -1) - args[1]) == 2 * abs(args[1])) and (not args[1] == 0):
                        return Array().call(self, [])

                    # Handle Positive and negative index
                    # count is always positive
                    # Run positivity test for index to determine behaviour (adapted from test above)
                    if (((args[0]) * -1) - args[0]) != 2 * abs(args[0]):
                        removed_array = self.elements[args[0]:args[0] + args[1]:]

                    else:
                        # I.e. when index is negative
                        removed_array = self.elements[args[0]:(args[0] * -1) + args[1]:]
                        is_negative_index = True

                # if only index provided then the entire list from the index to end is returned
                removed_array = Array().call(self, self.elements[args[0]:])

                # Remove array items
                # Remember the slices are contiguously stored so we can safely use indexing
                # ... by cutting out the first chunk and last chunk then attaching them (surgically)
                head = self.elements[0:len(self.elements) + args[0]] if is_negative_index else self.elements[0:args[0]]
                tail = self.elements[len(self.elements) + args[0] + args[1]:] if is_negative_index else self.elements[args[0] + args[1]:]

                self.elements = head + tail

                # return removed array slice
                return Array().call(self, removed_array)

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.nature = 'native'
            rocketCallable.signature = 'Array'
            rocketCallable.toString = "<native method 'splice' of Array>"
            rocketCallable.slice = True
            rocketCallable.inc = False

        if (name.lexeme == 'append') or (name.lexeme == 'push'):
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                # Internally add new elm
                self.elements.append(args[0])

                # we return the appended array
                return self

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

                # return the newly cleared array
                return self

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
                    removed_index = -1

                    for i in range(len(self.elements) - 1):
                        if args[0].value == self.elements[i].value:
                            self.elements.remove(self.elements[i])
                            removed_index = i

                    if removed_index == -1:
                        raise _RuntimeError('Array', "IndexError: Item not in list")
                
                    else:
                        return _number.Int().call(self, [removed_index])

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
                    # internally change and return mutation
                    self.elements.reverse()
                    return self

                else:
                    return Array().call(self, [])

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
                if isinstance(args[0], RocketArray):
                    # we return the mutation
                    return Array().call(self, self.elements + args[0].elements)

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
                    for i in range(len(self.elements)):
                        if args[0].value == self.elements[i].value:
                            return _number.Int().call(self, [i])

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
                    for i in range(len(self.elements)):
                        if args[0].value == self.elements[i].value:
                            return _boolean.Bool().call(self, [True])
                    
                    return _boolean.Bool().call(self, [False])

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
                    for item in self.elements: args[0].call(interpreter, [item])
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

    def stringify(self, elm, uncoloured=False):
        try:
            elm = elm.value

        except:
            # If detected 'Array'
            return elm.__str__()

        if uncoloured:
            return elm.__str__() if elm != None else 'nin'

        if type(elm) == int or type(elm) == float:
            return f'\033[36m{elm}\033[0m' if not uncoloured else elm

        if type(elm) == str:
            if elm == 'nin':
                return '\033[1mnin\033[0m' if not uncoloured else 'nin'

            else:
                return f'\033[32m{elm}\033[0m' if not uncoloured else elm

        if type(elm) == bool and (type(elm) == True or type(elm) == False):
            return f'\033[1m{elm}\033[0m' if not uncoloured else elm

        if type(elm) == None:
            return '\033[1mnin\033[0m' if not uncoloured else 'nin'

        return elm


    def stringifyList(self, array, uncoloured=False):
        result = '[ '

        # if called to display and empty Array
        if len(array) == 0:
            return []

        if len(array) >= 1:
            for elm in array[0:-1]:
                result += self.stringify(elm, uncoloured) + ", "

            result += f"{self.stringify(array[-1], uncoloured)} ]"

        else:
            result += self.stringify(array[0], uncoloured) + ' ]'

        return result

    def raw_string(self):
        if len(self.elements) > 0:
            return self.stringifyList(self.elements, True)

        else:
            return '[]'

    def __repr__(self):
        if len(self.elements) >= 1:
            return self.stringifyList(self.elements)

        else:
            return "[]"

    def __str__(self):
        return self.__repr__()