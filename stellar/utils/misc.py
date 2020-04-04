# if p is negative then
# (p * -1) - p will be equal to twice the absolute value of p (aka |p| ** 2), where x != 0
#
# Proof:
#   Assume x = -x
#
#   (-x * -1) - (-x)
#   = x - (-x)
#   = x + x
#   2x (hence |x| * 2)
#
# Now assume x = x
#
#       (x * -1) - (x)
#       -x - x
#       -2x (hence -|x| * 2 and not |x| * 2)
#
# QED
def isValNeg(x):
    return (((x * -1) - x) == 2 * abs(x)) and (not x == 0)