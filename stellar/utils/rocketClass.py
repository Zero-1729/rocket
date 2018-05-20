from env import Environment as _Environment
from utils.reporter import runtimeError as _RuntimeError
from tokens import Token as _Token


class RocketCallable:
    def __init__(self, callee):
        self.callee = callee

    def arity(self):
        return NotImplementedError

    def call(self, interpreter: object,  args: list):
        raise NotImplementedError


class RocketClass(RocketCallable):
    def __init__(self, name, superclass, methods: dict):
        self.name = name
        self.superclass = superclass
        self.methods = methods
        self.merged = False


    def locateMethod(self, instance: object, name: str):
        if self.methods.get(name):
            return self.methods.get(name).bind(instance)

        if self.superclass != None:
            return self.superclass.locateMethod(instance, name)

        return None


    def merge_inits(self, sub, sup, short_sup_init=False):
        # store copy, to be manipulated and used
        tmp = sup

        # So, we loop through sub checking the names declared in the inits
        # if we find a name that appears in both the sub-class 'init' and the super-clas 'init' we just shadow the super-class with the sub-class decl.
        # At the end unmatched decls are simply added to the sub's decls. Forming a fully merged (inherited and shadow ready) list of decls on the sub-class's 'init' method
        # TODO: In the future, use this loop to 'loop-n-merge' all the super-classes of a subclass

        # We loop through using this sub's decls body IF and ONLY if sup decls body is longer than sub's ELSE we use sup's decls body len
        # 'lim' is the number we use to loop with
        lim = len(sub.decleration.body)

        # check for sup-init decls height and adjust lim appropriately
        if short_sup_init: lim = len(sup.decleration.body)

        for i in range(lim):
            subdec = sub.decleration.body[i].expression.name.lexeme
            supdecs = [i.expression.name.lexeme for i in tmp.decleration.body]

            if subdec in supdecs:
                index = tmp.decleration.body[i]
                tmp.decleration.body.remove(index)

        sub.decleration.body += tmp.decleration.body

        self.superclass.bp_arity = True

        return sub


    def call(self, interpreter: object, args: list):
        instance = RocketInstance(self)

        # Grab subclass
        sub_init = self.methods.get("init")
        super_init = None

        # Grab superclass and leave untouched
        if self.superclass != None:
            super_init = self.superclass.methods.get("init")

        # Align init to sub unless we need to merge with a sup-class
        # Remember, sometimes a subclass might not have 'init' only in its superclass. So we just set it to superclass's 'init'
        init = sub_init if sub_init != None else super_init

        if super_init != None:
            # only merge if super-class has more than or just as many 'init' decls
            if not len(super_init.decleration.body) == 0 and sub_init != None:
                # Lets merge the params also
                # But make sure the order is still matched
                # I.e init(type) (sup) init(x, y) (sub) --> init(type, x, y) not init(x, y, type)
                init.decleration.params = [p for p in super_init.decleration.params if p not in init.decleration.params] + init.decleration.params
                init = self.merge_inits(sub_init, super_init, len(super_init.decleration.body) < len(sub_init.decleration.body))
                self.merged = True

        if init != None:
            binded_init = init.bind(instance)
            binded_init.call(interpreter, args)

        return instance


    def arity(self):
        # Fix so tha KSL still applies here and in 'self.call()'
        # Add dynamic superclass res for params and iinit. Maybe we call a function who knows
        init_arity = 0

        sub_init = True if self.methods.get("init") != None else False
        sup = True if self.superclass != None else False

        # Yeah, I know. Hack much?!
        # But consider if we inherit an empty class, trying to make a get wouldn't work do we make sure it exists first
        sup_init = True if sup and self.superclass.methods.get('init') else False

        if sup_init:
            # has both then combine arities
            if sub_init:
                init_arity = self.methods['init'].arity()
                # Only increment when sub's 'merged' flag bot set. I.e sub and sup 'inits' haven't merged. To avoid overflow of sub's arity
                if not self.merged:
                    init_arity += self.superclass.methods['init'].arity()

            if not sub_init:
                init_arity = self.superclass.methods.get("init").arity()

        # Only branch if sub has one 'init', i.e its own
        if sub_init and not sup_init:
            init_arity = self.methods.get("init").arity()


        return init_arity


    def type(self):
        return self.__repr__()


    def __str__(self):
        return f"<class '{self.name}'>"


    def __repr__(self):
        return self.__str__()


class RocketInstance:
    def __init__(self, _class: RocketClass):
        self._class = _class
        self.fields = {}


    def get(self, name: _Token):
        # Not exactly sure why accessing a value stored as '0' causes regular 'if something' check to be jumped. So we explicitly check to see if it is not 'None'
        if self.fields.get(name.lexeme) != None:
            return self.fields.get(name.lexeme)

        method = self._class.locateMethod(self, name.lexeme)

        if method != None:
            # 'iniy' should just return an instance when called instead of 'nin'
            if method.isInit:
                return method.bind(self)

            return method

        raise _RuntimeError(name, f"Undefined property '{name.lexeme}.")


    def set(self, name: _Token, value: object):
        self.fields[name.lexeme] = value


    def type(self):
        return self.__repr__()


    def __str__(self):
        return f"<class instanceOf '{self._class.name}'>"


    def __repr__(self):
        return self.__str__()



class RocketFunction(RocketCallable):
    def __init__(self, decleration, closure, isInit):
        super(RocketCallable)
        self.closure = closure
        self.decleration = decleration
        self.isInit = isInit


    def bind(self, instance: RocketInstance):
        env = _Environment(self.closure)
        env.define("this", instance)

        bounded = RocketFunction(self.decleration, env, self.isInit)
        return bounded


    def arity(self):
        return len(self.decleration.params)


    def call(self, interpreter: object, args: list):
        env = _Environment(self.closure)

        for i in range(len(self.decleration.params)):
            env.define(self.decleration.params[i].lexeme, args[i])

        try:
            interpreter.executeBlock(self.decleration.body, env)

        # Hack to avoid "ReturnException" from prematurely quiting prog
        except Exception as ret:
            if ret.returnable():
                return ret.value

            # If 'ret' is not 'returnable'
            # its most probably a sub-class of 'Exception' (an Error)
            else:
                return ret

        if (self.isInit):
            return self.closure.getAt(0, "this")

        return "nin"


    def type(self):
        return self.__repr__()


    def __str__(self):
        return f"<fn '{self.decleration.name.lexeme}'>"

    def __repr__(self):
        return self.__str__()
