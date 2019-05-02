#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

from argparse import HelpFormatter
from backports.shutil_get_terminal_size import get_terminal_size

from lib.settings import IS_WINDOWS

class PrettyHelpFormatter(HelpFormatter):
    """
    Help Formatter untuk :mod:`argparse`
    Ini akan menampilkan opsi, seperti ini:

    Output:
        -s, --long
        -s, --long <value>
    """

    def __init__(self, *args, **kwargs):
        kwargs["width"] = get_terminal_size()[0] - 2
        HelpFormatter.__init__(self, *args, **kwargs)

    def _format_action_invocation(self, action):
        if not action.option_strings:
            metavar, = self._metavar_formatter(action, action.dest)(1)
            return metavar

        else:
            parts = []
            for opt in action.option_strings:
                parts.append(opt)

            opt_string = ", ".join(parts)
            if action.nargs != 0:
                dest = action.metavar or action.dest
                metavar = "<%s>" % dest.lower()
                opt_string += " " + metavar

            return opt_string

    def _format_usage(self, usage, actions, groups, prefix):
        usage = HelpFormatter._format_usage(self, usage, actions, groups, prefix)
        parts = usage.split(" ", 2)
        prog = parts[1]
        parts[1] = (prog if IS_WINDOWS else "python " + prog)
        return " ".join(parts)
