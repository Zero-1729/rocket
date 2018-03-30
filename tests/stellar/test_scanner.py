/* Author: Abubakar NK
** License: MIT
** Purpose: Proper tokens output from Scanner*/


from scanner import Scanner, Token

source = """// None of this would show
var name = 'ank';
"""

print("Source code\n==========\n")
print(source, end="\n\n")

rover = Scanner(source)

def dump(tokens):
	for token in tokens:
		print(token.toString())


tokens = rover.scan()

print("\nTokens\n======\n")
dump(tokens)