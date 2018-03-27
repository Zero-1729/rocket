# Author: Abubakar NK (Zero-1729)
# License: GNU GPL V2
#!/usr/bin/python

import sys
import os
import readline

from utils.tokens import Keywords
from utils.resolver import Resolver

from scanner import Scanner
from parser import Parser
from interpreter import Interpreter

# to scan for 'config.rckt' file
from tools.custom_syntax import Scanner as Dante, Parser as Virgil


# So that global env is static throughout execution. Especially in REPL
interpreter = Interpreter()


def find_config():
    if os.path.exists('config.rckt'):
        return True

    return False


def load_config(filename):
    source = ''

    # load contents
    with open(filename, 'r') as f:
        source = f.read()
        f.close()

    tks = Dante(source).scan()
    keywords, pksl = Virgil(tks).parse()
    return [keywords, pksl]


def fillKSL():
    # Passing an empty fake 'config.rckt' will return th default KSL
    tks = Dante("").scan()
    keywords, pksl = Virgil(tks).parse()
    return [keywords, pksl]


def get_env():
    env = os.environ
    prompt = env.get("RCKTPROMPT")

    if prompt:
        return prompt


# Globally define KSL
KSL = None
# Search for config file
if find_config():
    KSL = load_config('config.rckt')
    print("Loaded 'config'")

else:
    print("No 'config.rckt' found. Launching with default 'KSL'")
    KSL = fillKSL()


def usage():

    info = """usage: stellar [ <option> | <file> ]

    Options and arguments (and corresponding environment variables):
    -c cmd : program <cmd> entered as string and executed
    -h     : print this help message and exit (also --help)
    -q     : don't print version and copyright messages on interactive startup
    -v     : print the Rocket version number and exit (also --version)

    file   : program read from script file

    RCKTPROMPT: Rocket Lang prompt environment variable. Default "><> ".
    """

    return info


def run_file(path):
    with open(path, encoding='utf-8') as f:
        run(f.read())


def run_prompt(prompt, headerless=False):
    header = f"""Rocket 0.1.7-a | Rocket Labs | [Stellar 0.2.7-a] (Ubuntu 16.04.3 LTS)] on linux\n"""

    if not headerless:
        print(header)

    # Load repl history file
    try:
        readline.read_history_file('.rocket_repl_history')

    except FileNotFoundError:
        # Just leave it till user finishes session to create the file
        pass

    while True:

        readline.set_auto_history('enabled')

        chunk = input(prompt)

        if chunk == "exit":
            readline.write_history_file('.rocket_repl_history')
            sys.exit(0)

        elif chunk == "":
            pass

        else:
            run(chunk, "REPL") # replace with actual shell interpreter (REPL)


def run(source, mode=None):
    # To avoid running resolver on statements
    hadError = False

    scanner = Scanner(source, KSL[0])
    tokens = scanner.scan()

    parser = Parser(tokens, KSL[1])
    statements = parser.parse()

    errors = scanner.errors + parser.errors
    for error in errors:
        print(error)

    if errors:
        hadError = True
        return errors

    #resolver = Resolver(interpreter)
    #resolver.resolveStmts(statements)

    if hadError: return

    # create interpreter each time 'run' is called
    # Avoids mixing error reports in REPL
    interpreter.interpret(statements)

    runtime_errs = interpreter.errors
    for err in runtime_errs: print(err, file=sys.stderr)

    if mode == "REPL":
        # If running REPL session clear err logs for interpreter
        # To avoid reporting old errors
        interpreter.errors, runtime_errs, errors = [], [], []

    return errors, runtime_errs


def main():
    sca = ['-q', '--quite', '-v', '--version', '-h', '--help', '-c']
    prompt = get_env() if get_env() != None else "><> "

    if len(sys.argv) == 1:
        run_prompt(prompt)

    if len(sys.argv) == 2 and (sys.argv[1] not in sca):
        try:
            run_file(sys.argv[1])
            sys.exit(0) # Run file and exit

        except FileNotFoundError:
            print("Error: File not found")

    elif len(sys.argv) == 2:
        if sys.argv[-1] == '-q' or sys.argv[1] == '--quite':
            run_prompt(prompt, True)

        elif sys.argv[-1] == '-v' or sys.argv[-1] == '--version':
            print("Rocket v0.1.7-a [Stellar v0.2.7-a]")

        elif sys.argv[-1] == '-h' or sys.argv[-1] == '--help':
            print(usage())


    if len(sys.argv) == 2 and sys.argv[1] == '-c':
        print(usage())

    elif len(sys.argv) == 3:
        if sys.argv[1] == '-c':
            run(sys.argv[2])

    else:
        print(usage())
        sys.exit(1)



if __name__ == '__main__':
    main()
