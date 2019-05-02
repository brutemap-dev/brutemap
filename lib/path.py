#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import os

_BASE_PATH = None

def setPath(_):
    """
    Mengatur base path, digunakan untuk
    mengambil ``data`` brutemap yang ada di
    directory **data**.
    """

    global _BASE_PATH
    _BASE_PATH = os.path.dirname(os.path.realpath(_))

def getPath():
    """
    Mendapatkan ``base path`` *brutemap*.
    Untuk digabungkan dengan daftar ``data`` bawaan
    brutemap.
    """

    return _BASE_PATH
