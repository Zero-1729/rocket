# Author: Abubakar NK (Zero-1729)
# License: GNU GPL V2

#!/usr/bin/python

import sys
import readline


def usage():

    info = """usage: stellar [option] ... [ file ] [arg] ...

    Options and arguments (and corresponding environment variables):
    -h     : print this help message and exit (also --help)
    -q     : don't print version and copyright messages on interactive startup
    -v     : print the Rocket version number and exit (also --version)
    
    file   : program read from script file
    """

    return info


def run_file(path):
    with open(path, encoding='utf-8') as f:
        run(f.read())


def run_prompt(headerless=False):

    header = f"""Rocket 0.0.1 | Rocket Labs | [Stellar 0.1.1-b] (Ubuntu 4.4.7-1)] on linux\n"""

    if not headerless:
        print(header)

    while True:

        readline.set_auto_history('enabled')

        chunk = input('<>> ')

        if chunk != "exit":
            print(chunk) # replace with actual shell interpreter (REPL)
            
        else:
            sys.exit(0)


def run(source):
    print(f"Source Contents:\n\n\t{source}")


def main():

    sca = ['-q', '--quite', '-v', '--version', '-h', '--help']

    if len(sys.argv) > 2:
        print(usage())
        sys.exit(1)

    elif len(sys.argv) == 2 and sys.argv[-1] not in sca:
        run_file(sys.argv[1])

    elif len(sys.argv) == 2:
        if sys.argv[-1] == '-q' or sys.argv[-1] == '--quite':
            run_prompt(True)

        elif sys.argv[-1] == '-v' or sys.argv[-1] == '--version':
            print("Rocket v0.0.1 [Stellar v0.1.1-b]")

        elif sys.argv[-1] == '-h' or sys.argv[-1] == '--help':
            print(usage())

    else:
        run_prompt()


if __name__ == '__main__':
    main()
