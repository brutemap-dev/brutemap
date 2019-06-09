#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import argparse
import json
import os
import sys

from lib.utils.option import PrettyHelpFormatter
from lib.compat import xrange
from lib.core import createWordlist
from lib.core import printVersion
from lib.data import DEFAULT
from lib.data import SETTING

def cmdLineParser():
    """
    konfigurasi opsi
    """

    parser = argparse.ArgumentParser(formatter_class=PrettyHelpFormatter)

    try:
        parser.add_argument(
            "-v", "--version",
            dest="version",
            action="store_true",
            help="Show version number and exit"
        )

        # Target options
        target = parser.add_argument_group(
            "Target",
            "This option is used to enter the target."
        )

        target.add_argument(
            "-t", "--target",
            dest="targets",
            metavar="url",
            nargs="+",
            help="Target URL (e.g. http://www.example.com/admin/login.php) or FILE (e.g. /path/to/targets.txt)"
        )

        # Credential options
        credential = parser.add_argument_group(
            "Credential",
            "This option is used to enter a list of usernames, passwords or email domains."
        )

        credential.add_argument(
            "-u", "--user",
            dest="usernames",
            metavar="username",
            nargs="*",
            help="Username or FILE (e.g. /path/to/usernames.txt)"
        )

        credential.add_argument(
            "-p", "--pass",
            dest="passwords",
            metavar="password",
            nargs="*",
            help="Password or FILE (e.g. /path/to/passwords.txt)",
        )

        credential.add_argument(
            "-d", "--domain",
            dest="domains",
            metavar="domain",
            nargs="*",
            help="Email domain or FILE (e.g. /path/to/domains.txt)"
        )

        # Request options
        request = parser.add_argument_group(
            "Request",
            "This option is used to set HTTP connection requests."
        )

        request.add_argument(
            "--timeout",
            dest="socket_timeout",
            metavar="seconds",
            type=float,
            help="Socket timeout (default %d)" % DEFAULT.SOCKET_TIMEOUT
        )

        request.add_argument(
            "--retries",
            dest="max_retry",
            metavar="num",
            type=int,
            help="The limit repeats the connection, if it has a problem (default %d)" % DEFAULT.MAX_RETRY
        )

        request.add_argument(
            "--delay",
            dest="delay",
            metavar="seconds",
            type=float,
            help="Waiting time before starting the connection (default %d)" % DEFAULT.DELAY
        )

        # Attack options
        attack = parser.add_argument_group(
            "Attack",
            "This option is used to select the attack method."
        )

        attack.add_argument(
            "--twin",
            dest="twin_mode",
            action="store_true",
            help="Test passwords based on the current username index (e.g. user1:passw1, user2:passw2, ...)"
        )

        attack.add_argument(
            "--sqli-bypass",
            dest="sqli_bypass_mode",
            action="store_true",
            help="Test the account using SQL injection payloads"
        )

        attack.add_argument(
            "--sqli-payloads",
            dest="use_sqli_payloads",
            action="store_true",
            help="Test the account using the username and SQL injection payloads"
        )

        # Verify options
        verify = parser.add_argument_group(
            "Verify",
            "This option is used for the account verification process."
        )

        verify.add_argument(
            "--regex-map",
            dest="regex_map",
            metavar="json",
            help="Check pages using regex (e.g. '(?i)Dashboard')"
        )

        verify.add_argument(
            "--prompt",
            dest="show_prompt",
            action="store_true",
            help="Showing a prompt, if the account has the potential to be found"
        )

        # Other options
        other = parser.add_argument_group(
            "Other"
        )

        other.add_argument(
            "--use-webdriver",
            dest="use_webdriver",
            metavar="name",
            help="Use custom webdriver (default auto-detect)"
        )

        other.add_argument(
            "--webdriver-timeout",
            dest="webdriver_timeout",
            metavar="seconds",
            type=float,
            help="Waiting time loads page (default %d)" % DEFAULT.WEBDRIVER_TIMEOUT
        )

        other.add_argument(
            "--max-cred",
            dest="max_credential",
            metavar="num",
            type=int,
            help="Limit find account"
        )

        other.add_argument(
            "--output-dir",
            dest="output",
            metavar="file",
            help="Result file name or with directory (e.g. /path/for/result.html)"
        )

        opt = parser._actions[0]
        opt.help = opt.help.capitalize()

        # Hack modul argparse untuk mendukung unique option!
        uniqueOptions = {} # penyimpanan opsi unik
        for action in parser._actions: # menguraikan aksi opsi
            option = None # opsi yang bisa dijadikan (opsi unik)
            for opt in action.option_strings: # menguraikan daftar opsi
                # ketika di str.lstrip(), opsi harus punya tanda '-' (satu atau lebih)
                if opt.lstrip("-").count("-") >= 1:
                    option = opt
                    break

            if option is None:
                continue

            # ok-gud => ['ok','gud']
            parts = option.lstrip("-").split("-", 1)
            # ok-gud => -oG
            opt = "-" + parts[0][0].lower() + parts[1][0].upper()
            # cek jika opsi unik belum ada di penyimpanan
            if opt not in uniqueOptions:
                # mengganti opsi unik dengan opsi asli
                uniqueOptions[opt] = option
                # menambahkan opsi unik ke aksi opsi
                action.option_strings.insert(0, opt)

        args = sys.argv[1:]
        for i in xrange(len(args)):
            opt = args[i]
            # cek jika anda menggunakan opsi unik
            if opt in uniqueOptions:
                # dan... ganti dengan opsi asli ! simple !
                args[i] = uniqueOptions.get(opt)

        # mulai menguraikan...
        options = parser.parse_args(args)
        if options.version:
            printVersion()

            raise SystemExit

        if not options.targets:
            errMsg = "try '-h/--help' for more information"
            parser.error(errMsg)

        if options.sqli_bypass_mode and options.use_sqli_payloads:
            errMsg = "clash options! you have to choose one option "
            errMsg += "('--sqli-bypass' or '--sqli-payloads')"
            parser.error(errMsg)

        if options.sqli_bypass_mode:
            options.usernames = DEFAULT.SQLI_PAYLOADS
            options.passwords = options.usernames

        if options.use_sqli_payloads:
            SETTING.SQLI_PAYLOADS = createWordlist(DEFAULT.SQLI_PAYLOADS)

        if options.regex_map:
            if os.path.isfile(options.regex_map):
                with open(options.regex_map, "r") as fp:
                    options.regex_map = fp.read()
            try:
                options.regex_map = json.loads(options.regex_map)
            except ValueError as e:
                errMsg = "cannot load json object: %s\n\n" % options.regex_map
                errMsg += str(e)
                parser.error(errMsg)

        if options.max_credential:
            if options.max_credential < 1:
                errMsg = "the value of the '--max-cred' option must be greater than 1"
                parser.error(errMsg)

        return options

    except argparse.ArgumentError as e:
        parser.error(e)
