#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import logging
import os
import re

from colorama import ansi
from colorama import AnsiToWin32
from colorama import Fore
from colorama import Style

from lib.settings import IS_WINDOWS

class ColorizedStreamHandler(logging.StreamHandler):
    color_map = {
        logging.INFO: Fore.LIGHTGREEN_EX,
        logging.ERROR: Fore.LIGHTRED_EX,
        logging.WARNING: Fore.LIGHTYELLOW_EX,
        logging.CRITICAL: ansi.code_to_chars("41")
    }
    def __init__(self, stream):
        logging.StreamHandler.__init__(self, stream)

        if IS_WINDOWS:
            stream = AnsiToWin32(stream)

        self.stream = stream
        self.record = None

    def colored(self):
        """
        Cek jika pesan bisa di warnai
        """

        _ = self.stream
        if isinstance(_, AnsiToWin32):
            _ = _.wrapped

        if hasattr(_, "isatty") and _.isatty():
            return True

        if os.getenv("TERM", "").lower() == "ansi":
            return True

        return False

    def emit(self, record):
        """
        Cetak pesan
        """

        try:
            message = self.format(record) + "\n"
            self.stream.write(message)

            if hasattr(self.stream, "flush"):
                self.stream.flush()

        except (SystemExit, KeyboardInterrupt):
            raise
        except IOError:
            pass
        except:
            self.handleError(record)

    def colorize(self, msg):
        """
        Mewarnai pesan
        """

        color = self.color_map[self.record.levelno]
        reset = Style.RESET_ALL
        levelname = reset + color + self.record.levelname + reset
        if self.record.levelname == "CRITICAL":
            color = self.color_map[logging.ERROR]

        name = Fore.LIGHTBLUE_EX + self.record.name + reset
        message = self.record.message
        # XXX: kenapa cara dibawah ini tidak bekerja?
        #
        # match = re.findall(r"['\"]+(.*?)['\"]+", message)
        # if match:
        #     match.reverse()
        #     for m in match:
        #         message = message.replace(m, color + m + reset, 1)

        match = re.search(r"=> (?P<account>.*?(?:| \: .*?)) \((?P<status>[A-Z]+)\)", message)
        if match:
            account = match.group("account")
            status = match.group("status")
            if status == "NO":
                color_status = Fore.LIGHTRED_EX
            else:
                color_status = Fore.LIGHTGREEN_EX

            newmsg = message.replace(account, color_status + account + reset)
            newmsg = newmsg.replace(status, color_status + status + reset)
            msg = msg.replace(message, newmsg)

        asctime = re.findall(r"\[(.+?)\]", msg)[0]
        msg = msg.replace(asctime, Fore.LIGHTMAGENTA_EX + asctime + reset, 1)
        msg = msg.replace(self.record.name, name, 1)
        msg = msg.replace(self.record.levelname, levelname, 1)
        msg = msg + reset

        return msg

    def format(self, record):
        """
        Format pesan
        """

        self.record = record
        msg = logging.StreamHandler.format(self, record)
        if self.colored():
            msg = self.colorize(msg)

        return msg
