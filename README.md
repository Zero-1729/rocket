# ![](logo/logo-full-with-text-large.png)

## The Syntax* Hackable Language

---

## About :book:

Rocket is a High level Dynamically-typed, Object-Oriented Programming Language that facilitates easy keyword-syntax customization.


[More](docs/About.md)

---

## Docs :books:
[Specification](docs/Specification.md) For Information on The Language Specification.<br>
[User Guide](docs/Tutorials.md) For Tutorials.

---

## Rocket's Compiler & Interpreter

> The Rocket Repo comes with Rocket's C VM (**Luna**) as well as the Python Interpreter (**Stellar**).

#### Which am I running?

Just type in `rocket -v` or `rocket --version`. You would see the Rocket version aswell as the name of the interpreter and its associated version. E.g:-

```
$ rocket -v
Rocket v0.1.8-p [Stellar v0.2.7-b]
```

From the output above, we can see that we are running `stellar` v0.2.7-b.

##### Which One should I get?

It depends on your needs!

##### RLuna :full_moon:

> Note: RLuna is still in development.

RLuna is intended to be a compiler for Rocket, and when finished would be used to compile source code into an intermediate "parts" file and executed by the vm.

##### Stellar :dizzy:

This is recommended for Beginners and Users who prefer to use the interactive shell or run their code without compiling. Like the Python interpreter, **Stellar** can be run as an interactive shell by invoking the `rocket` command which would start the interactive shell:-

```
$ rocket
Rocket 1.0.1 | Rocket Labs | [Stellar 0.2.1] (Ubuntu 4.4.7-1)] on linux
Type "help", "copyright", "credits" or "license" for more information.

><>
```

Or alternatively invoke the `rocket` command followed by a file path to execute a Rocket program like so:-

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

> You need GNU's **GCC**, **git** and **make**

```sh
# clone the repo
$ git clone https://github.com/Zero-1729/rocket/

# Navigate into the repo and install the necessary packages
$ cd Rocket/ && python setup.py install

# Run the REPL
$ python main.py
```

---

## Contributing :busts_in_silhouette: :wrench:

> Note: You need GNU's **GCC**, **git** and **make**<br>

```sh
# clone the repo and Navigate into repo
$ git clone https://github.com/Zero-1729/rocket/ && cd rocket/
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


Rocket's creation was made possible by the insights provided by Robert Nystrom in his [craftinginterpreters series](https://github.com/munificent/craftinginterpreters) and various other works like [byterun](https://github.com/byterun).

---

> Copyright &copy; Abubakar N K (@Zero-1729) :neckbeard:<br>
[**Rocket Labs**](https://github.com/Zero-1729) RLOL &copy; 2018 - 20
