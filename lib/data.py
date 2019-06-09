#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import os
import signal

from lib.log import LOGGER
from lib.path import getPath

class SETTING:
    """
    Pengaturan brutemap
    """

    # mengabaikan interupsi, jika proses menyimpan hasil brute force sedang berlangsung.
    IGNORE_INTERRUPT = False
    # objek kelas web driver.
    WEB_DRIVER = None
    # instan objek kelas web driver.
    BROWSER = None
    # untuk mengetahui jika sesi brute force sedang berlangsung.
    BRUTE_SESSION = False
    # daftar target.
    TARGETS = None
    # daftar username.
    USERNAMES = None
    # daftar password.
    PASSWORDS = None
    # daftar email domain.
    DOMAINS = None
    # untuk mengetahui jika autentikasi target (bidang form) (user) menggunakan *email*.
    IS_EMAIL_AUTHENTICATION = False
    # untuk mengetahui jika autentikasi target adalah web shell.
    IS_WEBSHELL_AUTHENTICATION = False
    # socket timeout.
    SOCKET_TIMEOUT = None
    # batas mengulang koneksi.
    MAX_RETRY = None
    # waktu tunggu koneksi (jika koneksi bermasalah).
    DELAY = None
    # daftar regex untuk target.
    REGEX_MAP = None
    # perintah untuk memunculkan *prompt* pada saat menemukan akun berpotensi.
    SHOW_PROMPT = False
    # batas menemukan akun berpotensi.
    MAX_CREDENTIAL = None
    # mode pengambilan akun di daftar.
    TWIN_MODE = False
    # menggunakan sqli payloads sebagai *akun*.
    SQLI_BYPASS_MODE = False
    # menambahkan sqli payloads ke *akun*.
    USE_SQLI_PAYLOADS = False
    # daftar sqli payloads.
    SQLI_PAYLOADS = None
    # webdriver yang digunakan.
    USE_WEBDRIVER = None
    # waktu tunggu proses memuat halaman
    WEBDRIVER_TIMEOUT = None
    # output file.
    OUTPUT = None
    # untuk *python-requests*.
    HTTP_AUTH_HANDLER = None
    # paksa keluar, jika anda menekan tombol CTRL-C/Z berkali-kali.
    EXIT_NOW = False

    @classmethod
    def init(cls, items):
        """
        Memperbaharui nilai pengaturan
        """

        for (k, v) in items:
            k = k.upper()
            if hasattr(cls, k):
                setattr(cls, k, v)

class DEFAULT:
    """
    Data bawaan brutemap
    """

    # lokasi file (daftar username) bawaan.
    USERNAMES = os.path.join(getPath(), os.path.join("data", "usernames.txt"))
    # lokasi file (daftar password) bawaan.
    PASSWORDS = os.path.join(getPath(), os.path.join("data", "passwords.txt"))
    # lokasi file (daftar email domain) bawaan.
    DOMAINS = os.path.join(getPath(), os.path.join("data", "emaildomains.txt"))
    # lokasi file (daftar SQLi payloads) bawaan.
    SQLI_PAYLOADS = os.path.join(getPath(), os.path.join("data", "sqlipayloads.txt"))
    # socket timeout bawaan.
    SOCKET_TIMEOUT = 25.0
    # waktu tunggu memuat halaman bawaan.
    WEBDRIVER_TIMEOUT = 5.0
    # batas mengulang koneksi bawaan.
    MAX_RETRY = 5
    # waktu tunggu koneksi bawaan.
    DELAY = 3.0
    # nama file bawaan.
    FILENAME = "result"
    # ekstensi file.
    FILE_EXTENSION = "html"
    # nama file hasil (bawaan) yang akan digunakan.
    OUTPUT = ""
    # root direktori brutemap.
    ROOT_PATH = os.path.join(os.getenv("HOME", os.getcwd()), ".brutemap")
    # output directory bawaan
    OUTPUT_DIRECTORY = os.path.join(ROOT_PATH, "output")
    # direktori pesan lengkap pengecualian
    ERROR_DIRECTORY = os.path.join(ROOT_PATH, "error")
    # interrupt handler bawaan
    INTERRUPT_HANDLER = signal.getsignal(signal.SIGINT)

class TARGET:
    """
    Data target
    """

    URL = None
    PAGE = None
    CREDENTIALS = []

class STATUS:
    """
    Status akun
    """

    OK = "OK"
    NO = "NO"

logger = LOGGER
