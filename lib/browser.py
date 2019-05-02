#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

from selenium.webdriver.remote.remote_connection import RemoteConnection

from lib.data import SETTING
from lib.manager import errormanager

class _Browser(object):
    """
    Kelas ini digunakan untuk membungkus
    instan objek dari :mod:`selenium.webdriver`.
    """

    def get(self, url):
        """
        Buka situs dan handle koneksi error
        """

        # Atur socket timeout
        RemoteConnection.set_timeout(SETTING.SOCKET_TIMEOUT)

        wrapped = errormanager(SETTING.BROWSER.get)
        wrapped(url)

    @property
    def page_source(self):
        """
        Untuk WebKitGTK() tidak bisa mengambil sumber halaman.
        """

        script = "return document.getElementsByTagName('html')[0].innerHTML"
        html = self.execute_script(script)
        return html

    def __getattr__(self, name):
        object_ = getattr(SETTING.BROWSER, name)
        if callable(object_):
            object_ = errormanager(object_)
        return object_

browser = _Browser()
