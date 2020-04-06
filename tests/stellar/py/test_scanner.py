# Author: Abubakar Nur Khalil
# License: MIT
# Purpose: Test tokens output from Scanner

from core.scanner import Scanner

from tools.custom_syntax import Scanner as _Virgil
from tools.custom_syntax import Parser  as _Dante

# Again, we need to first generate the KSL then pass it along
KSL = _Dante(_Virgil('').scan()).parse()

source = """/// None of this would show
var name = 'ank';
"""

print("Source code\n==========\n")
print(source, end="\n")

rover = Scanner(source, KSL[0])

def dump(tokens):
	for token in tokens:
		print(token.toString())


tokens = rover.scan()

print("\nTokens\n======\n")
dump(tokens)
