# About Rocket :book:

The Rocket Programming Language is a high level Keyword-Syntax Hackable, Multi-paradigm, Dynamically Typed language, much like [Python](https://python.org), [Javascript](https://wikepedia.com/Javascript), etc.

## Inspiration

The language is inspired by Python's clean syntax and OOP structure and certain Javascript design choices. This makes the language feel like a cross between Python and Js, and some extra stuff.


## What do we mean by **hackable**?

The language comes with a set of default keywords ([list of keywords](https://github.com/Zero-1729/rocket/tree/master/docs/Specification.md#x.x-list-keywords)), operator signs (op signs), etc. like all other languages. However, You can customize Rocket's keywords to your liking by writing a small `config.rckt` file.

Create `config.rckt` file in your project's **root directory**

```rckt
// My customs
this        self
keep_that   while
bake        print
```

> **Note**: including symbols would trigger an error.

The file should contain a list of mappings of the type `new default`.

Rocket by default searches for this file and makes the necessary changes to its *Keyword Syntax List* (KSL) and bundles your script if program execution was fired, otherwise it uses this in your `REPL` session.

> **Note**: The reason for this addition is to make the language flexible enough to hack the syntax keywords without having to touch the guts of the Interpreter at all. Plus, this gives the user additional freedom to code with keywords of their choice.
