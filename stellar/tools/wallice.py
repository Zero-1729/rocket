# Author: Abubakar N. K. (Zero-1729)
# LICENSE: RLOL
# Rocket Lang (Stellar) Scanner (C) 2018

import sys as _sys
import os as _os
import subprocess as _subprocess
import time as _time

from pathlib import Path

# Runs set of scripts
# Compares output of the script(s) with a predefined one
# Upon any irregularities, it prints out the expected output and recieved output


def _usage():
    message = """
    Wallice (Script Checker) v0.1.0

    Wallice is a script output consistency checker. It is given a 'target script' or 'target folder'
    for which it either records the script's/scripts' output in a 'storage folder' or
    it compares the output of a script's/scripts' output with the saved '.wlc' file/files in the 'storage folder'.

    Note: The '.wlc' & 'wlc.err' files generated in a 'storage folder' are given the same name as the target scripts
          to avoid name clashes. And so simply writting this file manually (even in the 'storage folder')
          would suffice if you want to compare output of a script or scripts in a 'target folder'.

    Usage: wallice [option] [cmd] [target script | target folder] [storage folders | storage file] <wait_time>

    wait_time: sleep time per script in seconds

    Options: -r --record  cmd    Record output of a (target) script or script(s) in a target folder
                                 and write the output to storage folder.

                                 'cmd' is the command to run for executing the script.
                                 E.g 'python','rocket',etc

             -c --check   cmd    Check the output of (target) script or script(s) in a target folder
                                 against the expected output(s) in storage folder

                                 'cmd' is the command to run for executing the script.
                                 E.g 'python','rocket',etc


    Examples: wallice -r rocket hello.rckt . 1
              wallice -r python tests/ exepectedOutputs 1
              wallice -c rocket hello.rckt exepectedOutputs 1
              wallice -c rocket hello.rckt hello.wlc 1
    """

    print(message)


def record(cmd, script, folder, timeout):
    outfile = _os.path.join(folder, script.split('/')[-1].split(".")[0] + ".wlc")

    # Print status
    print(f"[*] Recording {script} into '{folder}' ...")

    # Lets check if the folder tree sturcture exists
    if not _os.path.lexists(outfile):
        folder = '/'.join(outfile.split('/')[0:-1])
        path = Path(folder)

        try: path.mkdir(parents=True)
        except FileExistsError: pass

    with open(outfile, "w") as f:
        with open(outfile+".err", "w") as e:
            cmd = cmd + " " + script

            process = _subprocess.Popen(cmd, shell=True, stdout=f, stderr=e)
            _time.sleep(timeout)
            process.terminate()

            e.close()

        f.close()

    print(f"[+] Recorded {script}")


def recordScripts(cmd, targetFolder, folder, timeout):
        scripts = [targetFolder + script for script in _os.listdir(targetFolder)]

        for script in scripts:
            record(cmd, script, folder, timeout)


def report(expected, recieved, status):
    if status == "failed":
        print("[!] Recieved offensive output")
        print("\nRecieved: ")
        print(">>> ")
        print(recieved)
        print(">>>")

        print("Expected: ")
        print("<<< ")
        print(expected)
        print("<<<")


def check(cmd, script, outfile, timeout):
    errfile = outfile + '.err'

    tmp_outfile = outfile + '.tmp'
    tmp_errfile = outfile + '.tmp.err'

    passed_output = False
    passed_err = False

    # Print status
    print(f"[*] Checking '{script}' ...")

    # Lets check if the folder tree sturcture exists
    if not _os.path.lexists(outfile):
        folder = '/'.join(outfile.split('/')[0:-1])
        path = Path(folder)

        try: path.mkdir(parents=True)
        except FileExistsError: pass


    with open(tmp_outfile, 'w') as f:
        with open(tmp_errfile, 'w') as e:
            cmd = cmd + " " + script

            process = _subprocess.Popen(cmd, shell=True, stdout=f, stderr=e)
            _time.sleep(timeout)
            process.terminate()

            e.close()
        f.close()

    # Check and report
    # Check output
    with open(outfile, "r") as out:
        with open(tmp_outfile) as tmp_out:
            out_text = out.read()
            tmp_out_text = tmp_out.read()

            if out_text == tmp_out_text:
                report(None, None, "success")
                passed_output = True

            else:
                report(out_text, tmp_out_text, "failed")

            tmp_out.close()
        out.close()

    # Check error
    with open(errfile, "r") as err:
        with open(tmp_errfile, "r") as tmp_err:
            err_text = err.read()
            tmp_err_text = tmp_err.read()

            if err_text == tmp_err_text:
                report(None, None, "success")
                passed_err = True

            else:
                report(err_text, tmp_err_text, "failed")

            tmp_err.close()
        err.close()

    print(f"[{'+' if passed_output else '!'}] stdout {'correct' if passed_output else 'incorrect'}")
    print(f"[{'+' if passed_err else '!'}] stderr {'correct' if passed_err else 'incorrect'}")

    # Delete tmp files after check
    _os.remove(tmp_outfile)
    _os.remove(tmp_errfile)

    return 1 if passed_output else 0, 1 if passed_err else 0


def stripdotted(filename):
    return filename if filename[0] != '.' else ''


def checkScripts(cmd, targetFolder, folder, timeout):
    files = filter(stripdotted, _os.listdir(targetFolder))
    scripts = [_os.path.join(targetFolder, script) for script in files]
    total_scripts = len(scripts)
    passed_out = 0
    passed_err = 0

    for script in scripts:
        outfile = _os.path.join(folder, _os.path.split(script)[-1].split('.')[0] + ".wlc")
        print("===================")

        outs, errs = check(cmd, script, outfile, timeout)

        passed_out += outs
        passed_err += errs

    print("\n=================================")
    print(f"Passed {passed_out}/{total_scripts} for 'stdout' checks")
    print(f"Passed {passed_err}/{total_scripts} for 'stderr' checks")
    print("=================================")


def _main():
    if len(_sys.argv) == 6:
        timeout = int(_sys.argv[5])

        if _sys.argv[1] in ["-r", "--record"]:
            if _os.path.isfile(_sys.argv[3]):
                record(_sys.argv[2], _sys.argv[3], _sys.argv[4], timeout)


            else:
                recordScripts(_sys.argv[2], _sys.argv[3], _sys.argv[4], timeout)

            _sys.exit(0)


        if _sys.argv[1] in ["-c", "--check"]:
            if _os.path.isfile(_sys.argv[3]):
                if _os.path.isfile(_sys.argv[4]): check(_sys.argv[2], _sys.argv[3], _sys.argv[4], timeout)
                else: print("[!] 'storageFile' must be directory")

            else:
                checkScripts(_sys.argv[2], _sys.argv[3], _sys.argv[4], timeout)

                _sys.exit(0)

        else:
            print(_sys.argv[1])
            _usage()
            _sys.exit(0)

    else:
        _usage()
        _sys.exit(0)


if __name__ == "__main__":
    _main()
