from utils.reporter    import runtimeError   as _RuntimeError

from utils.tokens import Token     as _Token
from utils.tokens import TokenType as _TokenType

from utils.misc   import isValNeg as _isValNeg

from native.datastructs.rocketClass import RocketCallable as _RocketCallable
from native.datastructs.rocketClass import RocketInstance as _RocketInstance

from native.datatypes import rocketBoolean as _boolean
from native.datatypes import rocketNumber  as _number


class List(_RocketCallable):
    def __init__(self):
        self.callee = 'List'
        self.nature = 'native'

    def arity(self):
        return 1

    def call(self, obj, args):
        nin_lexeme = obj.KSL[1][_TokenType.NIN.value]

        return RocketList(args, nin_lexeme)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<native type 'List'>"


class RocketList(_RocketInstance):
    def __init__(self, elms, nin_lexeme):
        self.elements = elms
        self.nature = 'datatype'
        self.kind = "<native type 'List'>"
        self.nin_lexeme = nin_lexeme

    def get(self, name: _Token):
        # Note: 'edna' is what we use to manipulate arity for 'slice' function from '1' to '2'
        if name.lexeme == 'get':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                index = args[0].value

                if index >= len(self.elements):
                    raise _RuntimeError('List', "IndexError: list index out of range")

                return self.elements[index]

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'get' of list>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'insert':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 2

            def call(interpreter, args):
                # This fn expects input like the standard Python 'insert' list method
                # 'insert(index, item)'
                # It requires two args exactly
                # where if 'index' is -1 it translates to secone to the last not the last
                # to add an item at the end we need to pass the length of the list as the index
                # i.e. [list].insert([list].length(), [item]) 
                self.elements.insert(args[0].value, args[1])

                return List().call(self, self.elements)

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.nature = 'native'
            rocketCallable.signature = 'List'
            rocketCallable.toString = "<native method 'insert' of List>"
            rocketCallable.insert = True

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
                        raise _RuntimeError('List', "IndexError: list index out of range")

                    # Special case
                    if (args[0].value >= args[1].value):
                        return List().call(self, [])

                    else:
                        return List().call(self, self.elements[args[0].value:args[1].value])

                return List().call(self, self.elements[args[0].value:])

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.nature = 'native'
            rocketCallable.signature = 'List'
            rocketCallable.toString = "<native method 'slice' of List>"
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
                    return List().call(self, [])

                removed_list = []
                is_negative_index = False

                if inc:
                    # Please note, if the item count is zero then nothing is returned
                    if args[1].value == 0:
                        return List().call(self, [])

                    # Negative steps return nothing irrespective of the index
                    # ... so we need to perform a negativivty test on the input
                    if _isValNeg(args[1].value):
                        return List().call(self, [])

                    # Handle Positive and negative index
                    # count is always positive
                    # Run positivity test for index to determine behaviour (adapted from test above)
                    if not _isValNeg(args[0].value):
                        removed_list = self.elements[args[0].value:args[0].value + args[1].value:]

                    else:
                        # I.e. when index is negative
                        idx = args[0].value
                        # step is the index of the starting elm to the next subseq. 'n' (args[1]) elms
                        step = (len(self.elements) + args[0].value) + args[1].value

                        removed_list = self.elements[idx:step:]
                        is_negative_index = True

                else:
                    # if only index provided then the entire list from the index to end is returned
                    removed_list = List().call(self, self.elements[args[0].value:])

                # Remove list items
                # Remember the slices are contiguously stored so we can safely use indexing
                # ... by cutting out the first chunk and last chunk then attaching them (surgically)
                head = self.elements[0:len(self.elements) + args[0].value] if is_negative_index else self.elements[0:args[0].value]
                tail = self.elements[len(self.elements) + args[0].value + args[1].value:] if is_negative_index else self.elements[args[0].value + args[1].value:]

                self.elements = head + tail

                # return removed list slice
                return List().call(self, removed_list)

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.nature = 'native'
            rocketCallable.signature = 'List'
            rocketCallable.toString = "<native method 'splice' of List>"
            rocketCallable.splice = True
            rocketCallable.inc = False

            return rocketCallable

        if (name.lexeme == 'append') or (name.lexeme == 'push'):
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                # Internally add new elm
                self.elements.append(args[0])

                # we return the appended list
                return self

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'append' of List>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'clear':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 0

            def call(interpreter, args):
                self.elements = []

                # return the newly cleared list
                return self

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'clear' of List>"
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
            rocketCallable.toString = "<native method 'length' of List>"
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
                    raise _RuntimeError('List', "IndexError: cannot pop empty list")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'pop' of List>"
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
                        raise _RuntimeError('List', "IndexError: Item not in list")
                
                    else:
                        return _number.Int().call(self, [removed_index])

                else:
                    raise _RuntimeError('List', "IndexError: cannot remove items from an empty list")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'remove' of List>"
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
            rocketCallable.toString = "<native method 'sort' of List>"
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
                    return List().call(self, [])

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'reverse' of List>"
            rocketCallable.nature = 'native'

            return rocketCallable

        if name.lexeme == 'concat':
            rocketCallable = _RocketCallable(self)

            def arity():
                return 1

            def call(interpreter, args):
                if isinstance(args[0], RocketList):
                    # we return the mutation
                    return List().call(self, self.elements + args[0].elements)

                else:
                    raise _RuntimeError('List', "IndexError: can only concatenate 'List' native type with another 'List'.")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'concat' of List>"
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

                    raise _RuntimeError('List', "IndexError: Item not in list")

                else:
                    raise _RuntimeError('List', "IndexError: cannot index from an empty list")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'indexOf' of List>"
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
                    raise _RuntimeError('List', "IndexError: cannot index from an empty list")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'includes' of List>"
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
                    raise _RuntimeError('List', "IndexError: cannot run function on an empty list")

            rocketCallable.arity = arity
            rocketCallable.call = call
            rocketCallable.toString = "<native method 'forEach' of List>"
            rocketCallable.nature = 'native'

            return rocketCallable

        else:
            raise _RuntimeError(name, f"'List' has no method '{name.lexeme}'.")


    def set(self, name, value):
        raise _RuntimeError(name, "Cannot mutate an List's props")


    def notEmpty(self):
        if len(self.elements) == 0:
            return False

        return True

    def stringify(self, elm, uncoloured=False):
        if (_isType(elm, RocketArray) or _isType(elm, _list.RocketList)):
            return elm.__str__()

        if (_isType(elm, _number.RocketInt) or _isType(elm, _number.RocketFloat)):
            return f'\033[36m{elm}\033[0m' if not uncoloured else str(elm.value)

        if _isType(elm, _string.RocketString):
            return f'\033[32m{elm}\033[0m' if not uncoloured else elm.value

        if _isType(elm, _boolean.Bool):
            return f'\033[1m{elm}\033[0m' if not uncoloured else str(elm.value)

        if type(elm) == type(None):
            return '\033[1m' + self.nin_lexeme + '\033[0m' if not uncoloured else self.nin_lexeme


    def stringifyList(self, list, uncoloured=False):
        result = '[ '

        # if called to display and empty List
        if len(list) == 0:
            return []

        if len(list) >= 1:
            for elm in list[0:-1]:
                result += self.stringify(elm, uncoloured) + ", "

            result += f"{self.stringify(list[-1], uncoloured)} ]"

        else:
            result += self.stringify(list[0], uncoloured) + ' ]'

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

    def __len__(self):
        return len(self.elements)
