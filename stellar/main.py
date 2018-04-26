# Author: Abubakar NK (Zero-1729)
# License: GNU GPL V2
#!/usr/bin/python

import sys
import os
import readline

from utils.resolver import Resolver

from scanner import Scanner
from parser import Parser
from interpreter import Interpreter

# to scan for 'config.rckt' file
from tools.custom_syntax import Scanner as Dante, Parser as Virgil

# For REPL Auto completion
from tools.autocompleter import AutoComp

# So that global env is static throughout execution. Especially in REPL
interpreter = Interpreter()

def find_config(path='.'):
    if os.path.exists(os.path.join(path, 'config.rckt')):
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


def assemble_ksl():
    KSL = fillKSL()

    # Search for config file
    if find_config():
        KSL = load_config('config.rckt')
        print("<> Loaded 'config' <>")

    return KSL


def locate_and_assemble():
    KSL = fillKSL()

    path = f'{os.path.sep}'.join(sys.argv[1].split(os.path.sep)[0:-1])

    if find_config(path):
        KSL = load_config(os.path.join(path, 'config.rckt'))
        print("<> Loaded 'config' <>")

    return KSL


def assemble_acmp(KSL):
    # Create auto completer
    starters = [key.lower() for key in KSL[0]]
    autoCmp = AutoComp(starters)

    return autoCmp


def UpdateAuto(autoCmp):
    autoCmp.updateEnv(interpreter.environment)
    autoCmp.updateEnv(interpreter.globals)
    autoCmp.update(interpreter.locals)

    readline.set_completer(autoCmp.completer)


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


def run_file(path, KSL):
    with open(path, encoding='utf-8') as f:
        run(f.read(), KSL)


def run_prompt(prompt, headerless=False):
    KSL = assemble_ksl()
    autoCmp = assemble_acmp(KSL)

    header = f"""Rocket 0.1.8-p | Rocket Labs | [Stellar 0.2.7-b] (Ubuntu 16.04.3 LTS)] on linux\n"""

    if not headerless:
        print(header)


    readline.set_completer(autoCmp.completer)
    readline.parse_and_bind("tab: complete")

    # Load repl history file
    try:
        readline.read_history_file('.rocket_repl_history')

    except FileNotFoundError:
        # Just leave it till user finishes session to create the file
        pass

    readline.set_auto_history('enabled')

    while True:

        chunk = input(prompt)

        if chunk == "exit":
            readline.write_history_file('.rocket_repl_history')
            sys.exit(0)

        elif chunk == "":
            pass

        else:
            # Allow user to SIGINT (^C) a running chunk of code and still be in the REPL
            try:
                run(chunk, KSL, "REPL") # replace with actual shell interpreter (REPL)

            except KeyboardInterrupt:
                pass

        UpdateAuto(autoCmp)


def run(source, KSL, mode=None):
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

    resolver = Resolver(interpreter, KSL[1])
    resolver.resolveStmts(statements)
    resolution_errs = resolver.errors

    if hadError: return

    # create interpreter each time 'run' is called
    # Avoids mixing error reports in REPL
    try:
        interpreter.interpret(statements)
    except Exception:
        pass

    runtime_errs = interpreter.errors + resolution_errs
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
            KSL = locate_and_assemble()

            run_file(sys.argv[1], KSL)
            sys.exit(0) # Run file and exit

        except FileNotFoundError:
            print("Error: File not found")
            exit(1)

    elif len(sys.argv) == 2:
        if sys.argv[-1] == '-q' or sys.argv[1] == '--quite':
            run_prompt(prompt, True)

        elif sys.argv[-1] == '-v' or sys.argv[-1] == '--version':
            print("Rocket v0.1.8-p [Stellar v0.2.7-b]")

        elif sys.argv[-1] == '-h' or sys.argv[-1] == '--help':
            print(usage())


    if len(sys.argv) == 2 and sys.argv[1] == '-c':
        print(usage())

    elif len(sys.argv) == 3:
        if sys.argv[1] == '-c':
            KSL = assemble_ksl()
            run(sys.argv[2], KSL)

    else:
        print(usage())
        sys.exit(1)



if __name__ == '__main__':
    main()
