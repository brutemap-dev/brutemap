#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Firefox
from selenium.webdriver import Chrome
from selenium.webdriver import WebKitGTK
from selenium.webdriver import Edge
from selenium.webdriver import Safari
from selenium.webdriver import PhantomJS
from selenium.webdriver import BlackBerry
from selenium.webdriver import Android
from selenium.webdriver.support.ui import WebDriverWait

from lib.browser import browser
from lib.data import logger
from lib.data import SETTING
from lib.data import TARGET
from lib.exceptions import BrutemapSkipTargetException

def initWebDriver():
    """
    Menemukan WebDriver yang terpasang.
    """

    infoMsg = "Finding web driver..."
    logger.info(infoMsg)

    webdriver = [Firefox, Chrome, WebKitGTK, Edge, Safari, PhantomJS, BlackBerry, Android]
    for driver in webdriver:
        try:
            infoMsg = "Trying %s ..." % str(driver)
            logger.info(infoMsg)

            _browser = driver()
            infoMsg = "WebDriver found: %s" % str(driver)
            logger.info(infoMsg)

            # simpan WebDriver, untuk digunakan :func:`reinitWebDriver`.
            SETTING.WEB_DRIVER = driver
            # simpan objek instan WebDriver.
            SETTING.BROWSER = _browser
            return

        except WebDriverException:
            continue

        except Exception:
            continue

    errMsg = "You need to install a selenium webdriver first. "
    errMsg += "(visit 'https://www.seleniumhq.org/docs/03_webdriver.jsp')"
    logger.error(errMsg)

    raise SystemExit

def reinitWebDriver(reload_url=True):
    """
    Menginisialisasi ulang WebDriver
    """

    tryCloseWebDriver()

    SETTING.BROWSER = SETTING.WEB_DRIVER()
    if SETTING.HTTP_AUTH_HANDLER is None and TARGET.URL is not None:
        if reload_url:
            SETTING.BROWSER.get(TARGET.URL)

def waitingResult(condition, *args):
    wait = WebDriverWait(browser, 10)
    try:
        return wait.until(condition(args))
    except TimeoutException:
        criMsg = "There are no results from the function '%s'" % str(condition)
        logger.critical(criMsg)
        raise BrutemapSkipTargetException

def tryCloseWebDriver():
    """
    Menutup WebDriver
    """

    if SETTING.BROWSER is not None:
        try:
            SETTING.BROWSER.quit()
        except:
            pass
