#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

from __future__ import print_function

import os
import platform
import random
import re
import signal
import sys
import time
import traceback

from backports.shutil_get_terminal_size import get_terminal_size
from colorama import init as coloramainit
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.support.expected_conditions import visibility_of_all_elements_located
from termcolor import colored

from lib.utils.wordlist import Wordlist
from lib.browser import browser
from lib.compat import get_items
from lib.compat import raw_input
from lib.compat import urlparse
from lib.data import DEFAULT
from lib.data import logger
from lib.data import SETTING
from lib.data import STATUS
from lib.data import TARGET
from lib.exceptions import BrutemapNullValueException
from lib.exceptions import BrutemapSkipTargetException
from lib.exceptions import BrutemapStopBruteForceException
from lib.exceptions import BrutemapQuitException
from lib.generator import emailGenerator
from lib.generator import sqliPayloadsGenerator
from lib.settings import BANNER
from lib.settings import HOMEPAGE
from lib.settings import SEPARATOR_REGEX
from lib.settings import TOOL_NAME
from lib.settings import URL_SCHEMES
from lib.settings import VERSION_STRING
from lib.webdriver import reinitWebDriver
from lib.webdriver import tryCloseWebDriver
from lib.webdriver import waitingResult

def stdoutWrite(msg):
    """
    Mencetak pesan ke terminal
    """

    try:
        sys.stdout.write(msg)
        sys.stdout.flush()

    except IOError:
        pass

def printBanner():
    """
    Mencetak banner brutemap ke terminal
    """

    coloramainit()
    stdoutWrite(BANNER)

def printVersion():
    """
    Mencetak versi tool
    """

    msg = "%s version %s\n" % (TOOL_NAME.capitalize(), VERSION_STRING)
    stdoutWrite(msg)

def randomHexColor():
    """
    Warna acak untuk hasil file format (.html)
    """

    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    color = "#%x%x%x" % (r, g, b)
    return color

def printStatus(start=True):
    """
    Mencetak pesan status jika brutemap sedang berjalan atau tidak
    """

    msg = "\n[%s] ( %s ) %s at %s\n\n"
    char, status = ("*", "Starting") if start else ("-", "Die")
    msg %= (
        char,
        colored(HOMEPAGE, "green", attrs=["bold", "underline"]),
        status,
        time.strftime("%X")
    )
    stdoutWrite(msg)

    if not start:
        tryCloseWebDriver()

def interruptHandler(signum, frame):
    """
    Fungsi untuk menghandle sinyal interupsi dari tombol
    CTRL-C dan CTRL-Z.
    """

    if SETTING.IGNORE_INTERRUPT:
        return

    print()
    registerInterruptHandler(reset=True)

    try:
        msg = "[?] What do you want? [(C)ontinue (default) / (s)kip target / (q)uit]: "
        jawaban = (raw_input(msg) or "c").lower()
        if jawaban.startswith("c"):
            pass

        elif jawaban.startswith("s"):
            raise BrutemapSkipTargetException

        elif jawaban.startswith("q"):
            errMsg = "User quit"
            logger.error(errMsg)

            raise BrutemapQuitException

    except KeyboardInterrupt:
        print()

        errMsg = "User aborted"
        logger.error(errMsg)

        if SETTING.BRUTE_SESSION:
            SETTING.EXIT_NOW = True
            raise BrutemapStopBruteForceException

        raise BrutemapQuitException

    # XXX: ketika sinyal interupsi didapat, webdriver otomatis ketutup?
    reinitWebDriver()
    registerInterruptHandler()

def registerInterruptHandler(reset=False):
    """
    Mendaftarkan interrupt handler
    """

    handler = DEFAULT.INTERRUPT_HANDLER
    if not reset:
        handler = interruptHandler

    # sinyal CTRL-C
    signal.signal(signal.SIGINT, handler)
    # sinyal CTRL-Z
    signal.signal(signal.SIGTSTP, handler)

def createList(object_):
    """
    Membuat objek list
    """

    return re.split(SEPARATOR_REGEX, object_)

def createWordlist(object_):
    """
    Mengkonversikan ``object`` ke ``file-like`` object
    """

    wordlist = Wordlist(createList(object_))
    return wordlist

def autoCompleteUrl(url):
    """
    Menambahkan bagian url (``scheme``) jika belum ditambahkan.
    """

    if not url.startswith(URL_SCHEMES):
        url = URL_SCHEMES[0] + url
    return url

def getPage(url):
    """
    Mendapatkan ``halaman`` terakhir situs.
    Ini digunakan untuk proses verifikasi akun.
    """

    page = urlparse.urlparse(url).path
    if page.endswith("/"):
        page = page.rstrip("/")

    page = page.split("/")[-1]
    return page

def verifyAccount():
    """
    Verifikasi jika akun valid
    """

    re_scan = False # memeriksa kembali menggunakan regex.
    status = STATUS.NO
    regex = None
    if SETTING.REGEX_MAP is not None:
        host = urlparse.urlparse(TARGET.URL).netloc
        regex = SETTING.REGEX_MAP.get(host) # memeriksa jika target, memiliki regex.

    page, is_slide = TARGET.PAGE, False
    if isinstance(TARGET.PAGE, list):
        page, is_slide = TARGET.PAGE[0], True

    if not re.search(re.escape(page), browser.current_url):
        # jika halaman berubah, kemungkinan akun valid.
        status = STATUS.OK
        if is_slide:
            if not TARGET.PASSWORD_TESTED:
                # kemungkinan, username tidak valid.
                status = STATUS.NO
            else:
                TARGET.PASSWORD_TESTED = False
                re_scan = True
        else:
            re_scan = True

    if re_scan and regex is not None:
        # memeriksa halaman, menggunakan regex.
        if re.search(regex, browser.page_source):
            status = STATUS.OK
        else:
            status = STATUS.NO

    return status

def getCssSelector(type_):
    """
    Membuat CSS Selector (``input element``).
    Ini digunakan untuk mengetahui jika situs memiliki bidang ``Admin``.
    """

    return "input[type='%s']" % type_

def getFormElements():
    """
    Mendapatkan daftar ``form`` element, dari halaman situs.
    """

    elems = waitingResult(visibility_of_all_elements_located, By.TAG_NAME, "form") or []
    return elems

def findElement(parent, css_selector):
    """
    Menemukan element dengan CSS Selector.
    """

    try:
        elem = waitingResult(visibility_of_element_located, By.CSS_SELECTOR, css_selector)
        return elem
    except NoSuchElementException:
        return None

def isStandardLoginPage(object_):
    """
    Memeriksa jika form adalah ``standard`` halaman login
    """

    return all(object_)

def isWebShellLoginPage(object_):
    """
    Memeriksa jika form adalah halaman login ``web shell``
    """

    return object_[1] is None

def isSlideLoginPage(object_):
    """
    Memeriksa jika form adalah halaman login tipe ``slide``, seperti halaman login akun google.
    """

    return object_[-1] is None

def isSupportedTarget(object_):
    """
    Memeriksa jika target adalah ``target`` yang didukung.

    Tipe target yang didukung:
        * standard login page
        * webshell login page
        * slide login page
        * HTTP otentikasi

    """

    if isStandardLoginPage(object_):
        return True, "STANDARD"

    elif isWebShellLoginPage(object_):
        if not SETTING.IS_WEBSHELL_AUTHENTICATION:
            SETTING.IS_WEBSHELL_AUTHENTICATION = True

        return True, "WEBSHELL"

    elif isSlideLoginPage(object_):
        return True, "SLIDE"

    else:
        return False, None

def accountGenerator():
    """
    Akun generator
    """

    if SETTING.IS_WEBSHELL_AUTHENTICATION:
        try: # pertama, uji menggunakan username
            for user in SETTING.USERNAMES:
                yield user

        except BrutemapNullValueException:
            try: # kedua, uji password
                for passw in SETTING.PASSWORDS:
                    yield passw

            except BrutemapNullValueException:
                pass

    elif not SETTING.TWIN_MODE:
        try: # uji username dengan semua password
            for user in SETTING.USERNAMES:
                try:
                    for passw in SETTING.PASSWORDS:
                        yield user, passw

                except BrutemapNullValueException:
                    pass

        except BrutemapNullValueException:
            pass

    else:
        try:
            # uji username berdasarkan total password
            for user in SETTING.USERNAMES:
                try:
                    passw = SETTING.PASSWORDS.next()
                    yield user, passw

                except BrutemapNullValueException:
                    # password habis
                    break

        except BrutemapNullValueException:
            pass

    yield

def getAccount():
    """
    Mendapatkan daftar akun/password
    """

    registerInterruptHandler(reset=True)

    re_init = False
    gen = accountGenerator

    if SETTING.IS_EMAIL_AUTHENTICATION:
        jawaban = ""
        infoMsg = "[?] Do you want to add an email domain to '%s'? (y/n)> "
        infoMsg %= urlparse.urlsplit(TARGET.URL).netloc
        try:
            jawaban = raw_input(infoMsg).lower()
        except KeyboardInterrupt:
            re_init = True
            print()

        if jawaban.startswith("y"):
            domains = ""
            try:
                domains = raw_input("[#] Enter domain (e.g. 'google.com, yahoo.com')> ")
            except KeyboardInterrupt:
                re_init = True
                print()

            for _ in re.split(SEPARATOR_REGEX, domains):
                if _:
                    SETTING.DOMAINS.append(_)

        gen = emailGenerator(gen)

    if SETTING.SQLI_BYPASS_MODE:
        if SETTING.IS_WEBSHELL_AUTHENTICATION:
            jawaban = ""
            infoMsg = "[?] Do you want to use the 'SQL injection bypass authentication' technique "
            infoMsg += "in webshell authentication? > "
            try:
                jawaban = raw_input(infoMsg).lower()
            except KeyboardInterrupt:
                re_init = True
                print()

            if jawaban.startswith("n"):
                infoMsg = "Disable the 'SQL injection bypass authentication' technique..."
                logger.info(infoMsg)

                SETTING.SQLI_BYPASS_MODE = False
                SETTING.USERNAMES = createWordlist(DEFAULT.USERNAMES)
                SETTING.PASSWORDS = createWordlist(DEFAULT.PASSWORDS)

    if SETTING.USE_SQLI_PAYLOADS:
        abaikan = True
        if SETTING.IS_WEBSHELL_AUTHENTICATION:
            jawaban = ""
            infoMsg = "[?] Do you want to use the 'SQL injection bypass authentication' technique "
            infoMsg += "in webshell authentication? > "
            try:
                jawaban = raw_input(infoMsg).lower()
            except KeyboardInterrupt:
                re_init = True
                print()

            if jawaban.startswith("n"):
                SETTING.USE_SQLI_PAYLOADS = abaikan = False

        if abaikan:
            gen = sqliPayloadsGenerator(gen)

    if re_init:
        reinitWebDriver()

    registerInterruptHandler()

    infoMsg = "Starting attacks !!!"
    logger.info(infoMsg)

    return gen()

def makeDir(lok):
    """
    Buat dir jika ``dir`` belum dibuat
    """

    if not os.path.isdir(lok):
        os.mkdir(lok)

def _checkRootPath():
    """
    Memeriksa base ``dir`` *brutemap*
    """

    makeDir(DEFAULT.ROOT_PATH)

def _checkOutputDir():
    """
    Memeriksa output ``dir``
    """

    makeDir(DEFAULT.OUTPUT_DIRECTORY)

def _checkErrorDir():
    """
    Memeriksa error ``dir``
    """

    makeDir(DEFAULT.ERROR_DIRECTORY)

def initDir():
    """
    Memeriksa ``dir`` *brutemap*
    """

    _checkRootPath()
    _checkOutputDir()
    _checkErrorDir()

def getErrorMessage():
    """
    Mendapatkan pesan error, yang tidak ke handle.
    """

    errMsg = traceback.format_exception(*sys.exc_info())
    return "\n".join(errMsg)

def saveErrorMessage():
    """
    Simpan pesan error ke directory ``error`` *brutemap*
    """

    errMsg = "Running version: %s\n" % VERSION_STRING
    errMsg += "Python version: %s\n" % sys.version.split()[0]
    errMsg += "Operating system: %s\n" % platform.platform()
    errMsg += "Command line: %s\n" % re.sub(
        r".+?%s.py\b" % TOOL_NAME,
        "%s.py" % TOOL_NAME,
        " ".join(sys.argv)
    )
    errMsg += ("=" * get_terminal_size()[0]) + "\n"
    errMsg += getErrorMessage()
    filename = time.strftime("%d-%m-%Y_%X").replace(":", "-") + ".txt"
    filepath = os.path.join(DEFAULT.ERROR_DIRECTORY, filename)
    with open(filepath, "w") as fp:
        fp.write(errMsg)

    return filepath

def makeFile():
    """
    Membuat file hasil brute force
    """

    dirname = os.path.dirname(SETTING.OUTPUT)
    if not dirname:
        dirname = DEFAULT.OUTPUT_DIRECTORY
    elif not os.path.isdir(os.path.realpath(dirname)):
        warnMsg = "No such directory %s (using default %s)"
        warnMsg %= (repr(dirname), repr(DEFAULT.OUTPUT_DIRECTORY))
        logger.warn(warnMsg)
        dirname = DEFAULT.OUTPUT_DIRECTORY

    dirname = os.path.realpath(dirname)
    filename = os.path.basename(SETTING.OUTPUT)
    if not filename:
        filename = DEFAULT.FILENAME
    else:
        filename = filename.split(".", 1)[0]

    filename = filename + "-" + os.urandom(4).encode("hex") + "." + DEFAULT.FILE_EXTENSION
    filepath = os.path.join(dirname, filename)
    fp = open(filepath, "w")
    return fp

def initOptions(options):
    """
    Mengkonversikan nilai opsi
    """

    new = {}
    for (k, v) in options._get_kwargs():
        k = k.upper()
        if not v:
            if hasattr(DEFAULT, k):
                v = getattr(DEFAULT, k)

        if k.upper() in ("TARGETS", "USERNAMES", "PASSWORDS", "DOMAINS"):
            if isinstance(v, list):
                v = " ".join(v)
            v = createWordlist(v)

        new[k] = v

    SETTING.init(get_items(new))

def clearData():
    """
    Membersihkan data target sebelumnya
    """

    SETTING.IS_EMAIL_AUTHENTICATION = False
    SETTING.IS_WEBSHELL_AUTHENTICATION = False
    SETTING.PASSWORD_TESTED = False
    TARGET.CREDENTIALS = []
    TARGET.PAGE = None
    TARGET.URL = None
