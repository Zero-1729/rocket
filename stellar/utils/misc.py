# Utilities fns to reduce code redundancy
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

