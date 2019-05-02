#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import functools
import time

from urllib3.exceptions import ProtocolError

from lib.data import logger
from lib.data import SETTING
from lib.data import TARGET
from lib.exceptions import BrutemapException
from lib.exceptions import BrutemapStopBruteForceException
from lib.webdriver import reinitWebDriver

INFO_ACCOUNT = []
RETRY_COUNT = 0

def errormanager(func, re_init=True):
    """
    Menangkap spesifikasi pengecualian
    """

    @functools.wraps(func)
    def decorated(*args, **kwargs):
        global RETRY_COUNT

        try:
            return func(*args, **kwargs)

        except ProtocolError, e:
            # XXX: abaikan ?
            pass

        except Exception, e:
            if issubclass(e.__class__, BrutemapException):
                raise e

            time.sleep(SETTING.DELAY)
            if re_init:
                reinitWebDriver()

            logger.error("Error occurred: %s" % str(e))
            if RETRY_COUNT != SETTING.MAX_RETRY:
                RETRY_COUNT += 1
                return decorated(*args, **kwargs)

            raise e

    return decorated

def brutemanager(func):
    """
    Mengelola akun valid
    """

    @functools.wraps(func)
    def decorated(*args):
        wrapped = errormanager(func)
        wrapped(*args)

        INFO_ACCOUNT.append(len(TARGET.CREDENTIALS))
        if len(INFO_ACCOUNT) == 2:
            if INFO_ACCOUNT[1] > INFO_ACCOUNT[0]:
                if SETTING.SHOW_PROMPT:
                    infoMsg = "[?] Account valid? (Y/n)> "
                    jawaban = raw_input(infoMsg).lower()
                    if jawaban.startswith("n"):
                        # hapus kredensial
                        TARGET.CREDENTIALS.pop(-1)

            INFO_ACCOUNT.pop(0)

        if SETTING.MAX_CREDENTIAL is not None:
            credType = "account" if len(args) != 1 else "password"
            if len(TARGET.CREDENTIALS) == SETTING.MAX_CREDENTIAL:
                infoMsg = "The '--max-cred' option is used. "
                infoMsg += "the process of finding an %s has reached the limit. " % repr(credType)
                infoMsg += "try with a value greater than '%d' (e.g. %d)"
                infoMsg %= (SETTING.MAX_CREDENTIAL, SETTING.MAX_CREDENTIAL * 2)
                logger.info(infoMsg)

                raise BrutemapStopBruteForceException

    return decorated
