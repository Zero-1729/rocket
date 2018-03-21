# About Rocket :book:

The Rocket Programming Language is a high level syntax hackable dynamiclly typed language, much like [Python](https://python.org), [Javascript](https://wikepedia.com/Javascript), etc. while being both an interpreted and compiled language.

## Inspiration

Really the language is inspired by Python's clean syntax and OOP structure and Javascript's savyness. So basically the language will feel like a cross between Python and Js.


## What do we mean by **hackable**?

The language comes with a set of default keywords ([list of keywords](https://github.com/RocketLabs/Docs/Specification.md)), Operator Signs (Op Signs), etc like all other languages. However, You can customize Rocket's keywords and Op Signs to your liking by writting a small `config.rckt` file. E.g:-

Create `config.rckt` file in your project's **root directory**

```rckt
// My customs
this ? self
keep_that ? while
bake ? print
```

> **Note**: Only single line comments `//` are allowed. Whitespaces and Comments are ignored.

Where a list of mappings of the type `new ? default` is given. The question mark `?` acts as the equator linking the `new` to the `default`.

The Rocket by default searches for this file and makes the necessary changes to its *Keyword Syntax List* (KSL) and bundles your script if program execution was fired else it uses this in your `REPL` session.

> Note: The reason for this addition is that I wanted to make the language flexible enough to hack the syntax without having the touch the guts of the Compiler at all. So I decided the easiest way is to provide a uniform way to do it! :sunglasses:
