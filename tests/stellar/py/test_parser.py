# Author: Abubakar Nur Khalil
# License: MIT
# Purpose: Appropriate parsed output from Parser

from utils.tokens import TokenType

from core.scanner import Scanner
from core.parser import Parser

from tools.custom_syntax import Scanner as _Virgil
from tools.custom_syntax import Parser  as _Dante

# Remember we always need to generate the KSL first and pass it over
KSL = _Dante(_Virgil('').scan()).parse()

source = """
var name = "ank";
77.67 * (8 // 2);
"""

print('Source code:')
print(source)

tks = Scanner(source, KSL[0]).scan()

pr = Parser(tks, KSL[1])

print("\nFirst Token is variable (VAR):", pr.check(TokenType.VAR)) # True
