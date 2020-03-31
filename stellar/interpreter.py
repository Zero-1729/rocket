# Author: Abubakar N K (Zero-1729)
# LICENSE: RLOL
# Rocket Lang (Stellar) Interpreter (C) 2018

import sys
import os

from utils.expr import Expr as _Expr, Assign as _Assign, Variable as _Variable, ExprVisitor as _ExprVisitor, Binary as _Binary, Call as _Call, Get as _Get, Set as _Set, Function as _Function, This as _This, Super as _Super, Conditional as _Conditional, Logical as _Logical, Grouping as _Grouping, Unary as _Unary, Literal as _Literal
from utils.reporter import runtimeError as _RuntimeError, BreakException as _BreakException, ReturnException as _ReturnException
from utils.tokens import Token as _Token, TokenType as _TokenType
from utils.stmt import Stmt as _Stmt, Var as _Var, Const as _Const, Import as _Import, If as _If, While as _While, Break as _Break, Func as _Func, Class as _Class, Block as _Block, Return as _Return, StmtVisitor as _StmtVisitor, Del as _Del, Print as _Print, Expression as _Expression
from env import Environment as _Environment
from utils.rocketClass import RocketCallable as _RocketCallable, RocketFunction as _RocketFunction, RocketClass as _RocketClass, RocketInstance as _RocketInstance
from scanner import Scanner as _Scanner
from parser import Parser as _Parser
from native.functions import locals, clock, copyright, natives, input, random, output
from native.datatypes import array, string, number


class Interpreter(_ExprVisitor, _StmtVisitor):
    def __init__(self):
        self.globals = _Environment() # For the native functions
        self.environment = _Environment() # Functions / classes
        self.locals = {}
        self.errors = []
        self.KSL = None
        self.stackCount = 0 # tracks stmt repetitions, 'stackoverflow' errs
        self.fnCallee = None # Tracks current fn callee

        # Statically define 'native' functions
        # random n between '0-1' {insecure}
        self.globals.define(random.Random().callee, random.Random)
        # print (escaped) output. i.e print("hello\tmr.Jim") -> "Hello	mr.Jim"
        self.globals.define(output.Print().callee, output.Print)
        # grab user input
        self.globals.define(input.Input().callee, input.Input)
        # 'locals' return all globally defined 'vars' and 'consts'
        self.globals.define(locals.Locals().callee, locals.Locals)
        # 'clock'
        self.globals.define(clock.Clock().callee, clock.Clock)
        # 'copyright'
        self.globals.define(copyright.Copyright().callee, copyright.Copyright)
        # 'natives' -> names of nativr functions
        self.globals.define(natives.Natives().callee, natives.Natives)

        # Datatypes
        self.globals.define(array.Array().callee, array.Array)
        self.globals.define(string.String().callee, string.String)
        self.globals.define(number.Int().callee, number.Int)
        self.globals.define(number.Float().callee, number.Float)


    def interpret(self, statements: list):
        try:
            for stmt in statements:
                if type(stmt) == list:
                    # We know we have proberbly hit a multi-variable definition
                    for decl in stmt:
                        self.execute(decl)

                else:
                    self.execute(stmt)

        except _RuntimeError as error:
            # Hopefully our last hack.
            # Remember that 'raising' reference error
            # caught inside of funcs/meths doesn't turn up here
            # instead we manually print it.
            # To make it uniform we only print it in 'visitVariableStmt'
            # to avoid duplicates
            if 'ReferenceError:' not in error.msg:
                self.errors.append(error)
            else:
                pass


    def visitLiteralExpr(self, expr: _Literal):
        if type(expr.value) == int:
            return number.Int().call(self, [expr.value])

        if type(expr.value) == float:
            return number.Float().call(self, [expr.value])

        if type(expr.value) == str:
            return string.String().call(self, [expr.value])

        return expr.value


    def visitGroupingExpr(self, expr: _Grouping):
        return self.evaluate(expr.expression)


    def visitUnaryExpr(self, expr: _Unary):
        right = self.evaluate(expr.right)
        right = number.Int().call(self, [right]) if type(right) == int else number.Float().call(self, [right])

        # Handle '~' bit shifter
        if (expr.operator.type == _TokenType.TILDE):
            self.checkNumberOperand(expr.operator, right.value)
            sum = -right.value - 1
            return number.Int().call(self, [sum]) if type(sum) == int else number.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.MINUS):
            self.checkNumberOperand(expr.operator, right.value)
            sum = -right.value
            return number.Int().call(self, [sum]) if type(sum) == int else number.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.BANG):
            return not (self.isTruthy(right.value))

        # If can't be matched return nothing
        return None


    def visitBinaryExpr(self, expr: _Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        left = number.Int().call(self, [left]) if type(left) == int else number.Float().call(self, [left])
        right = number.Int().call(self, [right]) if type(right) == int else number.Float().call(self, [right])

        # string concatenation and arithmetic operator '+'
        if (expr.operator.type == _TokenType.PLUS):
            if self.is_number(left.value) and self.is_number(right.value):
                sum = left.value + right.value
                return number.Int().call(self, [sum]) if type(sum) == int else number.Float().call(self, [sum])

            if (isinstance(left, str) and isinstance(right, str)):
                return string.String().call(self, [left + right])

            # To support implicit string concactination
            # E.g "Hailey" + 4 -> "Hailey4"
            # No need to allow this anymore. We make 'String' compulsory
            if ((isinstance(left, str)) or (isinstance(right, str))):
                # Concatenation of 'nin' is prohibited!
                if left.value == None or right.value == None:
                    raise _RuntimeError(expr.operator.lexeme, "Operands must be either both strings or both numbers.")

                return string.String().call(self, [str(left) + str(right)])

            raise _RuntimeError(expr.operator.lexeme, "Operands must be either both strings or both numbers.")

        # Arithmetic operators "-", "/", "%", "//", "*", "**"
        if (expr.operator.type == _TokenType.MINUS):
            self.checkNumberOperands(expr.operator, left.value, right.value)
            sum = left.value - right.value
            return number.Int().call(self, [sum]) if type(sum) == int else number.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.DIV):
            self.checkNumberOperands(expr.operator, left.value, right.value)
            if right.value == 0:
                raise _RuntimeError(right, "ZeroDivError: Can't divide by zero")

            sum = left.value / right.value
            return number.Int().call(self, [sum]) if type(sum) == int else number.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.MOD):
            self.checkNumberOperands(expr.operator, left.value, right.value)
            if right.value == 0:
                raise _RuntimeError(right, "ZeroDivError: Can't divide by zero")

            sum = left.value % right.value
            return number.Int().call(self, [sum]) if type(sum) == int else number.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.FLOOR):
            self.checkNumberOperands(expr.operator, left.value, right.value)
            if right.value == 0:
                raise _RuntimeError(right, "ZeroDivError: Can't divide by zero")

            sum = left.value // right.value
            return number.Int().call(self, [sum]) if type(sum) == int else number.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.MULT):
            self.checkNumberOperands(expr.operator, left.value, right.value)
            sum = left.value * right.value
            return number.Int().call(self, [sum]) if type(sum) == int else number.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.EXP):
            self.checkNumberOperands(expr.operator, left.value, right.value)
            sum = left.value ** right.value
            return number.Int().call(self, [sum]) if type(sum) == int else number.Float().call(self, [sum])

        # bitshifters "<<", ">>"
        if (expr.operator.type == _TokenType.LESS_LESS):
            self.checkNumberOperands(expr.operator, left.value, right.value)
            sum = left.value * (2 ** right.value)
            return number.Int().call(self, [sum]) if type(sum) == int else number.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.GREATER_GREATER):
            self.checkNumberOperands(expr.operator, left.value, right.value)
            sum = left.value // (2 ** right.value)
            return number.Int().call(self, [sum]) if type(sum) == int else number.Float().call(self, [sum])

        # Comparison operators ">", "<", ">=", "<=", "!=", "=="
        if (expr.operator.type == _TokenType.GREATER):
            self.checkNumberOperands(expr.operator, left.value, right.value)
            return left.value > right.value

        if (expr.operator.type == _TokenType.LESS):
            self.checkNumberOperands(expr.operator, left.value, right.value)
            return left.value < right.value

        if (expr.operator.type == _TokenType.GREATER_EQUAL):
            self.checkNumberOperands(expr.operator, left.value, right.value)
            return left.value >= right.value

        if (expr.operator.type == _TokenType.LESS_EQUAL):
            self.checkNumberOperands(expr.operator, left.value, right.value)
            return left.value <= right.value

        if (expr.operator.type == _TokenType.BANG_EQUAL):
            self.checkValidOperands(expr.operator, left.value, right.value)
            return not (self.isEqual(left.value, right.value))

        if (expr.operator.type == _TokenType.EQUAL_EQUAL):
            if left.value == None or right.value == None:
                return self.isEqual(left.value, right.value)

            if isinstance(left.value, bool) or isinstance(right.value, bool):
                return self.isEqual(left.value, right.value)

            self.checkValidOperands(expr.operator, left.value, right.value)
            return self.isEqual(left.value, right.value)

        # If can't be matched return None
        return None


    def visitCallExpr(self, expr: _Call):
        callee = self.evaluate(expr.callee)

        eval_args = []
        for arg in expr.args:
            # Fix passing expr and stmt to 'stdlib' functions
            eval_args.append(self.evaluate(arg))

        # Well, built-in functions in 'native/' have a special 'nature' field to distinguish them from user defined funcs.
        isNotNative = True
        isNotDatatype = True
        try:
            if callee().nature == "native":
                isNotNative = False
        except:
            if hasattr(callee, 'nature'):
                isNotDatatype = False

        # Specially inject check for 'rocketClass' and 'rocketCallable'
        isNotCallable = not isinstance(callee, _RocketCallable)
        isNotClass = not isinstance(callee, _RocketClass)

        if isNotCallable and isNotClass and isNotNative and isNotDatatype:
            raise _RuntimeError(expr.paren, "Can only call functions and classes")

        function = callee if isNotNative else callee()

        # We dynamically change 'arity' for Array's 'slice' fn depending on the args
        if not isNotDatatype:
            if hasattr(function, 'signature') and hasattr(function, 'slice'):
                if function.signature == 'Array' and len(eval_args) == 2:
                    function.inc = True

        if hasattr(function, 'slice'):
            if len(eval_args) != function.arity(function.inc):
                raise _RuntimeError(expr.callee.name.lexeme, f"Expected '{function.arity(function.inc)}' args but got '{len(eval_args)}.'")

        else:
            # We handle 'Print()' carefully here. so that it print a newline when no args are given
            if isinstance(function, output.Print) and len(eval_args) == 0:
                return function.call(self, [''])

            if len(eval_args) != function.arity():
                raise _RuntimeError(expr.callee.name.lexeme, f"Expected '{function.arity()}' args but got '{len(eval_args)}.'")

        if hasattr(function, 'inc'):
            return function.call(self, eval_args, function.inc)

        else:
            try:
                # Monitor recursive calls to same function
                # set current function
                if (self.stackCount == 66):
                    # Reset counter
                    self.stackCount = 0

                    raise _RuntimeError(expr.callee.name.lexeme, f"Maximum recursion depth reached from calls to '{expr.callee.name.lexeme}' fn.")

                # We increment our stack counter if same fn called from previous call
                if (self.fnCallee == expr.callee.name.lexeme):
                    self.stackCount += 1

                # Set new fn callee
                else:
                    self.fnCallee = expr.callee.name.lexeme
                
                return function.call(self, eval_args)

            except Exception as err:
                self.errors.append(err)
                # Trip the interpreter to halt it from printing/returning 'nin'
                raise err


    def visitGetExpr(self, expr: _Get):
        object = self.evaluate(expr.object)

        if isinstance(object, _RocketInstance):
            return object.get(expr.name)

        # Another special check for datatypes
        if hasattr(object, 'nature'):
            try:
                return object.get(expr.name)
            except Exception as err:
                raise _RuntimeError(err.token, err.msg)

        else:
            raise _RuntimeError(expr.name, "Only instances have properties.")


    def visitSetExpr(self, expr: _Set):
        object = self.evaluate(expr.object)

        if hasattr(object, 'nature'):
            raise _RuntimeError('Array', f"Cannot assign external attribute to native datatype 'Array'")

        if not isinstance(object, _RocketInstance):
            raise _RuntimeError(expr.name, "Only instances have fields.")

        value = self.evaluate(expr.value)
        object.set(expr.name, value)

        return value


    def visitConditionalExpr(self, expr: _Conditional):
        if self.isTruthy(self.evaluate(expr.expr)):
            return self.evaluate(expr.thenExpr)

        else:
            return self.evaluate(expr.elseExpr)


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


    def visitFunctionExpr(self, expr: _Function):
        this_lexeme = self.KSL[1][_TokenType.THIS.value]
        return _RocketFunction(expr, self.environment, False, this_lexeme, True)


    def visitThisExpr(self, expr: _This):
        return self.lookUpVariable(expr.keyword, expr)


    def visitSuperExpr(self, expr: _Super):
        this_lexeme = self.KSL[1][_TokenType.THIS.value]
        super_lexeme = self.KSL[1][_TokenType.SUPER.value]

        # 'super' is defined '2' hops in
        dist = self.locals.get(expr) + 2
        superclass = self.environment.getAt(dist, super_lexeme)

        # And 'this' is alwats one nearer than 'super'
        obj = self.environment.getAt(dist - 1, this_lexeme)

        method = superclass.locateMethod(obj, expr.method.lexeme)

        if (method == None):
            # Call works but 'msg' not printing
            raise RuntimeError(expr.keyword, "Cannot find undefined method '{expr.method.lexeme}' in superclass")

        # If we called the 'init' method of our superclass we just return an instance of the superclass
        if method.__str__() == "<fn 'init'>":
            return superclass

        return method


    def visitDelStmt(self, stmt: _Del):
        # patch env
        glob = self.globals.values
        var_env = self.environment.values
        const_env = self.environment.statics

        for name in stmt.names:
            if name in glob.keys():
                del glob[name]
                return None

            if name in var_env.keys():
                del var_env[name]
                return None

            if name in const_env.keys():
                del const_env[name]
                return None

            else:
                raise _RuntimeError(name, f"can't undefined name '{name}'")
                return None


    def visitExpressionStmt(self, stmt: _Expression):
        self.evaluate(stmt.expression)
        return None


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


    def visitImportStmt(self, stmt: _Import):
        import_lexeme = self.KSL[1][_TokenType.IMPORT.value]

        # TODO: add more built-in modules
        native_modules = [
            'math' # Note: even this module isn't done
        ]

        if len(stmt.modules) == 0:
            raise _RuntimeError(import_lexeme, f"{import_lexeme} statement requires atleast one module name.")

        for module in stmt.modules:
            if module.type == _TokenType.IDENTIFIER and module.lexeme in native_modules:
                # read and execute sorce file
                contents = ''

                # Get exec base home
                basehome = os.path.dirname(os.path.realpath(__file__))

                # Assemble native module path
                filename = os.path.join(basehome, "native/modules/" + module.lexeme + '.rckt')

                with open(filename, 'r') as f:
                    contents = f.read()
                    f.close()

                    tks = _Scanner(contents, self.KSL[0]).scan()
                    stmts = _Parser(tks, self.KSL[1]).parse()
                    self.interpret(stmts)

            else:
                try:
                    # read and execute sorce file
                    contents = ''

                    # This way the user can specify both './path/to/module.rckt' and './path/to/module' are valid
                    filename = (module.lexeme + '.rckt') if module.lexeme.split(os.path.extsep)[-1] != 'rckt' else module.lexeme

                    with open(filename, 'r') as f:
                        contents = f.read()
                        f.close()

                        tks = _Scanner(contents, self.KSL[0]).scan()
                        stmts = _Parser(tks, self.KSL[1]).parse()
                        self.interpret(stmts)

                except FileNotFoundError:
                    raise _RuntimeError(import_lexeme, f"No native or local module named '{module.lexeme}'.")

        return None


    def visitPrintStmt(self, stmt: _Print):
        value = self.evaluate(stmt.expression)
        val, color = self.stringify(value)

        if color:
            print(f"{color}{val}\033[0m")
        else:
            # to force '__str__' to be printed for 'native' methods
            if hasattr(val, 'toString'):
                print(val.toString)

            else:
                print(val)

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
        this_lexeme = self.KSL[1][_TokenType.THIS.value]

        function = _RocketFunction(stmt, self.environment, False, this_lexeme)
        self.globals.define(stmt.name.lexeme, function)

        return None


    def visitClassStmt(self, stmt: _Class):
        super_lexeme = self.KSL[1][_TokenType.SUPER.value]
        this_lexeme = self.KSL[1][_TokenType.THIS.value]

        superclass = None
        if (stmt.superclass != None):
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, _RocketClass):
                raise _RuntimeError(stmt.superclass.name, "Superclass must be a class.")

        self.environment.define(stmt.name.lexeme, None)

        if stmt.superclass != None:
            self.environment = _Environment(self.environment)
            self.environment.define(super_lexeme, superclass)

        methods = {}

        for method in stmt.methods:
            function = _RocketFunction(method, self.environment, method.name.lexeme.__eq__("init"), this_lexeme)
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
        if type(expr.value) == list:
            init_value = self.environment.get(expr.value[0])
            var_value = expr.value[1] if type(expr.value[1]) != _Literal else self.evaluate(expr.value[1])

            ### Lets handle our post fix arithmetic ops

            # First lets start with '++'
            if expr.value[2] == 'inc':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform arithmetic increment on string.")

                value = number.Int().call(self, [init_value.value + 1]) if type(init_value.value) == int else number.Float().call(self, [init_value.value + 1])

                self.environment.assign(expr.name, value)

                # I.e :-
                #       var p = 2;
                #       print p++; /// returns '2'
                return init_value

            # For our decrement post fix operator '--'
            if expr.value[2] == 'dec':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform arithmetic decrement on string.")

                value = number.Int().call(self, [init_value.value - 1]) if type(init_value) == int else number.Float().call(self, [init_value.value - 1])

                self.environment.assign(expr.name, value)

                # I.e :-
                #       var p = 2;
                #       print p--; /// returns '2'
                return init_value

            ### END of post arithmetic ops

            ### Beginning of assignment arithmetic ops

            # Perform op check to determine arithmetic operation to perform
            # Check for '+='
            # also works in cases were string concatenation is intended 'home += "/Github;"'
            if expr.value[2] == 'add':
                value = init_value.value + var_value
                value = number.Int().call(self, [value]) if type(value) == int else number.Float().call(self, [value])

                self.environment.assign(expr.name, value)

                return value

            # Check for '-='
            if expr.value[2] == 'sub':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform subtraction arithmetic assignment on string.")

                value = init_value.value - var_value
                value = number.Int().call(self, [value]) if type(value) == int else number.Float().call(self, [value])

                self.environment.assign(expr.name, value)

                return value

            # Check for '*='
            if expr.value[2] == 'mul':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform multiplication arithmetic assignment on string.")

                value = init_value.value * var_value
                value = number.Int().call(self, [value]) if type(value) == int else number.Float().call(self, [value])

                self.environment.assign(expr.name, value)

                return value

            # Check for '/='
            if expr.value[2] == 'div':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform division arithmetic assignment on string.")

                value = init_value.value / var_value
                value = number.Int().call(self, [value]) if type(value) == int else number.Float().call(self, [value])

                self.environment.assign(expr.name, value)

                return value

            # Check for '//='
            if expr.value[2] == 'flo':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform floor division arithmetic assignment on string.")

                value = init_value.value // var_value
                value = number.Int().call(self, [value]) if type(value) == int else number.Float().call(self, [value])

                self.environment.assign(expr.name, value)

                return value

            # Check for '%='
            if expr.value[2] == 'mod':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform modulo arithmetic assignment on string.")

                value = init_value.value % var_value
                value = number.Int().call(self, [value]) if type(value) == int else number.Float().call(self, [value])

                self.environment.assign(expr.name, value)

                return value

            # Check for '**='
            if expr.value[2] == 'exp':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform exponent arithmetic assignment on string.")

                value = init_value.value ** var_value
                value = number.Int().call(self, [value]) if type(value) == int else number.Float().call(self, [value])

                self.environment.assign(expr.name, value)

                return value

            ### END of assignment arithmetic ops

        else:
            value = self.evaluate(expr.value)

            try:
                self.environment.assign(expr.name, value)
            except _RuntimeError as error:
                if 'ReferenceError:' in error.msg:
                    self.errors.append(error)
                else:
                    pass

            return value


    def visitVariableExpr(self, expr: _Variable):
        # NOTE: 'const' variables get retrieved from this call also
        try:
            return self.globals.get(expr.name)

        except:
            # We try to see if its in either 'envs'
            # if not we raise the exception for our interpreter to catch
            try:
                return self.environment.get(expr.name)

            except _RuntimeError as err:
                print(err, file=sys.stderr)
                raise _RuntimeError(err.token, err.msg)

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


    def evaluate(self, expr: _Expr):
        return expr.accept(self)


    def resolve(self, expr: _Expr, depth: int):
        self.locals[expr] = depth


    def lookUpVariable(self, name: _Token, expr: _Expr):
        this_lexeme = self.KSL[1][_TokenType.THIS.value]
        dist = self.locals[expr] if self.locals.get(expr) else None

        # remeber that our expr friend is always hidden at the very first 'env' enclosing; at dist = 0
        # So we might have to do an aditional check to see if the current expr bieng querried is 'this' inorder to artificially make 'dist = 0'
        expr_type = expr.parent()
        isFoldedThis = expr.keyword.lexeme == this_lexeme if expr_type == "Expr" else False

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


    def checkNumberOperand(self, operator: _Token, right: object):
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
        if (value == None) or value == "nin": return "nin", "\033[1m"

        # HACK: Against bug #28 'print 0;' -> false && 'print 1;' -> true
        if (value == True and type(value) == bool): return "true", "\033[1m"
        if (value == False and type(value) == bool): return "false", "\033[1m"

        if isinstance(value, str):
            if value == '':
                return value, None

            if value[0] == '[' and value[-1]:
                return value, None

            return value, "\033[32m"

        elif isinstance(value, int) or isinstance(value, float):
            return value, "\033[36m"

        else:
            try:
                if (value().nature == "native"):
                    return value(), None

            except:
                return value, None
