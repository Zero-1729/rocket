from rocketClass import RocketCallable as _RocketCallable
from rocketClass import RocketClass, RocketFunction

class Type(_RocketCallable):
    def __init__(self):
        self.callee = "Type"
        self.nature = "native"

    def arity(self):
        return 1

    def call(self, obj: object, args: list):
        # TODO: Create seperate classes for each to be used for checks
        # I.e 'print Type(3) == Int'
        # We handle how type's are represented
        if type(args[0]) == int:
            return "<number 'int'>"

        if type(args[0]) == float:
            return "<number 'float'>"

        if type(args[0]) == str:
            return "<str>"

        # We directly check for 'None'
        if args[0] == None:
            return "<nin>"

        if type(args[0]) == bool:
            # Becuase python internally sees our bools as 'True' and 'False'.
            # So we force our own represenation to the user
            return f"<bool '{str(args[0]).lower()}'>"

        if type(args[0]) == RocketClass:
            print(0)
            return f"<class '{args[0]}'"

        return f"<built-in fn {args[0]().callee}>"


    def type(self):
        return self.__repr__()


    def __repr__(self):
        return "<built-in fn 'Type'>"

    def __str__(self):
        return "<built-in fn 'Type'>"
