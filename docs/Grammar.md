# Rocket Lang Grammar :bowtie:

## Notation notes

*Capitalization indicates terminals that are single lexemes of varying types*

+ `→`       :- operand for production declaration; `production` (left) & `definition` (RIGHT).
+ `...`     :- signifies a range.
+ `|`       :- separator indicating optionality (serves as `OR`).
+ `(` `)`   :- used to group items.
+ `;`       :- signifies end of grammar definition.
+ `+`       :- indicates a production can appear at least once.
+ `*`       :- indicates multiple reuse of an item or items.
+ `?`       :- indicates a production is optional; can appear once or not at all.

---

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

class_decl      → "class" IDENTIFIER ("<" IDENTIFIER)? "{" function* "}" ;

func_decl       → "func" function ;

var_decl        → "var" ( single_var_decl | "{" single_var_decl* "}" ";"? ) ;
const_decl      → "const" ( single_const_decl | "{" single_const_decl* "}" ";"? ) ;

single_var_decl   → IDENTIFIER "=" expression ";" ;
single_const_decl → IDENTIFIER ( "=" expression )? ";" ;
```

## Expressions

```rocket
expression  → assignment ;

assignment  → ( call "." )? IDENTIFIER "=" assignment | logic_or ;

logic_or    → logic_and ( "or" logic_and )* ;
logic_and   → conditional  ( "and" conditional )* ;
conditional → equality ( "?" equality : conditional )? ;
equality    → comparison ( ( "!=" | "==" ) comparison )* ;
comparison  → addition ( ( ">" | ">=" | "<" | "<=" ) addition)* ;
addition    → mult ( ( "-" | "+" | "<<" | ">>" ) mult )* ;
mult        → unary ( ( "/" | "//" | "%" | "*" | "**" ) unary )* ;
unary       → ( "~" | "!" | "-" ) unary | call ;
call        → primary ( "(" arguments? ")" | "." IDENTIFIER )* ;
arrow_func  → "(" arguments ")" "=>" block ;
postfix     → primary ( "--" | "++" ) ;
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
                | import_stmt
                | block ;

print_stmt       → "print" expression ;
expr_stmt        → expression ;
if_stmt          → "if" "(" expression ")" statement ( "else" statement )? ;
for_stmt         → "for" "(" ( var_decl | expr_stmt | ";" ) expression? ";" expression? ")" statement ;
while_stmt       → "while" "(" expression ")" statement ;
break_stmt       → "break" ";" ;
return_stmt      → "return" expression? ";" ;
del_stmt         → "del" IDENTIFIER ( ( "," IDENTIFIER )* )? ";" ;
import_stmt      → "import" ( "(" IDENTIFIER*  ")" | IDENTIFIER ) ;
block            → "{" declaration* "}" ;
```

## Utility Rules
```
function        → IDENTIFIER? "(" parameters? ")" block ;
parameters      → IDENTIFIER ( "," IDENTIFIER )* ;
arguments       → expression ( "," expression )* ;
```

## Lexical Grammar

```
STRING          → ('"' <char except '"'>* '"') | ("'" <char except "'"> "'") ;
IDENTIFIER     → ALPHA ( ALPHA | DIGIT )* ; // I.e '8bit' not allowed
ALPHA           → 'a' ... 'z' | 'A' ... 'Z' | '_' ;
NUMBER          → INT | FLOAT ;
FLOAT           → (INT)+ "." (INT)+ ;
INT             → ('0' ... '9')+ ;
```
