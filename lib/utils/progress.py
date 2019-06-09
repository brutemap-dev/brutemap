#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import itertools

from lib.compat import next
from lib.core import stdoutWrite
from lib.settings import SPINNER_CHARS

class Spinner(object):
    def __init__(self, message, maxval=None):
        self.marker = itertools.cycle(SPINNER_CHARS)
        self.message = message
        self.curval = 0
        self.maxval = maxval or 100
        self._width = 0

        stdoutWrite(message)

    @property
    def percent(self):
        return (self.curval * 100) / self.maxval

    def write(self, msg):
        backspace = "\b" * self._width
        newmsg = backspace + msg.ljust(self._width)
        stdoutWrite(newmsg)
        self._width = max(self._width, len(msg))

    def show_progress(self):
        self.curval += 1
        progress = "%d%% %s" % (self.percent, next(self.marker))
        self.write(progress)

    def done(self):
        stdoutWrite("\b")
        stdoutWrite("(done)\n")
