#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import requests

from lib.brute.start import bruteForceAttack
from lib.parse.htmlform import getFormField
from lib.browser import browser
from lib.core import getFormElements
from lib.core import isSupportedTarget
from lib.core import registerInterruptHandler
from lib.data import logger
from lib.data import SETTING
from lib.data import TARGET
from lib.exceptions import BrutemapSkipTargetException
from lib.manager import errormanager

def checkTarget(url):
    """
    Memeriksa jika target adalah target yang didukung.
    """

    infoMsg = "Checking target..."
    logger.info(infoMsg)

    response = None

    try:
        wrapped = errormanager(requests.get, False)
        response = wrapped(url)
    except Exception, e:
        logger.exception(e)
        raise BrutemapSkipTargetException

    if response.status_code == 401:
        infoMsg = "Login page type: 'HTTP AUTHENTICATION'"
        logger.info(infoMsg)

        TARGET.URL = response.url
        header = response.headers.get("www-authenticate")
        if not header:
            criMsg = "Cannot find HTTP Authentication type. "
            criMsg += "url %s there is no HTTP header 'WWW-Authenticate'" % repr(url)
            logger.critical(criMsg)

            raise BrutemapSkipTargetException

        else:
            authType = header.split(" ", 1)[0].lower()

        auth_handler = None
        if authType == "basic":
            auth_handler = requests.auth.HTTPBasicAuth

        elif authType == "digest":
            auth_handler = requests.auth.HTTPDigestAuth

        else:
            warnMsg = "Unsupported HTTP authentication (%s). " % repr(authType.capitalize())
            logger.warn(warnMsg)
            infoMsg = "Enter HTTP authentication handler (for 'python-requests'). "
            infoMsg += "(press 'CTRL-C' to exit)"
            logger.info(infoMsg)

            registerInterruptHandler(reset=True)

            skip_target = False
            while not skip_target:
                try:
                    auth_handler = __import__(raw_input("[#] (e.g. 'requests.auth.HTTPDigestAuth')> "))
                    if issubclass(auth_handler, requests.auth.AuthBase) and \
                        not auth_handler is requests.auth.AuthBase:
                        break

                except KeyboardInterrupt:
                    print
                    skip_target = True

                except Exception, e:
                    logger.exception(e)

            registerInterruptHandler()
            if skip_target:
                raise BrutemapSkipTargetException

        infoMsg = "HTTP authentication type: %s" % authType.capitalize()
        logger.info(infoMsg)
        SETTING.HTTP_AUTH_HANDLER = auth_handler

    else:
        SETTING.HTTP_AUTH_HANDLER = response = None
        browser.get(url)

    form_elements = [] if response is not None else getFormElements()
    if len(form_elements) > 0:
        fields = getFormField()
        status, pageType = isSupportedTarget(fields)

        if not status:
            criMsg = "Unsupported target"
            logger.critical(criMsg)

            raise BrutemapSkipTargetException

        else:
            TARGET.URL = str(browser.current_url)
            infoMsg = "Login page type: %s" % repr(pageType)
            logger.info(infoMsg)
            bruteForceAttack(fields)

    elif response is not None:
        bruteForceAttack((), http_auth=response)

    else:
        criMsg = "Unsupported target"
        logger.critical(criMsg)

        raise BrutemapSkipTargetException
