import os
import sys

from tokens import Token


def usage():
    print("genast <out directory>")

def format_fields(fields):
    tmp = fields.split(', ')
    f = '' # final output string

    # loop through field and format it properly
    for t in tmp:
        d = t.split(' ') # ['Expr', 'left']
        d = [d[-1], d[0]] # ['left', 'Expr']
        d = ': '.join(d) # 'left: Expr'

        f = f + (d + ', ')

    f = f[:-2]

    return f


def getNames(fields):
    tmp = fields.split(', ')
    names = []

    for t in tmp:
        name = t.split(':')[0]
        names.append(name)

    return names


def defineAst(out, baseName, types):
    filename = (baseName[0].lower() + baseName[1:])  + '.py'
    filename = os.path.join(out, filename)

    className = baseName
    exprClassNames = [t for t in types]

    with open(filename, "w") as f:
        f.write(f"from tokens import Token\n\n\n")

        f.write(f"class Object(object):\n\tpass\n\n\n")

        f.write(f"class Visitor:")

        for name in exprClassNames:
            f.write(f"\n\tdef visit{name}{baseName}(self, expr):")
            f.write(f"\n\t\traise NotImplementedError\n")

        f.write("\n\n")

        f.write(f"class {className}:")
        f.write(f"\n\tdef accept(visitor: Visitor):")
        f.write(f"\n\t\traise NotImplementedError\n\n\n")

        for t in types:
            className = t
            fields = format_fields(types[t])
            field_names = getNames(fields)

            f.write(f"class {className}:")
            f.write(f"\n\tdef __init__(self, {fields}):")

            for fn in field_names:
                f.write(f"\n\t\tself.{fn} = {fn}")

            f.write("\n\n\tdef accept(self, Visitor: Visitor):")
            f.write(f"\n\t\treturn Visitor.visit{className}{baseName}(self)")

            f.write("\n\n\n")

        f.close()


def main():
    if len(sys.argv) == 2:
        out = os.path.join(sys.argv[1])

        types = {
                "Binary": "Expr left, Token operator, Expr right",
                "Grouping": "Expr expression",
                "Literal": "Object value",
                "Unary": "Token operator, Expr right"
        }

        defineAst(out, "Expr", types)

    else:
        usage()


if __name__ == "__main__":
    main()
