#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

from lib.core import randomHexColor
from lib.settings import HTML_FORMAT

class HtmlWriter(object):
    """
    Pembuat file hasil (ekstensi .html)
    """

    def __init__(self, fp, fieldnames):
        self.fp = fp
        self.fieldnames = fieldnames
        self._html_table = "<table id=\"result_brutemap\">\n"

        self.init()

    def init(self):
        self._html_table += "            <tr>\n"
        for header in self.fieldnames:
            self._html_table += "                <th>%s</th>\n" % header
        self._html_table += "            </tr>\n"

    def add_rows(self, *args):
        self._html_table += "            <tr>\n"
        for _ in args:
            self._html_table += "                <td>%s</td>\n" % _
        self._html_table += "            </tr>\n"

    def close(self):
        """
        tutup file dan simpan
        """

        self._html_table += "        </table>"
        html = HTML_FORMAT.substitute(html_table=self._html_table, bg_color=randomHexColor())
        self.fp.write(html)
        self.fp.close()
