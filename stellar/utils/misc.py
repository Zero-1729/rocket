# Utilities fns to reduce code redundancy
from core.scanner import Scanner as _Scanner
from core.parser  import Parser  as _Parser


# Integer Negativity test
def isValNeg(x):
    # Preamble:
    #
    #   if p is negative then
    #   (p * -1) - p will be equal to twice the absolute value of p (aka |p| ** 2), where x != 0
    #
    # Proof:
    #
    #   Assume x = -x    (negative)
    #
    #   (-x * -1) - (-x)
    #   = x - (-x)
    #   = x + x
    #   2x (hence |x| * 2)
    #
    #   Now assume x = x (positive)
    #
    #   (x * -1) - (x)
    #   -x - x
    #   -2x (hence -|x| * 2 and not |x| * 2)
    #
    # QED
    return (((x * -1) - x) == 2 * abs(x)) and (not x == 0)


# Used for code importing
def importCodeStmts(filename, KSL):
    # Reads the contents of a module and returns the stmts (parser output)
    module_contents = None

    with open(filename, 'r') as module:
        module_contents = module.read()
        module.close()

    tks = _Scanner(module_contents, KSL[0]).scan()
    stmts = _Parser(tks, KSL[1]).parse()

    return stmts


# Datatype assert fns
# master fn
def isType(obj, kind):
    return isinstance(obj, kind)


# check if a list of args are all of the same type
def isAllSameType(objs, kind):
    result = True

    for i in range(len(objs)):
        if not (isType(objs[i], kind) or (type(objs[i]) == type(None))):
            result = False

    return result


# array addition fn
def addArrays(left, right, sanitize):
    result = []

    # What about uneven array heights?
    for i in range(len(left.elements)):
        result.append(sanitize(left.elements[i].value + right.elements[i].value))

    return result

def doMath(left, right, op):
    return eval(f"{left} {op} {right}")

def opOverArray(arr, num, sanitize, op):
    result = []

    for i in range(len(arr.elements)):
        if type(arr.elements[i]) != type(None):
            result.append(sanitize(doMath(arr.elements[i].value, num.value, op)))

    return result