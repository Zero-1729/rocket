from tools.custom_syntax import Scanner as _Virgil

source = """
bake print
def func
"""

print('scanned: ')
print(source)

tks = _Virgil(source).scan() 

print('Got tokens:\n')

for i in range(len(tks)):
    print(f"[{i}] {tks[i]}")

"""
Output:

[0] TokenType.IDENTIFIER bake None
[1] TokenType.PRINT print None
[2] TokenType.IDENTIFIER def None
[3] TokenType.FUNC func None
[4] TokenType.EOF  None
"""