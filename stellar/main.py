# Author: Abubakar NK (Zero-1729)
# License: GNU GPL V2

#!/usr/bin/python

import sys
import os
import readline

from scanner import Scanner
from parser import Parser
from interpreter import Interpreter
from tools.printer import dump_tokens
from tools.astprinter import LispAstPrinter, RPNAstPrinter


# Make interpreter global
#interpreter = Interpreter()


def get_env():
    env = os.environ
    prompt = env.get("RCKTPROMPT")

    if prompt:
        return prompt


def usage():

    info = """usage: stellar [ <option> | <file> ]

    Options and arguments (and corresponding environment variables):
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

    header = f"""Rocket 0.1.1 | Rocket Labs | [Stellar 0.2.1-b] (Ubuntu 16.04.3 LTS)] on linux\n"""

    if not headerless:
        print(header)

    while True:

        readline.set_auto_history('enabled')

        chunk = input(prompt)

        if chunk == "exit":
            sys.exit(0)

        elif chunk == "":
            pass

        else:
            run(chunk) # replace with actual shell interpreter (REPL)


def run(source):
    scanner = Scanner(source)
    tokens = scanner.scan()

    parser = Parser(tokens)
    expression = parser.parse()

    errors = scanner.errors + parser.errors
    for error in errors:
        print(error)

    if errors:
        return errors

    # create interpreter each time 'run' is called
    # Avoids mixing error reports in REPL
    interpreter = Interpreter() 
    interpreter.interpret(expression)

    runtime_errs = interpreter.errors

    for err in runtime_errs: print(err)

    return errors, runtime_errs

    #print(LispAstPrinter().printAst(expression))



def main():

    sca = ['-q', '--quite', '-v', '--version', '-h', '--help']
    prompt = get_env() if get_env() != None else "><> "

    if len(sys.argv) > 2:
        print(usage())
        sys.exit(1)

    elif len(sys.argv) == 2 and sys.argv[-1] not in sca:
        run_file(sys.argv[1])

    elif len(sys.argv) == 2:
        if sys.argv[-1] == '-q' or sys.argv[-1] == '--quite':
            run_prompt(prompt, True)

        elif sys.argv[-1] == '-v' or sys.argv[-1] == '--version':
            print("Rocket v0.1.1 [Stellar v0.2.1-b]")

        elif sys.argv[-1] == '-h' or sys.argv[-1] == '--help':
            print(usage())

    else:
        run_prompt(prompt)


if __name__ == '__main__':
    main()
