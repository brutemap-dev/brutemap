#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

class BrutemapException(Exception):
    """
    Base exception
    """
    pass

class BrutemapSkipTargetException(BrutemapException):
    """
    Exception untuk melewati target
    """
    pass

class BrutemapNullValueException(BrutemapException):
    """
    Exception untuk ``data`` sudah habis
    """
    pass

class BrutemapNextTargetException(BrutemapException):
    """
    Exception untuk target berikutnya (jika sudah selesai)
    """
    pass

class BrutemapStopBruteForceException(BrutemapException):
    """
    Exception untuk menghentikan sesi brute force
    """
    pass

class BrutemapQuitException(BrutemapException):
    """
    Exception untuk keluar program
    """
    pass
