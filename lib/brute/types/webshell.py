#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

from lib.parse.htmlform import getFormField
from lib.browser import browser
from lib.core import verifyAccount
from lib.data import logger
from lib.data import STATUS
from lib.data import TARGET
from lib.manager import brutemanager
from lib.exceptions import BrutemapStopBruteForceException

@brutemanager
def login(password):
    _, _, p_field = getFormField()
    p_field.clear()
    p_field.send_keys(password)
    p_field.submit()

    status = verifyAccount()
    infoMsg = "Password => %s (%s)" % (password, status)
    logger.info(infoMsg)

    if status == STATUS.OK:
        TARGET.CREDENTIALS.append((password,))
        browser.delete_all_cookies()
        raise BrutemapStopBruteForceException
