# The Rocket Language Specification

Language's Specification info.

## Table of Content

| No.   | Topic Name            |
|-------|-----------------------|
|  0.0  | [Hello World Example](#hello-world-example) :wave:                                   |
|  1.0  | [Dynamic Typing](#dynamic-typing) :abc:                                              |
|  2.0  | [Automatic Memory Management](#automated-memory-management) (GC) :articulated_lorry: |
|  3.0  | [Data Types](#data-types)                                                            |
|  4.0  | [Expressions](#expressions) :performing_arts:                                        |
|  5.0  | [Statements](#statements) :speech_balloon:                                           |
|  6.0  | [Variables](#variables)                                                              |
|  7.0  | [Control Flow](#control-flow) :ocean:                                                |    
|  8.0  | [Functions](#functions)                                                              |
|  9.0  | [Classes](#classes) (Yes there's OOP) :neckbeard:                                    |
|  x.x  | [The Standard Library](#the-standard-library) (or The Core Library) :file_folder:    |

---

### 0.0 Hello World Example

> **Note**: Although a `print` function would br added later on! :wink: <br>

*Because we believe language syntax should be clean as simple.*

```rocket
/// Print is a built-in command
print "Hello, World!";
```

> Note that in Rocket single line comments begin with `///` or `#` and multi-line comments are contained in `/**/` just like in C.  

---

### 1.0 Dynamic Typing :abc:

Rocket is Dynamically typed. Which means variables can store values of any type, and a single value of different types at different times. For Example:-

```Rocket
/// Initial value of type int
var number = 2;

/// Later value of type string
number = "2";

/// List containing values of various Types
var stuff = ["string", 87, 2334.72, ["empty"], {"message": "hi"}];
```

However, if an operation on values of the wrong (incompatible) type is performed - like, Dividing a value of the type `Number` by a `String` i.e. `2 / "2";` - then a runtime error is reported.

Deciding whether the language should be statically typed like `C/C++`,`Java`,etc was a bit of a tough one. Mainly because dynamically typed languages tend to waste valuable memory space, due to how memory is allocated - in unneccesary abundance. While in a Statically typed language memory is allocated in a more efficient manner. Making the language dynamically typed was as a direct result of the following:-

+ A lot of load is taken off the programmers shoulders.
+ Allows for the Programmer to focus on the Design/Structure and not so much the implementation.
+ Fewer Obscure errors.   

As a final note, Rocket's C compiler (`RLuna`) allocates memory in accordance with the length of a value. Where a number like `1024` is considered as a `16bit` value. This atleast tries to make up for any unnecessary and inefficient memory allocation.

---

### 2.0 Automatic Memory Management :articulated_lorry:

High-level languages such as `Js`, `Python`, etc all eliminate error-prone, low-level memory management like allocation or precise intervals of memory cleanup. Eliminating the classic "where do i correctly place `free()`" for the C enthusiasts et el.

In these High-level languages there are two main techniques that are implemented for managing memory:-

+ Reference Counting (not commonly known as **RC**)
+ And Trace Garbage Collection (commonly referred to as **Garbage Collection** or **GC** for short).

While Reference counters are much simpler to implement hence why many initial iterations of languages e.g. **PHP**, **Python**, **Perl**, etc start off using them. Along the way they discover that dealing with the [many limitations]() of Reference counting is harder than just swapping it out for GC. Reference Counting is a good proof of concept and GC is just better at the big picture level.

Granted that GC is [notorious]() for causing programmers attempting to debug it with [hex dump]() dreams (That was a stolen Joke). But it has still proven to be robust, and good at what it does - *Picking up the trash for programs*.

Rocket's `rluna` also implements its own Automated GC. Which takes charge of freeing up the previously used either by a program or calculation (in the interactive shell).

---

### 3.0 Data Types

Instilled in Rocket's brain is four fundamental particles - I mean *data types*:-

+ **Boleans**. I.e. **True** or **False**.
+ **Numbers**. I.e. `2048`, `0.4546`, etc.
+ **Strings**. I.e. "Rocket is awesome".
+ And **nin**, as in "*nin is None*".

#### Booleans

At the heart and soul of every computer is *logic* which is represented as **on** or **off**, **1** or **0**, **True** or **False** and is therefore the foundation for programming. Rocket features two boolean values:-

```Rocket
True; /// Not False (aka true)
False; /// Not *not* false (aka false)
```

By default all literals are set to true unless explicitly specified by setting it to **False** or **nin**. Meaning everything except for **False** and **nin** are  *truthy* like in **Ruby**.

#### Numbers

Rocket uses the `Number` type for values that can be classified as an **int**, **float**, **scientific** (including `i` or `j`), **hex**, **octal** etc. **Luna** dynamically assigns values that are of the `Number` type their equivalent or close enough to type in the **C** Language. For example:-

```Rocket
var num = 1024; /// Stored by Rocket as Number type
```  

But for example **RLuna** does

```c
long num;

```

#### Strings

Remember the code snippet in `0.0`? No? Just scroll up. Seen it? Good. The text `"Hello, World!"` is what Rocket considers a string - a series of characters enclosed in **single** (') or **double** (") quote. Like most languages Rocket sees `"Hello World"` and `'Hello World'` as the same thing - a **string**. Here are some sample strings:-

```Rocket
"Stringy me";
""; /// Empty string
"1024"; /// String, not Number
```

#### nin

A little over the board? maybe. nin is Rocket's version of Python's **None**. nin stands for **n**in **I**s **N**one. It basically represents *no value*. The point of nin is just to avoid any *null point errors*, since **RLuna** is written in C.

---

### 4.0 Expressions :performing_arts:

> "If built-in types and their literals are atoms, then **expressions** must be the Molecules" - Robert Nystrom [Creator of the Lox Language]

Basically expressions are just groupings of literals linked together by some operator or just more literals, the same way in English clauses are groups of words put together. E.g:-

```Rocket
"Hello" + "World!";
```

The following are the kinds of expressions that Rocket understands.

##### Arithmetic Expressions

```Rocket
2 + 2;
add + me; /// same meaning as expression above
1024 * 6;
9826 / 22.3;
33 // 3; /// Yes even we reserved '//' for floor division instead of comments. hence why single line comments begin with '///' in Rocket
12 % 2;

-333; // Also considered an expression. I.e Negate '333'
```

##### Comaprisons/Equality

Yep the classics!

```Rocket
less < than;
lessThan <= orEqual;
6 > 8;
1 >= 0;
```

Rocket supports type to type comparisons and also comparisons of different types to each other. E.g:-

```Rocket
1 == 2; /// Evaluates to False
"Boy" != "Man"; /// Evaluates to True
314 == "pi"; /// Evaluates to False
```

> Note: Values of different types are never equal by default. Rocket doesn't Support Javascript's coersion.

#### Logical Oprators

In Rocket *prefixing*  the not operator (`!`) to literal returns the opposite of the literal. E.g:-

```Rocket
!True; /// Returns False
!False; /// Returns True
```

Likewise *prefixing* `and` invokes the and operator while `or` invokes the or operator, logic gate style. The and operator returns True if both literals are True and False otherwise. And the or operator returns True if  either literals if True and False Otherwise.E.g:-

```Rocket
true and true; /// Returns True
false or true; /// Returns True
```

##### Operation Precedence

Rockets operators have the same precedence and associativity as observed in Python or C. However, Rocket does allow you to override the default precedence by using braces `()` to group calculations.E.g:-

```Rocket
var num = low + high / 2; /// Result: low + (high / 2)
```

---

### 5.0 Statements :speech_balloon:

Statements are just Expressions that produce an effect not necessarily a value. This effect could be modifying a literal's state, reading input, producing output, etc. A good example is our hello world program, because the program is just a statement.

```Rocket
 /// This Statement displays output: 'Hello, world!'

print "Hello, world!";
```

There are also **expression statements**, where an expression is basically appended with the `;` symbol indicating the end of a statement. Because Rocket like C uses `;` to delimit statements. Thus making `2 + 2;` is actually an **expression statement** only because of the `;` delimiter.

A block is grouped using braces `{}` as follows in Rocket:-

```Rocket
// A block simply put is just stack of statements

{
    print "I am shown first!";
    print "I hate being last";
}
```

These blocks can also affect the **scope** of a function or program in general. E.g:-

```Rocket
func inc() {
    n = 9;
    return n;
}

inc();

print n /// Results in an Error because 'n' is only defined in the inc function's block    
```

---

### 6.0 variables

> Note: Rocket encourages use of camel case for variable names

variables in Rocket require the keyword `var` or `const` before they are declared. Like:-

```Rocket
var num = 8;
const NODE = "127.0.0.1:7545"; /// 'const' variables require an initializer
```

In Rocket declaring a variable with `var` without explicitly assigning it a value automatically makes it default to `nin`. Once variables are declared they can be referenced by their name. Variables declared with `const` are immutable and require an initializer. Otherwise the following error message is printed; `Error at ';':  'const' variables require initializers`.These variables are cannot be re-defined once initialized. Their purpose is to provide static immutable pieces of data to use.

In cases were a variable's value needs to change the following happens:-

> **Note**: This only affects variables declared with the `var` keyword. `const` variables cannot be re-defined.

```Rocket
var favouriteDrink = "Coke";

/// After you change your mind
favouriteDrink = "Pepsi"
```

Some variable names are considered **illegal** if they begin with number literals, like:-

> **Note**: This affects both `const` and `var` variables.

```Rocket
/// Wrong
var 8788L = "woohoo"; /// considered an 'illegal' declaration

/// Right
var validVar = "Uhuhh";
```

---

### 7.0 Control Flow :ocean:

Control flow refers to the manner in which code is executed. Whether a certain block is evaluated only if a certain condition is met. The keywords used for such are:-

+ if, else
+ while
+ and for

In the case of an `if` it takes the following form:-

```Rocket
if (condition) {
    print "It was true";
} else {
    print "It was false";
}
```

A `while` loop takes the following form:-

```Rocket
var n = 1;

// Loops through 100 digits and prints each one
while (n < 100) {
    print n
    n = n + 1;
}
```

Lastly a `for` loop has the form:-

```Rocket
for (var n = 1; a < 50; a++) {
    print n;
}
```

It is worth noting that there is a difference between a `while` loop and a `for` loop.

---

### 8.0 Functions

when the programmer decides that she wants to reuse a block of code later her program a function is declared. A sample function declaration is as follows:-

```Rocket
func name(args) {
    /// code
}
```

Functions are declared with the keyword `func` followed by the function name and an optional argument or arguments and then code is enclosed in braces. Functions that don't explicitly return anything implicitly return `nin`.

> If a function is invoked without the parenthesis its reference is what is returned.

#### Closures

Functions are *first class* meaning they are actual values that variables can get reference to. Such manipulations are valid:-

```Rocket
func digit() {
    return 2;
}

var num = digit(); /// num has the value 2

func addList(a, b) {
    return a + b;
}

func id(a) {
    return a;
}

print id(addList([1,2,3], [4,5,6])); /// Returns [1,2,3,4,5,6]

/* Nested functions are also possible
Resulting in the creation of local variables
*/

func outer() {
    func inner() {
        print "I'am buried";
    }

    return inner();
}

outer(); /// Outputs "I'am buried"


/// nested functions are permitted

func returnFunction() {
  var outside = "outside";

  fun inner() {
    print outside;
  }

  return inner;
}

var fn = returnFunction();

fn(); /// Outputs "outside"
```

---

### 9.0 Classes :neckbeard:

Rocket features Object-Oriented-Programming (**OOP**). Which allows the programmer to define an object and declare instances of that object. A simple analogy is a *Human* being an object and an instance of a *Human* would be a *Woman*. Classes take the form:-

```Rocket
class Object {
    init(props) {
        /// Default properties
    }

    attr() {
        /// code
    }

    attr2(args) {
        /// more code
    }
}
```

> Notice that methods are declared like functions but without the `func` keyword.

The body of a class contains its methods. They look like function declarations but without the `func` keyword. When the class declaration is executed, it creates a class object and stores it in a variable named after the class. Just like functions, classes are first class in Rocket:-

```Rocket
class Person {
    init(name) {
        this.name = name;
    }

    talk() {
        print "Hi, I am " + this.name;
    }
}

var alice = Person("Alice");

alice.talk(); /// Outputs "Hi, I am Alice"
```

> Notice that Methods of a class are accessed the same they are accesed in other languages like **Python**.

Next, we need a way to create instances. We could add some sort of new keyword, but to keep things simple, in Lox the class itself is a factory function for instances. Call a class like a function and it produces a new instance of itself:

New methods or properties can be added to a class on the fly like so:-

```Rocket
class Drink {
    init(name) {
        this.name = name;
    }
}

var coke = Drink("Coke");

coke.isFull = True;
```

If you noticed classes have a method named init(), it is called automatically when the object is constructed. Any parameters passed to the class are forwarded to its initializer.

```Rocket
class SportsCar {
    init(brand, model) {
        this.brand = model;
        this.model = model;
    }

    /// More methods

}

var electricCar = SportsCar("tesla", "roadstar");

electricCar.topSpeed(250);
```

#### Inheritance

Rocket supports (full) class inheritance, where newly defined classes can *inherit* properties of other objects. E.g:-

```Rocket
class Earth < Planet {
    revolve() {
        print "I just R-evolved"; /// Anyone? Catch that?
  }
}
```

Your probably wondering why Planet is not just enclosed in the brace like `Earth(Planet)`. I wanted **Ruby** to have a piece of the production and also because it looks cooler. The point of `<` is to show that Earth is a subclass of Planet.

```Rocket
class Computer {
    init(os) {
        this.os = os;
    }
}


class Laptop <  Computer {
    turnOn() {
        print "I am awake";
    }
}


var macBook = Laptop("Kali");
```

> Notice that even Computer's init is inherited

Rocket provides a way to overide `init` method of a super class with use of the `super` keyword. Like:-

```Rocket
class Laptop < Computer {
    init(os, arch) {
        super.init(os);
        this.arch = arch;
    }
}

var macBook = Laptop("Mac Os", "x86_64");
```

---

### x.x The Standard Library :file_folder:

Rocket comes shipped with a standard library which includes the following packages:-

> The `math` module include a `random` function which returns a random number between **0** and **1**.

+ **math**:- For math related functions. E.g `sqrt`, `log`, etc.

+ **time**:- For time related function. E.g `time.date`.

+ **crypto**:- For Cryptography related functions. E.g `hash`.

+ **io**:- For File manipulation functions. E.g `read`,`write`.

+ **os**:- For interaction with the computer. E.g `os.platform`.

+ **sys**:- for Argument parsing. E.g `sys.argv`.

+ **socket**:- For close to low level Networking. E.g **Python**'s `socket` module.

+ **web**:- For *http*, *https*, *server*, etc related functions.

+ **blockchain**:- For Blockchain related functions. E.g `blockchain.chain`

As the language continues to mature more packages would be added. Probably demanding that a centralized package repo store to be set up. Just think **Python**'s pypi.

> **Food For Thought**: How would a `decentralized` *distributed* (like hosted on **IPFS**) package repo host do compared to a `centralized` one like a CDN?

---

That's the Rocket Lang in a nutshell.
