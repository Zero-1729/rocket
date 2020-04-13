# Author: Abubakar Nur Kahlil (Zero-1729)
# LICENSE: RLOL
# Rocket Lang (Stellar) Interpreter (C) 2018

import sys as _sys
import os  as _os

from utils.expr import Expr         as _Expr
from utils.expr import Assign       as _Assign
from utils.expr import Variable     as _Variable
from utils.expr import ExprVisitor  as _ExprVisitor
from utils.expr import Binary       as _Binary
from utils.expr import Call         as _Call
from utils.expr import Get          as _Get
from utils.expr import Set          as _Set
from utils.expr import Function     as _Function
from utils.expr import This         as _This
from utils.expr import Super        as _Super
from utils.expr import Conditional  as _Conditional
from utils.expr import Logical      as _Logical
from utils.expr import Grouping     as _Grouping
from utils.expr import Unary        as _Unary
from utils.expr import Literal      as _Literal

from utils.reporter import runtimeError      as _RuntimeError
from utils.reporter import BreakException    as _BreakException
from utils.reporter import ReturnException   as _ReturnException

from utils.tokens import Token        as _Token
from utils.tokens import TokenType    as _TokenType

from utils.stmt import Stmt           as _Stmt
from utils.stmt import Var            as _Var
from utils.stmt import Const          as _Const
from utils.stmt import Import         as _Import
from utils.stmt import If             as _If
from utils.stmt import While          as _While
from utils.stmt import Break          as _Break
from utils.stmt import Func           as _Func
from utils.stmt import Class          as _Class
from utils.stmt import Block          as _Block
from utils.stmt import Return         as _Return
from utils.stmt import StmtVisitor    as _StmtVisitor
from utils.stmt import Del            as _Del
from utils.stmt import Print          as _Print
from utils.stmt import Expression     as _Expression

from utils.env import Environment     as _Environment

from native.datastructs.rocketClass import RocketCallable  as _RocketCallable
from native.datastructs.rocketClass import RocketFunction  as _RocketFunction
from native.datastructs.rocketClass import RocketClass     as _RocketClass
from native.datastructs.rocketClass import RocketInstance  as _RocketInstance

from core.scanner import Scanner as _Scanner

from core.parser  import Parser  as _Parser

from native.functions import localdefs    as _locals
from native.functions import clock       as _clock
from native.functions import rights      as _copyright
from native.functions import natives     as _natives
from native.functions import read        as _input
from native.functions import random      as _random
from native.functions import output      as _output
from native.functions import kind        as _kind

from native.datastructs import rocketList    as _rocketList
from native.datastructs import rocketArray   as _rocketArray

from native.datatypes import rocketString    as _rocketString
from native.datatypes import rocketNumber    as _rocketNumber
from native.datatypes import rocketBoolean   as _rocketBoolean

from utils.misc import importCodeStmts   as _importCodeStmts 

# to assert rocket datatypes
from utils.misc import isType              as _isType

# Array arithmetic fns
from utils.misc import opOverArray        as _opOverArray
from utils.misc import addArrays          as _addArrays


class Interpreter(_ExprVisitor, _StmtVisitor):
    def __init__(self, KSL: list):
        self.globals = _Environment() # For the native functions
        self.environment = _Environment() # Functions / classes
        self.locals = {}
        self.errors = []
        self.KSL = KSL
        self.stackCount = 0 # tracks stmt repetitions, 'stackoverflow' errs
        self.fnCallee = None # Tracks current fn callee

        # Statically define 'native' functions
        # random n between '0-1' {insecure}
        self.globals.define(_random.Random().callee,             _random.Random)
        # print (escaped) output. i.e print("hello\tmr.Jim") -> "Hello	mr.Jim"
        self.globals.define(_output.Print().callee,               _output.Print)
        # grab user input
        self.globals.define(_input.Input().callee,                 _input.Input)
        # 'locals' return all globally defined 'vars' and 'consts'
        self.globals.define(_locals.Locals().callee,             _locals.Locals)
        # 'clock'
        self.globals.define(_clock.Clock().callee,                 _clock.Clock)
        # 'copyright'
        self.globals.define(_copyright.Copyright().callee, _copyright.Copyright)
        # 'natives' -> names of nativr functions
        self.globals.define(_natives.Natives().callee,         _natives.Natives)
        # 'type' -> check datatype
        self.globals.define(_kind.Type().callee,                     _kind.Type)

        # Datatypes
        self.globals.define(_rocketList.List().callee,         _rocketList.List)
        self.globals.define(_rocketArray.Array().callee,     _rocketArray.Array)
        self.globals.define(_rocketString.String().callee, _rocketString.String)
        self.globals.define(_rocketNumber.Int().callee,       _rocketNumber.Int)
        self.globals.define(_rocketNumber.Float().callee,   _rocketNumber.Float)
        self.globals.define(_rocketBoolean.Bool().callee,   _rocketBoolean.Bool)

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

            if not (hasattr(error, 'willDup')):
                self.errors.append(error)

            else:
                if not error.willDup: self.errors.append(error)

    def visitLiteralExpr(self, expr: _Literal):
        if type(expr.value) == int:
            return _rocketNumber.Int().call(self, [expr.value])

        if type(expr.value) == float:
            return _rocketNumber.Float().call(self, [expr.value])

        if type(expr.value) == str:
            return _rocketString.String().call(self, [expr.value])

        if type(expr.value) == bool:
            return _rocketBoolean.Bool().call(self, [expr.value])

        return expr.value

    def visitGroupingExpr(self, expr: _Grouping):
        return self.evaluate(expr.expression)

    def visitUnaryExpr(self, expr: _Unary):
        right = self.sanitizeNum(self.evaluate(expr.right))

        # Handle '~' bit shifter
        if (expr.operator.type == _TokenType.TILDE):
            self.checkNumberOperand(expr.operator, right.value)
            sum = -right.value - 1
            return _rocketNumber.Int().call(self, [sum]) if type(sum) == int else _rocketNumber.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.MINUS):
            self.checkNumberOperand(expr.operator, right.value)
            sum = -right.value
            return _rocketNumber.Int().call(self, [sum]) if type(sum) == int else _rocketNumber.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.BANG):
            return not (self.isTruthy(right.value))

        # If can't be matched return nothing
        return None

    def visitBinaryExpr(self, expr: _Binary):
        # Sanitize to get nums if avail
        left = self.sanitizeNum(self.evaluate(expr.left))
        right = self.sanitizeNum(self.evaluate(expr.right))

        # Catches all ops over an Array with a num
        # That is '+', '-', '*', '/', '//', '%', '**'
        if (expr.operator.lexeme in ['+', '-', '*', '/', '//', '%', '**']):
            if (self.isRocketArray(left)) and (self.isRocketNumber(right)):
                if (self.isNumberArray(left)) and not left.isEmpty:
                    return _rocketArray.Array().call(self, _opOverArray(left, right, self.sanitizeNum, expr.operator.lexeme))

                else:
                    raise _RuntimeError(expr.operator, "Array must contain Number elements.", False)

            if (self.isRocketArray(right)) and (self.isRocketNumber(left)):
                if (self.isNumberArray(right)) and not right.isEmpty:
                    return _rocketArray.Array().call(self, _opOverArray(right, left, self.sanitizeNum, expr.operator.lexeme))

                else:
                    raise _RuntimeError(expr.operator, "Array must contain Number elements.", False)

        # overloaded operator '+' that performs:
        # basic arithmetic addition (between numbers)
        # string and implicit concatenation, i.e. String + [other type] = String
        # list concatenation, i.e. [4,2,1] + [4,6] = [4,2,1,4,6]
        # Array addition, i.e. [4,3,5] + [3,1,0] = [7,4,5]
        if (expr.operator.type == _TokenType.PLUS):
            # basic arithmetic addition
            if self.is_number(left) and self.is_number(right):
                sum = left.value + right.value
                return _rocketNumber.Int().call(self, [sum]) if type(sum) == int else _rocketNumber.Float().call(self, [sum])

            # String concatenation
            if (isinstance(left, _rocketString.RocketString) and isinstance(right, _rocketString.RocketString)):
                return _rocketString.String().call(self, [str(left.value) + str(right.value)])

            # To support implicit string concactination
            # E.g "Hailey" + 4 -> "Hailey4"
            # No need to allow this anymore. We make 'String' compulsory
            if ((isinstance(left, _rocketString.RocketString)) or (isinstance(right, _rocketString.RocketString))):
                # Concatenation of 'nin' is prohibited!
                if (type(left) == type(None)) or (type(right) == type(None)):
                    raise _RuntimeError(expr.operator.lexeme, "Operands must be either both strings or both numbers.", False)

                return _rocketString.String().call(self, [self.sanitizeString(left) + self.sanitizeString(right)])

            # allow python style list concatenation
            if (isinstance(left, _rocketList.RocketList) or isinstance(right, _rocketList.RocketList)):
                concat_tok = _Token(_TokenType.STRING, 'concat', 'concat', 0)

                # return new concatenated list
                return left.get(concat_tok).call(self, [right])

            if (self.isRocketArray(left)) and (self.isRocketArray(right)):
                if (self.isNumberArray(left) and self.isNumberArray(right)) and not (left.isEmpty or right.isEmpty):
                    return _rocketArray.Array().call(self, _addArrays(left, right, self.sanitizeNum))

                else:
                    raise _RuntimeError(expr.operator, "Cannot concat empty Array(s).", False)

            if (type(left) == type(None)) or (type(right) == type(None)):
                raise _RuntimeError(expr.operator, "Operands must be either both strings or both numbers.", False)

        # Arithmetic operators "-", "/", "%", "//", "*", "**"
        if (expr.operator.type == _TokenType.MINUS):
            self.checkNumberOperands(expr.operator, left, right)
            sum = left.value - right.value
            return _rocketNumber.Int().call(self, [sum]) if type(sum) == int else _rocketNumber.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.DIV):
            self.checkNumberOperands(expr.operator, left, right)
            if right.value == 0:
                raise _RuntimeError(right, "ZeroDivError: Can't divide by zero", False)

            sum = left.value / right.value
            return _rocketNumber.Int().call(self, [sum]) if type(sum) == int else _rocketNumber.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.MOD):
            self.checkNumberOperands(expr.operator, left, right)
            if right.value == 0:
                raise _RuntimeError(right, "ZeroDivError: Can't divide by zero", False)

            sum = left.value % right.value
            return _rocketNumber.Int().call(self, [sum]) if type(sum) == int else _rocketNumber.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.FLOOR):
            self.checkNumberOperands(expr.operator, left, right)
            if right.value == 0:
                raise _RuntimeError(right, "ZeroDivError: Can't divide by zero", False)

            sum = left.value // right.value
            return _rocketNumber.Int().call(self, [sum]) if type(sum) == int else _rocketNumber.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.MULT):
            self.checkNumberOperands(expr.operator, left, right)
            sum = left.value * right.value
            return _rocketNumber.Int().call(self, [sum]) if type(sum) == int else _rocketNumber.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.EXP):
            self.checkNumberOperands(expr.operator, left, right)
            sum = left.value ** right.value
            return _rocketNumber.Int().call(self, [sum]) if type(sum) == int else _rocketNumber.Float().call(self, [sum])

        # bitshifters "<<", ">>"
        if (expr.operator.type == _TokenType.LESS_LESS):
            self.checkNumberOperands(expr.operator, left, right)
            sum = left.value * (2 ** right.value)
            return _rocketNumber.Int().call(self, [sum]) if type(sum) == int else _rocketNumber.Float().call(self, [sum])

        if (expr.operator.type == _TokenType.GREATER_GREATER):
            self.checkNumberOperands(expr.operator, left, right)
            sum = left.value // (2 ** right.value)
            return _rocketNumber.Int().call(self, [sum]) if type(sum) == int else _rocketNumber.Float().call(self, [sum])

        # Comparison operators ">", "<", ">=", "<=", "!=", "=="
        if (expr.operator.type == _TokenType.GREATER):
            self.checkNumberOperands(expr.operator, left, right)
            return left.value > right.value

        if (expr.operator.type == _TokenType.LESS):
            self.checkNumberOperands(expr.operator, left, right)
            return left.value < right.value

        if (expr.operator.type == _TokenType.GREATER_EQUAL):
            self.checkNumberOperands(expr.operator, left, right)
            return left.value >= right.value

        if (expr.operator.type == _TokenType.LESS_EQUAL):
            self.checkNumberOperands(expr.operator, left, right)
            return left.value <= right.value

        if (expr.operator.type == _TokenType.BANG_EQUAL):
            self.checkValidOperands(expr.operator, left, right)
            return not (self.isEqual(left, right))

        if (expr.operator.type == _TokenType.EQUAL_EQUAL):
            if left == None or right == None:
                return self.isEqual(left, right)

            if isinstance(left, _rocketBoolean.Bool) or isinstance(right, _rocketBoolean.Bool):
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

        # Well, native functions in 'native/' have a special 'nature' field to distinguish them from user defined funcs.
        isNotNative = True
        isNotDatatype = True
        overideArity = False # To allow (near) infinite 'arity' for 'List' elements

        try:
            if callee().nature == "native":
                if self.isRocketFlatList(callee()):
                    overideArity = True

                isNotNative = False
        except:
            if hasattr(callee, 'nature'):
                isNotDatatype = False

        # Specially inject check for 'rocketClass' and 'rocketCallable'
        isNotCallable = not self.isRocketCallable(callee) #isinstance(callee, _RocketCallable)
        isNotClass = not self.isRocketClass(callee) # isinstance(callee, _RocketClass)

        if isNotCallable and isNotClass and isNotNative and isNotDatatype:
            raise _RuntimeError(expr.paren, "Can only call functions and classes", False)

        function = callee if isNotNative else callee()

        # Special edge case for 'Print' fn
        # It allows for near infinite args
        if (hasattr(function, 'nature')):
            # We have to be sure its a native fn not some class or something
            if (function.nature == 'native'):
                if (function.callee == 'Print'):
                    overideArity = True

        # We dynamically change 'arity' for List's 'slice' fn depending on the args
        if not isNotDatatype:
            if hasattr(function, 'signature') and (hasattr(function, 'slice') or hasattr(function, 'splice')):
                if ((function.signature == 'String') or (function.signature == 'List')) and (len(eval_args) == 2):
                    function.inc = True

        if hasattr(function, 'slice') or hasattr(function, 'splice'):
            if len(eval_args) != function.arity(function.inc):
                raise _RuntimeError(expr.callee.name.lexeme, f"Expected '{function.arity(function.inc)}' args but got '{len(eval_args)}.'", False)

        else:
            if len(eval_args) != function.arity() and not overideArity:
                raise _RuntimeError(expr.callee.name.lexeme, f"Expected '{function.arity()}' args but got '{len(eval_args)}.'", False)

        if hasattr(function, 'inc'):
            return function.call(self, eval_args, function.inc)

        if overideArity:
            return function.call(self, eval_args)

        else:
            try:
                if (hasattr(expr.callee, 'name')):
                    # fns do not have 'name' so be careful
                    # Monitor recursive calls to same function
                    # set current function
                    if (self.stackCount == 66):
                        # Reset counter
                        self.stackCount = 0

                        raise _RuntimeError(expr.callee.name.lexeme, f"Maximum recursion depth reached from calls to '{expr.callee.name.lexeme}' fn.", False)

                    # We increment our stack counter if same fn called from previous call
                    if (self.fnCallee == expr.callee.name.lexeme):
                        self.stackCount += 1

                    # Set new fn callee
                    else:
                        self.fnCallee = expr.callee.name.lexeme

                return self.sanitizeNum(function.call(self, eval_args))

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
            raise _RuntimeError(expr.name, "Only instances have properties.", False)

    def visitSetExpr(self, expr: _Set):
        obj = self.evaluate(expr.object)

        if hasattr(obj, 'kind'):
            if ('List' in obj.kind):
                raise _RuntimeError('List', f"Cannot assign external attribute to native datatype 'List'", False)

        if not isinstance(obj, _RocketInstance):
            raise _RuntimeError(expr.name, "Only instances have fields.", False)

        value = self.evaluate(expr.value)
        obj.set(expr.name, value)

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
            raise RuntimeError(expr.keyword, "Cannot find undefined method '{expr.method.lexeme}' in superclass", False)

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
                raise _RuntimeError(name, f"can't undefined name '{name}'", False)
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
        value = self.KSL[1][_TokenType.NIN.value] # Grab nin lexeme from the KSL

        if stmt.value != None:
            value = self.evaluate(stmt.value)

        raise _ReturnException(value)

    def visitImportStmt(self, stmt: _Import):
        import_lexeme = self.KSL[1][_TokenType.IMPORT.value]

        # TODO: add more native modules
        native_modules = [
            'math' # Note: even this module isn't done
        ]

        if len(stmt.modules) == 0:
            raise _RuntimeError(import_lexeme, f"{import_lexeme} statement requires atleast one module name.", False)

        for module in stmt.modules:
            if module.type == _TokenType.IDENTIFIER and module.lexeme in native_modules:
                # read and execute sorce file
                contents = ''

                # Get exec base home
                basehome = _os.path.dirname(_os.path.realpath(__file__))

                # Assemble native module path
                filename = _os.path.join(basehome, "native/modules/" + module.lexeme + '.rckt')

                stmts = _importCodeStmts(filename, self.KSL)

                self.interpret(stmts)

            else:
                try:
                    # read and execute sorce file
                    contents = ''

                    # This way the user can specify both './path/to/module.rckt' and './path/to/module' are valid
                    filename = (module.lexeme + '.rckt') if module.lexeme.split(_os.path.extsep)[-1] != 'rckt' else module.lexeme

                    stmts = _importCodeStmts(filename, self.KSL)

                    self.interpret(stmts)

                except FileNotFoundError:
                    raise _RuntimeError(import_lexeme, f"No native or local module named '{module.lexeme}'.", False)

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

        # To avoid redifining vars with the same name as consts, functions, or classes
        if not (self.globals.isTaken(stmt.name)):
            self.environment.define(stmt.name.lexeme, value)

        else:
            raise _RuntimeError(stmt.name.lexeme, "Name already defined as 'class' or 'function'", False)

    def visitConstStmt(self, stmt: _Const):
        value = self.evaluate(stmt.initializer)

        # check for variable before definition to avoid passing in 'const' redefinitions
        if self.environment.constExists(stmt.name):
            raise _RuntimeError(stmt.name.lexeme, "Name already used as const.", False)

        if self.environment.varExists(stmt.name):
            raise _RuntimeError(stmt.name.lexeme, "Name already used as variable.", False)

        # stop 'const' re-decl for 'classes' 'functions'
        elif self.globals.isTaken(stmt.name):
            raise _RuntimeError(stmt.name.lexeme, "Name already used as 'class' or 'function' name.", False)

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
                raise _RuntimeError(stmt.superclass.name, "Superclass must be a class.", False)

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
                    raise _RuntimeError(expr.name, "cannot perform arithmetic increment on string.", False)

                value = _rocketNumber.Int().call(self, [init_value.value + 1]) if type(init_value.value) == int else _rocketNumber.Float().call(self, [init_value.value + 1])

                self.environment.assign(expr.name, value)

                # I.e :-
                #       var p = 2;
                #       print p++; /// returns '2'
                return init_value

            # For our decrement post fix operator '--'
            if expr.value[2] == 'dec':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform arithmetic decrement on string.", False)

                value = _rocketNumber.Int().call(self, [init_value.value - 1]) if type(init_value) == int else _rocketNumber.Float().call(self, [init_value.value - 1])

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
                value = _rocketNumber.Int().call(self, [value]) if type(value) == int else _rocketNumber.Float().call(self, [value])

                self.environment.assign(expr.name, value)

                return value

            # Check for '-='
            if expr.value[2] == 'sub':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform subtraction arithmetic assignment on string.", False)

                value = init_value.value - var_value
                value = _rocketNumber.Int().call(self, [value]) if type(value) == int else _rocketNumber.Float().call(self, [value])

                self.environment.assign(expr.name, value)

                return value

            # Check for '*='
            if expr.value[2] == 'mul':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform multiplication arithmetic assignment on string.", False)

                value = init_value.value * var_value
                value = _rocketNumber.Int().call(self, [value]) if type(value) == int else _rocketNumber.Float().call(self, [value])

                self.environment.assign(expr.name, value)

                return value

            # Check for '/='
            if expr.value[2] == 'div':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform division arithmetic assignment on string.", False)

                value = init_value.value / var_value
                value = _rocketNumber.Int().call(self, [value]) if type(value) == int else _rocketNumber.Float().call(self, [value])

                self.environment.assign(expr.name, value)

                return value

            # Check for '//='
            if expr.value[2] == 'flo':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform floor division arithmetic assignment on string.", False)

                value = init_value.value // var_value
                value = _rocketNumber.Int().call(self, [value]) if type(value) == int else _rocketNumber.Float().call(self, [value])

                self.environment.assign(expr.name, value)

                return value

            # Check for '%='
            if expr.value[2] == 'mod':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform modulo arithmetic assignment on string.", False)

                value = init_value.value % var_value
                value = _rocketNumber.Int().call(self, [value]) if type(value) == int else _rocketNumber.Float().call(self, [value])

                self.environment.assign(expr.name, value)

                return value

            # Check for '**='
            if expr.value[2] == 'exp':
                if type(init_value) == str:
                    raise _RuntimeError(expr.name, "cannot perform exponent arithmetic assignment on string.", False)

                value = init_value.value ** var_value
                value = _rocketNumber.Int().call(self, [value]) if type(value) == int else _rocketNumber.Float().call(self, [value])

                self.environment.assign(expr.name, value)

                return value

            ### END of assignment arithmetic ops

        else:
            value = self.evaluate(expr.value)

            try:
                self.environment.assign(expr.name, value)

            except _RuntimeError as error:
                if ('ReferenceError:' in error.msg) or ('AssignmentError: ' in error.msg):
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
                print(err, file=_sys.stderr)
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
        # get values
        if (hasattr(left_obj, 'value')):
            left_obj = left_obj.value

        if (hasattr(right_obj, 'value')):
            right_obj = right_obj.value

        if ((left_obj == None) and (right_obj == None)):
            return True

        # Nothing but "nin" (None) is equal to it
        if (left_obj == None):
            return False

        return left_obj == right_obj

    def sanitizeNum(self, n):
        # Returns a Rocket num if number received
        if (self.is_number(n)):
            if (isinstance(n, int)):
                return _rocketNumber.Int().call(self, [n])
            
            if (isinstance(n, float)):
                return _rocketNumber.Float().call(self, [n])

        # otherwise it returns it unchanged
        return n

    def sanitizeString(self, n):
        # NOTE: All datatypes must have this method
        return n.raw_string()

    def is_number(self, obj: object):
        if (type(obj) in [int, float, _rocketNumber.RocketInt, _rocketNumber.RocketFloat]):
            return True

        else:
            return False

    def checkNumberOperand(self, operator: _Token, right: object):
        if self.is_number(right): return

        raise _RuntimeError(operator.lexeme, "Operand must be number.", False)

    def checkNumberOperands(self, operator: _Token, left: object, right: object):
        if self.is_number(left) and self.is_number(right): return

        raise _RuntimeError(operator.lexeme, "Operands must be numbers.", False)

    def checkValidOperands(self, operator: _Token, left: object, right: object):
        if ((isinstance(left, str)) and (isinstance(right, str))): return

        if self.is_number(left) and self.is_number(right): return

        else:
            # Is comparing strings and numbers really important?
            # Maybe if you are trying to see if a number id transformed to an 'str'.
            # But wouldn't you just check the type with 'Type' native func?!
            raise _RuntimeError(operator.lexeme, "operands must both be either 'strings' or 'numbers'.", False)

    def stringify(self, value: object):
        # Customize literals
        nin_lexeme = self.KSL[1][_TokenType.NIN.value]

        if (value == None) or value == nin_lexeme: return nin_lexeme, "\033[1m"

        # HACK: Against bug #28 'print 0;' -> false && 'print 1;' -> true
        if (value == True and type(value) == bool): return "true", "\033[1m"
        if (value == False and type(value) == bool): return "false", "\033[1m"

        if isinstance(value, _rocketString.RocketString):
            if value == '':
                return value, None

            return value, "\033[32m"

        elif isinstance(value, _rocketNumber.RocketInt) or isinstance(value, _rocketNumber.RocketFloat):
            return value, "\033[36m"

        else:
            try:
                if (value().nature == "native"):
                    return value(), None

            except:
                return value, None

        # Child fns

    def isRocketArray(self, obj):
        return _isType(obj, _rocketArray.RocketArray)

    def isRocketList(self, obj):
        return _isType(obj, _rocketList.RocketList)

    def isRocketFlatList(self, obj):
        return _isType(obj, _rocketArray.Array) or _isType(obj, _rocketList.List)

    def isRocketClass(self, obj):
        return _isType(obj, _RocketClass)

    def isRocketClassInst(self, obj):
        return _isType(obj, _RocketInstance)

    def isRocketCallable(self, obj):
        return _isType(obj, _RocketCallable)

    def isRocketString(self, obj):
        return _isType(obj, _rocketString.RocketString)

    def isRocketInt(self, obj):
        return _isType(obj, _rocketNumber.RocketInt)

    def isRocketFloat(self, obj):
        return _isType(obj, _rocketNumber.RocketFloat)

    def isNumberArray(self, obj):
        return (obj.arrayType == _rocketNumber.RocketFloat) or (obj.arrayType == _rocketNumber.RocketInt)

    def isRocketNumber(self, obj):
        return _isType(obj, _rocketNumber.RocketFloat) or _isType(obj, _rocketNumber.RocketInt)

    def isRocketBool(self, obj):
        return _isType(obj, _rocketBoolean.RocketBool)
