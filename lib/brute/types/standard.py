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

@brutemanager
def login(username, password):
    form, u_field, p_field = getFormField()
    u_field.clear()
    u_field.send_keys(username)
    p_field.clear()
    p_field.send_keys(password)
    form.submit()

    status = verifyAccount()
    infoMsg = "Account => %s : %s (%s)" % (username, password, status)
    logger.info(infoMsg)

    if status == STATUS.OK:
        TARGET.CREDENTIALS.append((username, password))
        browser.delete_all_cookies()
        browser.get(TARGET.URL)
