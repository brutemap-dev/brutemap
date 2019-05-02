#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import time

from lib.utils.output import HtmlWriter
from lib.utils.progress import Spinner
from lib.browser import browser
from lib.core import getAccount
from lib.core import getPage
from lib.core import isStandardLoginPage
from lib.core import isWebShellLoginPage
from lib.core import makeFile
from lib.data import logger
from lib.data import SETTING
from lib.data import TARGET
from lib.exceptions import BrutemapNextTargetException
from lib.exceptions import BrutemapSkipTargetException
from lib.exceptions import BrutemapStopBruteForceException
from lib.exceptions import BrutemapQuitException
from lib.settings import TOOL_NAME

def bruteForceAttack(fields, http_auth=None):
    """
    Memulai brute force
    """

    start_time = time.time()
    if http_auth is None:
        TARGET.PAGE = getPage(browser.current_url)

    try:
        SETTING.BRUTE_SESSION = True

        if http_auth is not None:
            from lib.brute.types.httpauth import login

            for account in getAccount():
                if account is None:
                    break

                login(*account)

        elif isStandardLoginPage(fields):
            from lib.brute.types.standard import login

            for account in getAccount():
                if account is None:
                    break

                login(*account)

        elif isWebShellLoginPage(fields):
            from lib.brute.types.webshell import login

            for password in getAccount():
                if password is None:
                    break

                login(password)

        else:
            from lib.brute.types.slide import login

            TARGET.PAGE = [TARGET.PAGE]
            for account in getAccount():
                if account is None:
                    break

                login(*account)

    except BrutemapStopBruteForceException:
        pass

    SETTING.BRUTE_SESSION = False
    elapsed = time.time() - start_time
    credType = "account" if len(fields) == 0 or not isWebShellLoginPage(fields) else "password"
    totalCred = len(TARGET.CREDENTIALS)
    infoMsg = "Total %s(s): %d (elapsed %s)" % (credType, totalCred, elapsed)
    logger.info(infoMsg)

    exc_class = BrutemapSkipTargetException

    if totalCred > 0:
        SETTING.IGNORE_INTERRUPT = True
        fp = makeFile()
        fieldnames = ["#"]
        if credType == "account":
            fieldnames.append("username")
        fieldnames.append("password")

        output = HtmlWriter(fp, fieldnames)
        infoMsg = "[%s] [%s] INFO: Saving... " % (time.strftime("%X"), TOOL_NAME.capitalize())
        spin = Spinner(infoMsg, maxval=totalCred)
        for i, cred in enumerate(TARGET.CREDENTIALS):
            i += 1
            cred = (i,) + cred
            output.add_rows(*cred)
            spin.show_progress()

        output.close()
        spin.done()

        infoMsg = "Results from %s are stored in '%s'" % (TOOL_NAME, fp.name)
        logger.info(infoMsg)

        SETTING.IGNORE_INTERRUPT = False
        exc_class = BrutemapNextTargetException

    if SETTING.EXIT_NOW:
        exc_class = BrutemapQuitException

    raise exc_class
