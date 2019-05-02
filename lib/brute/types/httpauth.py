#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import requests

from lib.data import logger
from lib.data import SETTING
from lib.data import STATUS
from lib.data import TARGET
from lib.manager import brutemanager
from lib.manager import errormanager
from lib.exceptions import BrutemapStopBruteForceException

@brutemanager
def login(username, password):
    handler = SETTING.HTTP_AUTH_HANDLER(username, password)
    wrapped = errormanager(requests.get, False)
    r = wrapped(TARGET.URL, auth=handler)
    if r.status_code == 200:
        status = STATUS.OK
    else:
        status = STATUS.NO

    infoMsg = "Account => %s : %s (%s)" % (username, password, status)
    logger.info(infoMsg)

    if status == STATUS.OK:
        TARGET.CREDENTIALS.append((username, password))
        raise BrutemapStopBruteForceException
