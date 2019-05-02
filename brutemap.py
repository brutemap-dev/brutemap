#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import sys

sys.dont_write_bytecode = True

try:
    from lib.path import setPath

    setPath(__file__)

except ImportError:
    errMsg = "[!] Unable to set base path ! (missing modules). "
    errMsg += "See 'https://github.com/brutemap-dev/brutemap#installation' "
    errMsg += "for installation instructions.\n"
    exit(errMsg)

try:
    from lib.controller.start import initialize
    from lib.parse.cmdline import cmdLineParser
    from lib.core import initOptions
    from lib.core import printBanner
    from lib.core import printStatus
    from lib.core import stdoutWrite
    from lib.settings import IS_WINDOWS

except KeyboardInterrupt:
    print
    errMsg = "[!] Aborted..."
    exit(errMsg)

def main():
    """
    Fungsi utama untuk menjalankan brutemap di terminal
    """

    printBanner()

    show_exit_msg = True

    try:
        initOptions(cmdLineParser())
        printStatus()
        initialize()

    except SystemExit:
        print
        show_exit_msg = False

    finally:
        if show_exit_msg:
            printStatus(start=False)

    if IS_WINDOWS:
        stdoutWrite("[#] Press any key to continue... ")
        raw_input()

if __name__ == "__main__":
    main()
