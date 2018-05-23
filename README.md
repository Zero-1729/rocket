# ![](logo/logo-full-with-text-large.png)

# The Syntax* Hackable Language

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

> The Rocket Repo comes with Rocket's C VM (**Luna**) aswell as the Python Interpreter (**Stellar**).

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

If you want to compile Rocket programs and run them faster get **RLuna**. Usually advised for any software project that relies on speed, efficiency and accuracy. This is a perfect fit for any programs that require or perform scientific or intense Computation. Running the `rocket` command without specifying a file path produces info about **RLuna**'s usage:-
```
$ rocket
Rocket-Luna is a tool for managing Rocket source code.

Usage:

	rocket command [arguments] [file]

The commands are:

    build       compile packages and dependencies
    install     compile and install packages and dependencies
    test        test packages
    version     print Luna version
```

##### Stellar :dizzy:

This is recommended for Beginners and Users who prefer to use the interactive shell or run their code without compiling. Like the Python Interpreter. **Stellar** can be run as an interactive shell by invoking the `rocket` command which would start the interactive shell:-

```
$ rocket
Rocket 1.0.1 | Rocket Labs | [Sally 0.2.1] (Ubuntu 4.4.7-1)] on linux
Type "help", "copyright", "credits" or "license" for more information.

><>
```

Or alternatively invoke the `rocket` command followed by a file path to execute a Rocket program. Like so:-

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

If you have made up your mind you can follow the instructions below for your platform to download either **Stellar** or **RLuna**, or both :smiley:

### Download

Get the appropriate install file(s) from [Here](https://github.com/rocket.labs/Rocket/releases)

### Source :scroll:

> You need GNU's **GCC**, **git** and **make**

```sh
# clone the repo
$ git clone https://github.com/rocket.labs/Rocket/

# Navigate into the repo and install for your platform
$ cd Rocket/ && make

# The above script Makes the neccesarry preperations for your system to be ready to install both Stellar and Luna

# Run command below to install them
$ make install
```

---

## Contributing :busts_in_silhouette: :wrench:

> Note: You need GNU's **GCC**, **git** and **make**<br>

```sh
# clone the repo and Navigate into repo
$ git clone https://github.com/rocket.labs/Rocket/ && cd Rocket/
```

> Just hack on it as you wish!

The Rocket folder has the following structure:-

```sh
$ tree
Rocket
.
| -docs
| -logo
| -rluna
| -stellar
| -tests
| -tutorials
.
```

Feel free to issue a PR or open an issue to discuss any bugs :beetle:, improvements :chart_with_upwards_trend:, Ideas :bulb:, etc.

---

## Acknowledgements :pushpin:


Rocket's creation was made possible by the insights provided by Robert Nystrom in his [craftinginterpreters series](https://github.com/munificent/craftinginterpreters). And Various other works like [byterun](https://github.com/byterun).

---

> Copyright &copy; Abubakar NK (@Zero-1729) :neckbeard:<br>
[**Rocket Labs**](https://github.com/rocket.labs) RLOL &copy; 2018 - 2019
