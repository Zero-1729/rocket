from utils.tokens import TokenType
from scanner import Scanner
from parser import Parser
from tools.printer import dump_tokens


source = """
var name = "ank";
77.67 * (8 // 2);
"""

tks = Scanner(source).scan()

pr = Parser(tks)

print(pr.check(TokenType.VAR))
