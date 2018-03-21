# Rocket Lang Grammar :bowtie:

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
                  | const_decl
                  | statement ;

class_decl      → "class" IDENTIFIER ( "<-" IDENTIFIER )? "{" function* "}" ;
func_decl       → "func" function ;
var_decl        → "var" IDENTIFIER ( "=" expression )? ";" ;
const_decl      → "const" IDENTIFIER "=" expression ";" ;
```

## Expressions

```rocket
expression  → assignment ;

assignment  → ( call "." )? IDENTIFIER "=" assignment | logic_or ;

logic_or    → logic_and ( "or" logic_and )* ;
logic_and   → equality  ( "and" equality )* ;
equality    → comparison ( ( "!=" | "==" ) comparison )* ;
comparison  → addition ( ( ">" | ">=" | "<" | "<=" ) addition)* ;
addition    → mult ( ( "-" | "+" | "<<" | ">>" ) mult )* ;
mult        → unary ( ( "/" | "//" | "%" | "*" | "**" ) unary )* ;
unary       → ( "~" | "!" | "-" ) unary | call ;
call        → primary ( "(" arguments? ")" | "." IDENTIFIER )* ;
primary     → "true" | "false" | "nin" | "this" | NUMBER | STRING | IDENTIFIER | "(" expression ")" | "super" "." IDENTIFIER ;
```

## Statements

```rocket
statement       → print_stmt
                | expr_stmt
                | if_stmt
                | for_stmt
                | while_stmt
                | break_stmt
                | return_stmt
                | del_stmt
                | block ;

print_stmt       → "print" expression ;
expr_stmt        → expression ;
if_stmt          → "if" "(" expression ")" statement ( "else" statement )? ;
for_stmt         → "for" "(" ( var_decl | expr_stmt | ";" ) expression? ";" expression? ")" statement ;
while_stmt       → "while" "(" expression ")" statement ;
break_stmt       → "break" ";" ;
return_stmt      → "return" expression? ";" ;
del_stmt         → "del" IDENTIFIER ( ( "," IDENTIFIER )* )? ";" ;
block            → "{" declaration* "}" ;
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
STRING          → ('"' <char except '"'>* '"') | ("'" <char except "'"> "'") ;
INDENTIFIER     → ALPHA ( ALPHA | DIGIT )* ; // I.e '8bit' not allowed
ALPHA           → 'a' ... 'z' | 'A' ... 'Z' | '_' ;
DIGIT           → '0' ... '9' ;
```
