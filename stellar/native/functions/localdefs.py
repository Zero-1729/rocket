from utils.rocketClass import RocketCallable as _RocketCallable


class Locals(_RocketCallable):
    def __init__(self):
        self.callee = "Locals"
        self.nature = "native"
        self.kind = "<native function type>"

    def arity(self):
        return 0

    def call(self, obj: object, args: list):
        # get locals in global scope
        global_env_var_locals = [loc for loc in obj.environment.values.keys()]
        global_env_const_locals = [loc for loc in obj.environment.statics.keys()]

        # Just in case the user decides that they want to use the output from 'locals'
        if global_env_var_locals or global_env_const_locals:
            return "Vars: " + ', '.join(global_env_var_locals) + "\nConstants: " + ', '.join(global_env_const_locals)

        else:
            return None

    def __repr__(self):
        return "<native fn 'Locals'>"

    def __str__(self):
        return "<native fn 'Locals'>"
