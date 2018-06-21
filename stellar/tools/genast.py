import os
import sys


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
        if baseName == "Stmt":
            f.write("from expr import Expr as _Expr\n")

        f.write("from tokens import Token as _Token\n\n\n")

        f.write(f"class {baseName}Visitor:")

        for name in exprClassNames:
            field = baseName[0].lower() + baseName[1:]
            f.write(f"\n\tdef visit{name}{baseName}(self, {field}):")
            f.write(f"\n\t\traise NotImplementedError\n")

        f.write("\n\n")

        f.write(f"class {className}:")
        f.write(f"\n\tdef accept(visitor: {baseName}Visitor):")
        f.write(f"\n\t\traise NotImplementedError\n")
        f.write("\n\tdef parent(self):")
        f.write(f"\n\t\treturn '{baseName}'\n\n\n")

        globalClass = className

        for t in types:
            className = t
            formated_fields = format_fields(types[t])
            fields = formated_fields if formated_fields != ': ' else None
            field_names = getNames(fields) if fields else None

            f.write(f"class {className}({globalClass}):")

            if ((fields) and (field_names)):
                f.write(f"\n\tdef __init__(self, {fields}):")

                for fn in field_names:
                    f.write(f"\n\t\tself.{fn} = {fn}")

            f.write(f"\n\n\tdef accept(self, visitor: {baseName}Visitor):")
            f.write(f"\n\t\treturn visitor.visit{className}{baseName}(self)")

            f.write("\n\n\n")

        f.close()


def main():
    if len(sys.argv) == 2:
        out = os.path.join(sys.argv[1])

        types = {
                "Assign": "_Token name, Expr value",
                "Binary": "Expr left, _Token operator, Expr right",
                "Call": "Expr callee, _Token paren, list args",
                "Get": "Expr object, _Token name",
                "Set": "Expr object, _Token name, Expr value",
                "Super": "_Token keyword, _Token method",
                "This": "_Token keyword",
                "Function": "list params, list body",
                "Grouping": "Expr expression",
                "Logical": "Expr left, _Token operator, Expr right",
                "Literal": "object value",
                "Unary": "_Token operator, Expr right",
                "Variable": "_Token name"
        }

        defineAst(out, "Expr", types)

        types_two = {
            "Block": "list statements",
            "Expression": "_Expr expression",
            "Print": "_Expr expression",
            "Class": "_Token name, _Expr superclass, list methods",
            "Func": "_Token name, _Expr function",
            "Var": "_Token name, _Expr initializer",
            "Const": "_Token name, _Expr initializer",
            "If": "Stmt condition, Stmt thenBranch, Stmt elseBranch",
            "While": "_Expr condition, Stmt body",
            "Break": "",
            "Return": "_Token keyword, _Expr value",
            "Del"  : "list names"
        }

        defineAst(out, "Stmt", types_two)

    else:
        usage()


if __name__ == "__main__":
    main()
