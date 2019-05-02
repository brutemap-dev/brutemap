#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import functools
import re

from lib.data import SETTING
from lib.exceptions import BrutemapNullValueException
from lib.settings import EMAIL_REGEX

def emailGenerator(object_):
    """
    Menambahkan domain ke username
    jika username tidak memiliki ``domain``
    """

    @functools.wraps(object_)
    def wrapper():
        for account in object_():
            if account is None:
                break

            u, p = account
            try:
                for d in SETTING.DOMAINS:
                    if not re.search(EMAIL_REGEX, u):
                        yield u + "@" + d, p
                    else:
                        yield u, p

            except BrutemapNullValueException:
                pass

        yield

    return wrapper

def sqliPayloadsGenerator(object_):
    """
    Menambahkan SQLi payloads ke username/password
    """

    @functools.wraps(object_)
    def wrapper():
        for account in object_():
            if account is None:
                break

            u, p = None, None
            try:
                u, p = account
            except ValueError:
                p = account

            try:
                for payload in SETTING.SQLI_PAYLOADS:
                    if u is None:
                        yield p + payload
                    else:
                        yield u + payload, p

            except BrutemapNullValueException:
                pass

        yield

    return wrapper
