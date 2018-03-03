# Rocket Lang Grammar

---

> **Notation notes**

*Capaitalization indicates terminals that are single lexemes of a vary type*

+ `→`       :- operand for production declaration. `production` (left) & `ddefinition` (RIGHT)
+ `...`     :- signifies a range
+ `|`       :- separator indicating optionality. In place as `OR`
+ `(` `)`   :- used to group items
+ `;`       :- signifies end of grammar definition
+ `+`       :- indicates a production can appear at least once
+ `*`       :- indicates multiple reuse of an item or items
+ `?`       :- indicates a production is optional. Can appear once or not at all

## General Syntax Grammar
```rocket
program     → declaration* EOF ;
```

## Declarations
```rocket
declaration     → class_decl
                  | func_decl
                  | var_decl
                  | statement ;

class_decl      → "class" IDENTIFIER ( "<-" IDENTIFIER )? "{" function* "}" ;
func_decl       → "func" function ;
var_decl        → "var" IDENTIFIER ( "=" expression )? ";" ;
```

## Expressions

```rocket
expression  → assignment ;

assignment  → ( call "." )? IDENTIFIER "=" assignment | logic_or ;

logic_or    → logic_and ( "or" logic_and )* ;
logic_and   → equality  ( ) ;
```

## Statements

```rocket
statement       → printStmt
                | exprStmt
                | ifStmt
                | forStmt
                | whileStmt
                | returnStmt
                | block ;

printStmt       → "print" expression ;
exprStmt        → expression ;
ifStmt          → "if" "(" expression ")" statement ( "else" statement )? ;
forStmt         → "for" "(" ( var_decl | exprStmt ) expression? ";" expression? ")" statement ;
whileStmt       → "while" "(" expression ")" statement ;
block           → "{" declaration* "}" ;
```

## Utility Rules
```
function        → IDENTIFIER "(" parameters? ")" block ;
paremeters      → IDENTIFIER ( ", IDENTIFIER" )* ;
argumenrs       → expression ( "," expression )* ;
```

## Lexical Grammar

```
NUMBER          → DIGIT+ ( "." DIGIT+ )? ;
STRING          → '"' <char except '"'>* '"' ;
INDENTIFIER     → ALPHA ( ALPHA | DIGIT )* ;
ALPHA           → 'a' ... 'z' | 'A' ... 'Z' | '_' ;
DIGIT           → '0' ... '9' ;
```
