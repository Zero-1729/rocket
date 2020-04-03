from utils.rocketClass import RocketCallable as _RocketCallable
import codecs

class Print(_RocketCallable):
    def __init__(self):
        self.callee = "Print"
        self.nature = "native"
        self.kind = "<native function type>"

    def arity(self, n=1):
        # Allow almost infinite args to be passed
        return n

    def call(self, obj: object, args: list):
        # We will permit escsaped characters on user outputs, like '\n', '\t', etc
        # wrap it in 'utf-8' to decode escapes
        string = ''

        # Assuming we recieved no args it would just print a blank line
        # This is because that's the default behaviour in Python when 'print()' is called with no args

        # build string
        for i in range(len(args)):
            string += stringify(args[i])
            # the strings are separated by a space
            string += ' ' if should_space(stringify(args[i]), i, (len(args) - 1)) else ''

        encoded_input = codecs.escape_decode(string, "utf-8")[0]
        print("\033[32m" + encoded_input.decode("utf-8") + "\033[0m")

    def __repr__(self):
        return "<native fn 'Print'>"

    def __str__(self):
        return "<native fn 'Print'>"


def is_last_empty(item):
    # There are times where a user adds extra space after a string
    # and so we need to disable the xtra space we add
    return not (item[-1] == ' ')


def should_space(item, idx, lim):
    return is_last_empty(item) and idx < lim


def stringify(item):
    if (hasattr(item, 'nature')):
        if (item.nature == 'datatype'):
            return item.raw_string()

    return item.__str__()