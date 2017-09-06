#!/usr/bin/env python
# coding=utf-8
import sys

__author__ = 'revol'

from sys import stderr, stdout
from datetime import datetime
import json
import os

from mongodbhandler import MongodbHandler
from levels import Levels

MAX_LOG_COUNT = 99999
MONGODB_DEFAULT_CONFIG = {
    "host": "127.0.0.1",
    "port": 27017,
    "username": "admin",
    "password": "123456",
    "database": "maizi_log",
    "collection": "calc_log",
    "capped": False,
    "size": 10000,  # bytes
    "max": MAX_LOG_COUNT,
    "log_frame": False,
    "level": Levels.INFO
}


class L2M(object):
    levels = Levels

    def __init__(self, config=None):
        self.__name__ = 'default'
        self.config = MONGODB_DEFAULT_CONFIG
        # global L2M_BASIC_CONFIG
        self.config.update(json.loads(os.environ.get('L2M_BASIC_CONFIG','{}')))
        self.config.update(config  or {})
        mongodb_handler = self._init_mongodb_handler(self.config)
        self.handlers = [mongodb_handler]

    def _init_mongodb_handler(self, config):
        handler = MongodbHandler(config)
        return handler

    @staticmethod
    def basicConfig(config):
        cfg=json.loads(os.environ.get('L2M_BASIC_CONFIG','{}'))
        cfg.update(config or {})
        os.environ.update({'L2M_BASIC_CONFIG' : json.dumps(cfg)})

    @classmethod
    def getLogger(cls, name='default', config=None):
        rt = cls(config or {})
        setattr(rt, '__name__', name)
        return rt

    def setLevel(self, level):
        self.config.update({'level': level})

    def addHandler(self, handler):
        self.handlers.append(handler)

    def _log(self, record, level):
        if self.config.get('level') is not self.levels.DEBUG:
            if level == self.levels.DEBUG:
                return
        # stdout.write(datetime.now().ctime() + ':' + level + ':' + str(record))
        for handler in self.handlers:
            handler.emit(record, level)

    def error(self, e, **kwargs):
        frame_depth=kwargs.pop('frame_depth',0)
        record = {'exception': e,
                  'frame': sys._getframe(frame_depth + 1)}
        record.update(kwargs or {})
        stderr.write(datetime.now().ctime() + ':' + self.levels.ERROR + ':' + str(record))
        self._log(record, level=self.levels.ERROR)

    def debug(self, msg, **kwargs):
        frame_depth=kwargs.pop('frame_depth',0)
        record = {'debug_msg': msg,
                  'frame': sys._getframe(frame_depth + 1)}
        record.update(kwargs or {})
        self._log(record, level=self.levels.DEBUG)

    def warning(self, msg, **kwargs):
        frame_depth=kwargs.pop('frame_depth',0)
        record = {'warning_msg': msg,
                  'frame': sys._getframe(frame_depth + 1)}
        record.update(kwargs or {})
        self._log(record, level=self.levels.WARNING)


    def info(self, record):
        self._log(record, level=self.levels.INFO)

    def cache(self, record):
        self._log(record or {}, level=self.levels.CACHE)
