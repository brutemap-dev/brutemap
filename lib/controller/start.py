#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

from __future__ import print_function

from lib.controller.target import checkTarget
from lib.core import autoCompleteUrl
from lib.core import clearData
from lib.core import initDir
from lib.core import registerInterruptHandler
from lib.core import saveErrorMessage
from lib.data import logger
from lib.data import SETTING
from lib.exceptions import BrutemapNextTargetException
from lib.exceptions import BrutemapNullValueException
from lib.exceptions import BrutemapSkipTargetException
from lib.exceptions import BrutemapQuitException
from lib.settings import ISSUE_LINK
from lib.webdriver import initWebDriver
from lib.webdriver import reinitWebDriver

def initialize():
    initDir()
    initWebDriver()

    try:
        for i, url in enumerate(SETTING.TARGETS):
            i += 1
            url = str(autoCompleteUrl(url))
            infoMsg = "Target url '%s' (%d)" % (url, i)
            logger.info(infoMsg)

            try:
                registerInterruptHandler()
                checkTarget(url)

            except BrutemapSkipTargetException:
                infoMsg = "Skipping target %s" % repr(url)
                logger.info(infoMsg)

            except BrutemapNextTargetException:
                pass

            registerInterruptHandler(reset=True)
            clearData()
            reinitWebDriver(reload_url=False)

    except (BrutemapNullValueException, BrutemapQuitException):
        pass

    except KeyboardInterrupt:
        print()
        errMsg = "User aborted"
        logger.error(errMsg)

    except:
        path = saveErrorMessage()
        errMsg = "An error has occurred! look at: %s (for full error messages). " % repr(path)
        errMsg += "And report to: %s (thanks!)" % repr(ISSUE_LINK)
        logger.error(errMsg)

    registerInterruptHandler(reset=True)
