# ![](logo/logo-full-with-text-large.png)

## The Syntax* Hackable Language

---

## About :book:

Rocket is a High-level Dynamically-typed Object-Oriented Programming Language that enables easy keyword-syntax customization out-of-the-box.


[More](docs/About.md)

---

## Docs :books:
[Specification](docs/Specification.md) For Information on The Language Specification.<br>
[Code Samples](https://github.com/Zero-1729/rocket/tree/master/code%20samples) For code samples.

---

## Rocket's Compiler & Interpreter

> The Rocket Repo comes with Rocket's C VM (**Rluna**) as well as the Python Interpreter (**Stellar**).

### Which am I running?

Just type in `rocket -v` or `rocket --version`. You would see the Rocket version aswell as the name of the interpreter and its associated version. E.g:-

```
$ rocket -v
Rocket v0.1.8-p [Stellar v0.2.7-b]
```

From the output above, we can see that we are running `stellar` v0.2.7-b.


#### Rluna :full_moon:

> Note: Rluna is still in development.

Rluna is intended to be a compiler for Rocket, and when finished would be used to compile source code into an intermediate "parts" file and executed by the vm.

#### Stellar :dizzy:

This is recommended for Beginners and Users who prefer to use the interactive shell or run their code without compiling. Like the Python interpreter, **Stellar** can be run as an interactive shell by invoking the `rocket` command which would start the interactive shell:-

```
$ rocket
Rocket 1.0.1 | Rocket Labs | [Stellar 0.2.1] (Ubuntu 4.4.7-1)] on linux
Type "help", "copyright", "credits" or "license" for more information.

><>
```

Or alternatively, invoke the `rocket` command followed by a file path to execute a Rocket program like so:-

```
$ rocket hello.rckt
Hello Wolrd!
$
```

Invoking the `rocket` command and the `--help` option would produce a list of Stellar's usage. E.g:-

```
$ rocket --help
usage: rocket [ <option> | <file> ]

    Options and arguments (and corresponding environment variables):
    -c cmd : program <cmd> entered as string and executed
    -h     : print this help message and exit (also --help)
    -q     : don't print version and copyright messages on interactive startup
    -v     : print the Rocket version number and exit (also --version)

    file   : program read from script file

    RCKTPROMPT: Rocket Lang prompt environment variable. Default "><> ".
```

## Installation :floppy_disk:

### Source :scroll:

> You need **Python** 3.6.x+ installed.

```sh
# clone the repo
$ git clone https://github.com/Zero-1729/rocket/

# Navigate into the repo and install the necessary packages
$ cd rocket/stellar

# Run the REPL
$ python main.py

# Install stellar to use in Python
$ python setup.py install
```

---

## Contributing :busts_in_silhouette: :wrench:

> Note: You need **Python** 3.6.x+ and **git** installed.<br>

```sh
# clone the repo and Navigate into repo
$ git clone https://github.com/Zero-1729/rocket/ && cd rocket/stellar

# install stellar package
$ python setup.py install
```

> Just hack on it as you wish!

The Rocket folder has the following structure:-

```sh
$ tree
rocket
.
| -docs
| -logo
| -rluna # Unfinished C compiler
| -stellar # Python interpreter
| -tests
| -tutorials
.
```

Feel free to open a PR or issue to discuss any bugs :beetle:, improvements :chart_with_upwards_trend:, Ideas :bulb:, etc.

---

## Acknowledgements :pushpin:


Rocket's creation was made possible by the insights provided by Robert Nystrom in his [craftinginterpreters series](https://github.com/munificent/craftinginterpreters) and various other works like [byterun](https://github.com/nedbat/byterun).

---

> Copyright &copy; [Abubakar Nur Khalil](https://github.com/Zero-1729) :neckbeard:<br>
[RLOL](https://github.com/Zero-1729/rocket/tree/master/LICENSE.md) &copy; 2018 - present
