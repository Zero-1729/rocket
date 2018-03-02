# About Rocket :book:

The Rocket Programming Language is a high level syntax hackable dynamiclly typed language, much like [Python](https://python.org), [Javascript](https://wikepedia.com/Javascript), etc. while being both an interpreted and compiled language.

## Inspiration

Really the language is inspired by Python's clean syntax and OOP structure and Javascript's savyness. So basically the language will feel like a cross between Python and Js.


## What do we mean by **hackable**?

The language comes with a set of default keywords ([list of keywords](https://github.com/RocketLabs/Docs/Specification.md)), Operator Signs (Op Signs), etc like all other languages. However, You can customize Rocket's keywords and Op Signs to your liking by writting a small `config.rckt` file. E.g:-

Create `config.rckt` file in your project's **root directory**

```rckt
// First Section
[keywords]

this => self
keep_that => while
bake => print

EOS

// Last Section
[operators]

<- => =

EOF
```

> **Note**: Whitespaces and Comments are ignored.

Where you specify the spefic part of Rocket's syntax you want to edit in a `[]`. Followed by a list of mappings of the type `new -> default`. `EOS` or `End Of Section` is the keyword written at the end of a section. Lastly An `EOF` or `End Of File` string is written at the end of the file, indicating the end of the config file.

The Rocket Compiler by default searches for this file and makes the necessary changes to the Compiler's *Keyword Syntax List* (KSL), and *Operator Syntax List* (OSL), and bundles your script.

> Note: The reason for this addition is that I wanted to make the language flexible enough to hack the syntax without having the touch the guts of the Compiler at all. So I decided the easiest way is to provide a uniform way to do it! :sunglasses:
