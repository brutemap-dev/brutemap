#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import time

from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait

from lib.browser import browser
from lib.data import logger
from lib.data import SETTING
from lib.data import TARGET
from lib.exceptions import BrutemapSkipTargetException
from lib.exceptions import BrutemapQuitException
from lib.settings import WEB_DRIVER

def getWebDriver():
    """
    Mendapatkan webdriver yang terinstall
    """

    wd_name = SETTING.USE_WEBDRIVER
    if wd_name is not None:
        wd_name = wd_name.lower()
        if wd_name in WEB_DRIVER:
            driver = [WEB_DRIVER[wd_name]]
        else:
            criMsg = "Unknown webdriver %s (choose from: %r)" % (repr(wd_name), list(WEB_DRIVER.keys()))
            logger.critical(criMsg)
            raise BrutemapQuitException
    else:
        driver = list(WEB_DRIVER.values())

    return driver  

def initWebDriver():
    """
    Menemukan WebDriver yang terpasang.
    """

    if SETTING.USE_WEBDRIVER is None:
        infoMsg = "Finding web driver..."
        logger.info(infoMsg)

    for driver in getWebDriver():
        try:
            infoMsg = "%s %s ..." % ("Trying" if not SETTING.USE_WEBDRIVER else "Using", str(driver))
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

    errMsg = "Cannot find webdriver%s. " % (" %s" % repr(SETTING.USE_WEBDRIVER) if SETTING.USE_WEBDRIVER else "")
    errMsg += "(visit 'https://www.seleniumhq.org/docs/03_webdriver.jsp') "
    errMsg += "for further information"
    logger.error(errMsg)

    raise BrutemapQuitException

def reinitWebDriver(reload_url=True):
    """
    Menginisialisasi ulang WebDriver
    """

    tryCloseWebDriver()

    SETTING.BROWSER = SETTING.WEB_DRIVER()
    if SETTING.HTTP_AUTH_HANDLER is None and TARGET.URL is not None:
        if reload_url:
            SETTING.BROWSER.get(TARGET.URL)
            # menunggu untuk selesai memuat halaman.
            time.sleep(SETTING.WEBDRIVER_TIMEOUT)

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
