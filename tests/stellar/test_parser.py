# Author: Abubakar NK
# License: MIT
# Purpose: Appropriate parsed output from Parser

from utils.tokens import TokenType
from scanner import Scanner
from parser import Parser

source = """
var name = "ank";
77.67 * (8 // 2);
"""

tks = Scanner(source).scan()

pr = Parser(tks)

print(pr.check(TokenType.VAR))
