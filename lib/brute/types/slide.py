#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

from lib.parse.htmlform import getFormField
from lib.browser import browser
from lib.core import getPage
from lib.core import isWebShellLoginPage
from lib.core import verifyAccount
from lib.data import logger
from lib.data import STATUS
from lib.data import TARGET
from lib.manager import brutemanager

@brutemanager
def login(username, password):
    _, u_field, _ = getFormField()
    u_field.send_keys(username)
    u_field.submit()
    newFields = getFormField()
    if newFields is not None and isWebShellLoginPage(newFields):
        newPage = getPage(browser.current_url)
        TARGET.PAGE.insert(0, newPage)
        passwordField = newFields[-1]
        passwordField.send_keys(password)
        passwordField.submit()
        TARGET.PASSWORD_TESTED = True

    status = verifyAccount()
    infoMsg = "Account => %s : %s (%s)" % (username, password, status)
    logger.info(infoMsg)

    if status == STATUS.OK:
        TARGET.CREDENTIALS.append((username, password))
        TARGET.PAGE.pop(0)

    browser.delete_all_cookies()
    browser.get(TARGET.URL)
