# -*- coding: utf-8 -*-

import platform

import logging
from logging.handlers import SysLogHandler

system_str = platform.system()

if system_str == "Linux":
    logformat = "%(levelname)-9s %(filename)s %(funcName)s %(lineno)-4d %(message)s"

    handler = SysLogHandler("/dev/log", SysLogHandler.LOG_LOCAL1)
    handler.setFormatter(logging.Formatter(logformat))

    logger = logging.getLogger("web")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

else:
    logger = type("Log", (object,), {})()

    logger.debug = lambda x: x
    logger.info = lambda x: x
    logger.warn = lambda x: x
    logger.error = lambda x: x

