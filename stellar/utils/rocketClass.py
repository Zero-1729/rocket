from env import Environment as _Environment
from reporter import ReturnException as _ReturnException

class RocketCallable:
    def __init__(self, callee):
        self.callee = callee

    def arity(self):
        return NotImplementedError

    def call(self, interpreter: object,  args: list):
        raise NotImplementedError


class RocketFunction(RocketCallable):
    def __init__(self, decleration, closure):
        super(RocketCallable)
        self.closure = closure
        self.decleration = decleration

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
            return ret.value

        return "nin"

    def __repr__(self):
        return f"<fn {self.decleration.name.lexeme}>"

    def __str__(self):
        return f"<fn {self.decleration.name.lexeme}>"
