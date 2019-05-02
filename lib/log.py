#!/usr/bin/env python

"""
Brutemap is (c) 2019 By Brutemap Development Team.
See LICENSE for details.
"""

import logging
import sys

from lib.utils.logger import ColorizedStreamHandler

LOGGER = logging.getLogger("Brutemap")
FORMATTER = logging.Formatter("\r[%(asctime)s] [%(name)s] %(levelname)s: %(message)s", "%H:%M:%S")
HANDLER = ColorizedStreamHandler(sys.stdout)
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)
LOGGER.setLevel(logging.INFO)
