#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

from lib.settings import IS_PY3K

if IS_PY3K:
    # modul di py3k
    # reference: https://stackoverflow.com/questions/3783995/how-do-you-check-if-an-object-is-an-instance-of-file
    import io
    import urllib.parse as urlparse

    # disesuaikan untuk kompatibel py2k
    file = io.IOBase
    raw_input = input
    xrange = range

    def next(iterator):
        return iterator.__next__()

    # disesuaikan untuk kompatibel py2k
    def get_items(d):
        return list(d.items())

else:
    # modul di py2
    from __builtin__ import file, raw_input, xrange
    import urlparse

    def get_items(d):
        return d.items()

    # disesuaikan untuk kompatibel py3k
    def next(iterator):
        return iterator.next()
