#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import string
import sys

from selenium.webdriver import Firefox
from selenium.webdriver import Chrome
from selenium.webdriver import WebKitGTK
from selenium.webdriver import Edge
from selenium.webdriver import Ie
from selenium.webdriver import Safari
from selenium.webdriver import PhantomJS
from selenium.webdriver import Android
from termcolor import colored

AUTHOR = "Aprila Hijriyan"
VERSION = "1.1"
VERSION_STATUS = "4"
VERSION_STRING = "%s.%s" % (VERSION, VERSION_STATUS)
TOOL_NAME = "brutemap"
DESCRIPTION = "Let's find someone's account"
HOMEPAGE = "https://brutemap-dev.github.io"
GIT_PAGE = "https://github.com/brutemap-dev/brutemap"
ISSUE_LINK = "https://github.com/brutemap-dev/brutemap/issues"

BANNER = """\033[01;31m\
 _              _                         
| |_  ___  _ _ | |_  ___  _____  ___  ___ 
| . ||  _|| | ||  _|| -_||     || .'|| . |\033[0;1m
|___||_|  |___||_|  |___||_|_|_||__,||  _|
                                     |_|  
              %s v%s
      %s\n
""" % (
    colored(TOOL_NAME, "red", attrs=["bold"]),
    VERSION_STRING,
    colored(HOMEPAGE, "white", attrs=["bold", "underline"])
)

# reference: https://www.w3schools.com/css/css_table.asp
HTML_FORMAT = string.Template("""\
<html>
    <title>Brutemap - Let's find someone's account</title>
    <head>
        <style type=\"text/css\">
            #result_brutemap {
                font-family: \"Trebuchet MS\", Arial, Helvetica, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }

            #result_brutemap td, #result_brutemap th {
                border: 1px solid #ddd;
                padding: 8px;
            }

            #result_brutemap tr:nth-child(even) {
                background-color: #f2f2f2;
            }

            #result_brutemap tr:hover {
                background-color: #ddd;
            }

            #result_brutemap th {
                padding-top: 12px;
                padding-bottom: 12px;
                text-align: left;
                background-color: ${bg_color};
                color: white;
            }
        </style>
    </head>
    <body>
        ${html_table}
    </body>
</html>\
""")

SEPARATOR_REGEX = r"[,\s]*"

EMAIL_REGEX = r"[\w.-]+@[\w.-]+"

URL_SCHEMES = ("http://", "https://")

SPINNER_CHARS = ["|", "/", "-", "\\"]

WEB_DRIVER = {
    "firefox": Firefox,
    "chrome": Chrome,
    "gtk": WebKitGTK,
    "edge": Edge,
    "ie": Ie,
    "safari": Safari,
    "phantomjs": PhantomJS,
    "android": Android
}

IS_PY3K = sys.version_info[0] == 3

# for python 3.4, because it doesn't have the mswindows attribute.
IS_WINDOWS = sys.platform.startswith("win")
