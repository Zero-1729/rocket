# Author: Abubakar NK (Zero-1729)
# LICENSE: MIT
# Rocket Lang (Stellar) Interpreter (C) 2018

from utils.expr import Expr as _Expr, Assign as _Assign, Variable as _Variable, ExprVisitor as _ExprVisitor, Binary as _Binary, Call as _Call, Get as _Get, Set as _Set, This as _This, Super as _Super, Logical as _Logical, Grouping as _Grouping, Unary as _Unary, Literal as _Literal
from utils.reporter import runtimeError as _RuntimeError, BreakException as _BreakException, ReturnException as _ReturnException
from utils.tokens import Token as _Token, TokenType as _TokenType
from utils.stmt import Stmt as _Stmt, Var as _Var, Const as _Const, If as _If, While as _While, Break as _Break, Func as _Func, Class as _Class, Block as _Block, Return as _Return, StmtVisitor as _StmtVisitor, Del as _Del, Print as _Print, Expression as _Expression
from env import Environment as _Environment
from utils.rocketClass import RocketCallable as _RocketCallable, RocketFunction as _RocketFunction, RocketClass as _RocketClass, RocketInstance as _RocketInstance
from stdlib.functions import locals, clock, copyright, natives, input, random, type


class Interpreter(_ExprVisitor, _StmtVisitor):
    def __init__(self):
        self.globals = _Environment() # For the native functions
        self.environment = _Environment() # Functions / classes
        self.locals = {}
        self.errors = []

        # Statically define 'native' functions
        # random n between '0-1' {insecure}
        self.globals.define(random.Random().callee, random.Random)
        # grab user input
        self.globals.define(input.Input().callee, input.Input)
        # return value type
        self.globals.define(type.Type().callee, type.Type)
        # 'locals' return all globally defined 'vars' and 'consts'
        self.globals.define(locals.Locals().callee, locals.Locals)
        # 'clock'
        self.globals.define(clock.Clock().callee, clock.Clock)
        # 'copyright'
        self.globals.define(copyright.copyright().callee, copyright.copyright)
        # 'natives' -> names of nativr functions
        self.globals.define(natives.Natives().callee, natives.Natives)


    def interpret(self, statements: list):
        try:
            for stmt in statements:
                self.execute(stmt)

        except _RuntimeError as error:
            self.errors.append(error)


    def visitLiteralExpr(self, expr: _Literal):
        return expr.value


    def visitGroupingExpr(self, expr: _Grouping):
        return self.evaluate(expr.expression)


    def visitUnaryExpr(self, expr: _Unary):
        right = self.evaluate(expr.right)

        # Handle '~' bit shifter
        if (expr.operator.type == _TokenType.TILDE):
            self.checkNumberOperand(expr.operator, right)
            return (-float(right) - 1)

        if (expr.operator.type == _TokenType.MINUS):
            self.checkNumberOperand(expr.operator, right)
            return -float(right)

        if (expr.operator.type == _TokenType.BANG):
            return not (self.isTruthy(right))

        # If can't be matched return nothing
        return None


    def visitBinaryExpr(self, expr: _Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        # string concatination and arithmetic operator '+'
        if (expr.operator.type == _TokenType.PLUS):
            if self.is_number(left) and self.is_number(right):
                return left + right

            if (isinstance(left, str) and isinstance(right, str)):
                return left + right

            # To support implicit string concactination
            # E.g "Hailey" + 4 -> "Hailey4"
            if ((isinstance(left, str)) or (isinstance(right, str))):
                # Concatenation of 'nin' is prohibited!
                if left == None or right == None:
                    raise _RuntimeError(expr.operator.lexeme, "Operands must be either both strings or both numbers.")

                return str(left) + str(right)

            raise _RuntimeError(expr.operator.lexeme, "Operands must be either both strings or both numbers.")

        # Arithmetic operators "-", "/", "%", "//", "*", "**"
        if (expr.operator.type == _TokenType.MINUS):
            self.checkNumberOperands(expr.operator, left, right)
            return left - right

        if (expr.operator.type == _TokenType.DIV):
            self.checkNumberOperands(expr.operator, left, right)
            if right == 0:
                raise _RuntimeError(right, "ZeroDivError: Can't divide by zero")

            return left / right

        if (expr.operator.type == _TokenType.MOD):
            self.checkNumberOperands(expr.operator, left, right)
            if right == 0:
                raise _RuntimeError(right, "ZeroDivError: Can't divide by zero")

            return left % right

        if (expr.operator.type == _TokenType.FLOOR):
            self.checkNumberOperands(expr.operator, left, right)
            if right == 0:
                raise _RuntimeError(right, "ZeroDivError: Can't divide by zero")

            return left // right

        if (expr.operator.type == _TokenType.MULT):
            self.checkNumberOperands(expr.operator, left, right)
            return left * right

        if (expr.operator.type == _TokenType.EXP):
            self.checkNumberOperands(expr.operator, left, right)
            return left ** right

        # bitshifters "<<", ">>"
        if (expr.operator.type == _TokenType.LESS_LESS):
            self.checkNumberOperands(expr.operator, left, right)
            return left * (2 ** right)

        if (expr.operator.type == _TokenType.GREATER_GREATER):
            self.checkNumberOperands(expr.operator, left, right)
            return left // (2 ** right)

        # Comparison operators ">", "<", ">=", "<=", "!=", "=="
        if (expr.operator.type == _TokenType.GREATER):
            self.checkNumberOperands(expr.operator, left, right)
            return left > right

        if (expr.operator.type == _TokenType.LESS):
            self.checkNumberOperands(expr.operator, left, right)
            return left < right

        if (expr.operator.type == _TokenType.GREATER_EQUAL):
            self.checkNumberOperands(expr.operator, left, right)
            return left >= right

        if (expr.operator.type == _TokenType.LESS_EQUAL):
            self.checkNumberOperands(expr.operator, left, right)
            return left <= right

        if (expr.operator.type == _TokenType.BANG_EQUAL):
            self.checkValidOperands(expr.operator, left, right)
            return not (self.isEqual(left, right))

        if (expr.operator.type == _TokenType.EQUAL_EQUAL):
            if left == None or right == None:
                return self.isEqual(left, right)

            if isinstance(left, bool) or isinstance(right, bool):
                return self.isEqual(left, right)

            self.checkValidOperands(expr.operator, left, right)
            return self.isEqual(left, right)

        # If can't be matched return None
        return None


    def visitCallExpr(self, expr: _Call):
        callee = self.evaluate(expr.callee)

        eval_args = []
        for arg in expr.args:
            # Fix passing expr and stmt to 'stdlib' functions
            eval_args.append(self.evaluate(arg))

        # Well, built-in functions in 'stdlib/' have a special 'nature' field to distinguish them from user defined funcs.
        isNative = False
        try:
            if callee().nature == "native":
                isNative = True
        except: pass

        # Specially inject check for 'rocketClass'
        isNotCallable = not isinstance(callee, _RocketCallable)
        isNotClass = not isinstance(callee, _RocketClass)

        if isNotCallable and isNotClass and not isNative:
            raise _RuntimeError(expr.paren, "Can only call functions and classes")

        function = callee if not isNative else callee()

        if len(eval_args) != function.arity():
            raise _RuntimeError(expr.callee.name.lexeme, f"Expected '{function.arity()}' args but got '{len(eval_args)}.'")

        return function.call(self, eval_args)


    def visitGetExpr(self, expr: _Get):
        object = self.evaluate(expr.object)

        if isinstance(object, _RocketInstance):
            return object.get(expr.name)

        raise _RuntimeError(expr.name, "Only instances have properties.")


    def visitSetExpr(self, expr: _Set):
        object = self.evaluate(expr.object)

        if not isinstance(object, _RocketInstance):
            raise _RuntimeError(expr.name, "Only instances have fields.")

        value = self.evaluate(expr.value)
        object.set(expr.name, value)

        return value


    def visitThisExpr(self, expr: _This):
        return self.lookUpVariable(expr.keyword, expr)


    def visitSuperExpr(self, expr: _Super):
        # 'super' is defined '2' hops in
        dist = self.locals.get(expr) + 2
        superclass = self.environment.getAt(dist, "super")

        # And 'this' is alwats one nearer than 'super'
        obj = self.environment.getAt(dist - 1, "this")

        method = superclass.locateMethod(obj, expr.method.lexeme)

        if (method == None):
            # Call works but 'msg' not printing
            raise RuntimeError(expr.keyword, "Cannot find undefined method '{expr.method.lexeme}' in superclass")

        return method


    def visitDelStmt(self, stmt: _Del):
        # patch env
        glob = self.globals.values
        var_env = self.environment.values

        for name in stmt.names:
            if name in glob.keys():
                del glob[name]

            if name in var_env.keys():
                del var_env[name]

            else:
                raise _RuntimeError(name, f"can't undefined name '{name}'")

        return None


    def visitExpressionStmt(self, stmt: _Expression):
        self.evaluate(stmt.expression)
        return None


    def visitLogicalExpr(self, expr: _Logical):
        left = self.evaluate(expr.left)
        # Fix for bug #33
        # Bug #33: Check was not evaluating properly. 'OR' slides into 'else' even if matched as 'or'.
        if (expr.operator.type.value == _TokenType.OR.value):
            if self.isTruthy(left):
                return left

        else:
            if not self.isTruthy(left):
                return left

        return self.evaluate(expr.right)


    def visitIfStmt(self, stmt: _If):
         if (self.isTruthy(self.evaluate(stmt.condition))):
             self.execute(stmt.thenBranch)

         #if (stmt.elifCondition != None):
         #    if (self.isTruthy(self.evaluate(stmt.elifCondition))):
         #        self.execute(stmt.elifThenBranch)

         elif (stmt.elseBranch != None):
             self.execute(stmt.elseBranch)

         return None


    def visitWhileStmt(self, stmt: _While):
        try:
            while (self.isTruthy(self.evaluate(stmt.condition))):
                self.execute(stmt.body)

            # TODO: Add support to cover Python's stack trace when CTRL-C is used to exit REPL
        except _BreakException:
            pass

        return None


    def visitBreakStmt(self, stmt: _Break):
        # Just raises 'BreakExveption' to signal 'break'
        raise _BreakException()


    def visitReturnStmt(self, stmt: _Return):
        value = "nin"

        if stmt.value != None:
            value = self.evaluate(stmt.value)

        raise _ReturnException(value)


    def visitPrintStmt(self, stmt: _Print):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None


    def visitVarStmt(self, stmt: _Var):
        if (stmt.initializer is not None):
            value = self.evaluate(stmt.initializer)
        else:
            value = None

        # To avoid redifining vars with the same name as functions or classes
        if stmt.name.lexeme not in self.globals.values.keys():
            self.environment.define(stmt.name.lexeme, value)

        else:
            raise _RuntimeError(stmt.name.lexeme, "Name already defined as 'variable' or 'class' or 'function'")


    def visitConstStmt(self, stmt: _Const):
        value = self.evaluate(stmt.initializer)

        # NOTE: Fix for #19
        # check for variable before definition to avoid passing in 'const' redefinitions
        if self.environment.isTaken(stmt.name):
            raise _RuntimeError(stmt.name.lexeme, "Name already used as 'const'.")

        # stop 'const' re-decl for 'classes' 'functions'
        elif self.globals.isTaken(stmt.name):
            raise _RuntimeError(stmt.name.lexeme, "Name already used as 'class' or 'function' name.")

        # Use different decleration function for consts
        self.environment.decl(stmt.name.lexeme, value)


    def visitFuncStmt(self, stmt: _Func):
        function = _RocketFunction(stmt, self.environment, False)
        self.globals.define(stmt.name.lexeme, function)

        return None


    def visitClassStmt(self, stmt: _Class):
        self.environment.define(stmt.name.lexeme, None)

        superclass = None
        if (stmt.superclass != None):
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, _RocketClass):
                raise _RuntimeError(stmt.superclass.name, "Superclass must be a class.")

        self.environment = _Environment(self.environment)
        self.environment.define("super", superclass)

        methods = {}

        for method in stmt.methods:
            function = _RocketFunction(method, self.environment, method.name.lexeme.__eq__("init"))
            methods[method.name.lexeme] = function

        class_ = _RocketClass(stmt.name.lexeme, superclass, methods)

        if (superclass != None):
            self.environment = self.environment.enclosing

        self.environment.assign(stmt.name, class_)


        return None


    def visitBlockStmt(self, stmt: _Block):
        self.executeBlock(stmt.statements, _Environment(self.environment))
        return None


    def visitAssignExpr(self, expr: _Assign):
        value = self.evaluate(expr.value)
        self.environment.assign(expr.name, value)

        return value


    def visitVariableExpr(self, expr: _Variable):
        # NOTE: 'const' variables get retrieved from this call also
        try:
            return self.globals.get(expr.name)

        except:
            return self.environment.get(expr.name)

        #return self.lookUpVariable(expr.name, expr)


    def execute(self, stmt: _Stmt):
        stmt.accept(self)


    def executeBlock(self, stmts: list, env: _Environment):
        # Save global environment state
        previous = self.environment

        try:
            self.environment = env

            for stmt in stmts:
                self.execute(stmt)

        finally:
            # Resume global environment state
            self.environment = previous


    def evaluate(self, stmt: _Stmt):
        return stmt.accept(self)


    def resolve(self, expr: _Expr, depth: int):
        self.locals[expr] = depth


    def lookUpVariable(self, name: _Token, expr: _Expr):
        dist = self.locals[expr] if self.locals.get(expr) else None

        # remeber that our expr friend is is always hinding at the very first 'env' enclosing; at dist = 0
        # So we might have to do an aditional check to see if the current expr bieng querried is 'this' inorder to artificially make 'dist = 0'
        expr_type = type(expr)
        isFoldedThis = expr.keyword.lexeme == "this" if expr_type == _This else False

        # Check and artificially inject '0' as dist to fetch out 'this' in enclosing env
        # if a nested 'this' is not in the 'expr' then leave dist untouched
        dist = 0 if isFoldedThis else dist

        if (dist != None):
            return self.environment.getAt(dist, name.lexeme)

        else:
            return self.globals.get(name)


    def isTruthy(self, obj: object):
        if (obj == None):
            return False

        if (int(obj) == 0): return False

        if (int(obj) == 1): return True

        if (isinstance(obj, bool)):
            return obj # I.e if "True" return it

        # If its neither false nor "bool" type then it is truthy
        return True


    def isEqual(self, left_obj: object, right_obj: object):
        if ((left_obj == None) and (right_obj == None)):
            return True

        # Nothing but "nin" (None) is equal to it
        if (left_obj == None):
            return False

        return left_obj == right_obj


    def is_number(self, obj: object):
        if isinstance(obj, int) or isinstance(obj, float):
            return True

        else:
            return False


    def checkNumberOperand(self, opetator: _Token, right: object):
        if self.is_number(right): return

        raise _RuntimeError(operator.lexeme, "Operand must be number.")


    def checkNumberOperands(self, operator: _Token, left: object, right: object):
        if self.is_number(left) and self.is_number(right): return

        raise _RuntimeError(operator.lexeme, "Operands must be numbers.")


    def checkValidOperands(self, operator: _Token, left: object, right: object):
        if ((isinstance(left, str)) and (isinstance(right, str))): return

        if self.is_number(left) and self.is_number(right): return

        else:
            # Is comparing strings and numbers really important?
            # Maybe if you are trying to see if a number id transformed to an 'str'.
            # But wouldn't you just check the type with 'Type' native func?!
            raise _RuntimeError(operator.lexeme, "operands must both be either 'strings' or 'numbers'.")


    def stringify(self, value: object):
        # Customize literals
        if (value == None): return "nin"

        # HACK: Against bug #28 'print 0;' -> false && 'print 1;' -> true
        if (value == True and not self.is_number(value)): return "true"
        if (value == False and not self.is_number(value)): return "false"

        # Greedy hack: force 'built-in' funcs to pretty print
        try:
            return value()

        except:
            return value
