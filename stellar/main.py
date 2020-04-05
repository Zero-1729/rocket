# Author: Abubakar N. K. (Zero-1729)
# LICENSE: RLOL
# Rocket Lang (Stellar) (C) 2018
#!/usr/bin/python

import sys       as _sys
import os        as _os
import readline  as _readline

from utils.resolver import Resolver     as _Resolver

from core.scanner import Scanner             as _Scanner
from core.parser  import Parser              as _Parser
from core.interpreter import Interpreter     as _Interpreter

# to scan for 'config.rckt' file
from tools.custom_syntax import Scanner  as _Dante
from tools.custom_syntax import Parser   as _Virgil

# For REPL Auto completion
from tools.autocompleter import AutoComp as _AutoComp


# Version info
header = "Rocket 0.6.1 | Rocket Labs | [Stellar 0.4.0]"


def find_config(path='.'):
    if _os.path.exists(_os.path.join(path, 'config.rckt')):
        return True

    return False


def load_config(filename):
    source = ''

    # load contents
    with open(filename, 'r') as f:
        source = f.read()
        f.close()

    tks = _Dante(source).scan()
    wk_Dict, vk_Dict = _Virgil(tks).parse()
    return [wk_Dict, vk_Dict]


def fillKSL():
    # Passing an empty fake 'config.rckt' will return th default KSL
    tks = _Dante("").scan()
    wk_Dict, vk_Dict = _Virgil(tks).parse()

    return [wk_Dict, vk_Dict]


def get_env():
    env = _os.environ
    prompt = env.get("RCKTPROMPT")

    if prompt:
        return prompt


def assemble_ksl(noisy=True):
    KSL = fillKSL()

    # Search for config file
    if find_config():
        KSL = load_config('config.rckt')
        if noisy: print("\033[1m<> Loaded 'config' <>\033[0m")

    return KSL


def assemble_acmp(KSL):
    # Create auto completer
    starters = [key.lower() for key in KSL[0]]
    autoCmp = _AutoComp(starters)

    return autoCmp


def save_and_quit():
     # Ctrl-D
    # Save REPL history before exit
    _readline.write_history_file('.rocket_repl_history')

    # to avoid mangled return shell text
    print()
    _sys.exit(0)


def silent_quit():
    # same reason as discussed above
    print()
    _sys.exit(0)


def UpdateAuto(autoCmp):
    autoCmp.updateEnv(interpreter.environment)
    autoCmp.updateEnv(interpreter.globals)
    autoCmp.update(interpreter.locals)

    _readline.set_completer(autoCmp.completer)


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

# So that global env is static throughout execution. Especially in REPL
# Get and pass KSL
KSL = assemble_ksl()
interpreter = _Interpreter(KSL)


def run_file(path):
    with open(path, encoding='utf-8') as f:
        run(f.read())


def run_prompt(prompt, headerless=False):
    # Our KSL is global like the _Interpreter instance
    autoCmp = assemble_acmp(KSL)

    if not headerless:
        print(header, end="\n")

    _readline.set_completer(autoCmp.completer)
    _readline.parse_and_bind("tab: complete")

    # Load repl history file
    try:
        _readline.read_history_file('.rocket_repl_history')

    except FileNotFoundError:
        # Just leave it till user finishes session to create the file
        pass

    _readline.set_auto_history('enabled')

    while True:

        try:
            chunk = input(prompt)
        except EOFError:
            save_and_quit()

        except KeyboardInterrupt:
            silent_quit()

        if chunk == "exit":
            _readline.write_history_file('.rocket_repl_history')
            _sys.exit(0)

        elif chunk == "":
            pass

        else:
            # Allow user to SIGINT (^C) a running chunk of code and still be in the REPL
            try:
                run(chunk, "REPL") # replace with actual shell interpreter (REPL)

            except KeyboardInterrupt:
                pass

        UpdateAuto(autoCmp)


def run(source, mode=None):
    # To avoid running resolver on statements
    hadError = False

    scanner = _Scanner(source, KSL[0])
    tokens = scanner.scan()

    parser = _Parser(tokens, KSL[1])
    statements = parser.parse()

    errors = scanner.errors + parser.errors
    for error in errors:
        print(error, file=_sys.stderr)

    if errors:
        hadError = True

        # We don't bother resolving already 'error'ful code
        return

    resolver = _Resolver(interpreter, KSL[1])
    resolver.resolveStmts(statements)
    resolution_errs = resolver.errors

    if hadError: return

    # create interpreter each time 'run' is called
    # Avoids mixing error reports in REPL
    try:
        interpreter.interpret(statements)
    except:
        pass

    runtime_errs = interpreter.errors + resolution_errs
    for err in runtime_errs: print(err, file=_sys.stderr)

    if mode == "REPL":
        # If running REPL session clear err logs for interpreter
        # To avoid reporting old errors
        interpreter.errors, runtime_errs, errors = [], [], []


def main():
    valids = ['-q', '--quite', '-v', '--version', '-h', '--help', '-c']
    prompt = get_env() if get_env() != None else "><> "

    if len(_sys.argv) == 1:
        try:
            run_prompt(prompt)

        except EOFError:
            save_and_quit()

        except KeyboardInterrupt:
            silent_quit()


    if len(_sys.argv) == 2 and (_sys.argv[1] not in valids):
        try:
            run_file(_sys.argv[1])
            _sys.exit(0) # Run file and exit

        except FileNotFoundError:
            print(f"Error: file '{_sys.argv[1]}' not found")
            exit(1)

    elif len(_sys.argv) == 2:
        if _sys.argv[-1] == '-q' or _sys.argv[1] == '--quite':
            run_prompt(prompt, True)

        elif _sys.argv[-1] == '-v' or _sys.argv[-1] == '--version':
            print(header)
            _sys.exit(0)

        elif _sys.argv[-1] == '-h' or _sys.argv[-1] == '--help':
            print(usage())
            _sys.exit(0)

    if len(_sys.argv) == 2 and _sys.argv[1] == '-c':
        print(usage())

    elif len(_sys.argv) == 3:
        if _sys.argv[1] == '-c':
            run(_sys.argv[2])

    else:
        print(usage())
        _sys.exit(1)



if __name__ == '__main__':
    main()
