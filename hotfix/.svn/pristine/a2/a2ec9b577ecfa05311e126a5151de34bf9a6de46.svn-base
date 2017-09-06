#!/usr/bin/env python
# coding=utf-8
__author__ = 'revol'

# use gevent to improve I/O
# You must call patch_all() *before* importing any other modules
# from gevent import monkey
# monkey.patch_all()

import sys
import logging
from datetime import datetime
import os

sys.path.append(os.path.abspath('../../libs'))

from bson import InvalidDocument

try:
    from pymongo import MongoClient
except ImportError:
    from pymongo import Connection as MongoClient

if sys.version_info[0] >= 3:
    unicode = str

from basehandler import BaseHandler
from levels import Levels


class MongodbHandler(BaseHandler):
    def __init__(self, config):
        BaseHandler.__init__(self)
        host = config['host']
        port = config['port']
        username = config['username']
        password = config['password']
        db = config['database']
        collection = config['collection']

        # if isinstance(collection, str):
        client = MongoClient(host, port, tz_aware=True)
        if username and password:
            client[db].authenticate(username, password)
        self.collection = client[db][collection]

    def emit(self, record, level, **kwargs):
        try:
            self.collection.insert_one(self.format(record, level))
        except InvalidDocument as e:
            logging.error("Unable to save log record: %s", e.message,
                          exc_info=True)

    def format(self, record, level):
        result = {'log_time': datetime.now(),
                  'log_level': level}
        if level == Levels.ERROR:
            # Format exception object as a string
            e = record.pop('exception')
            data=self.formatException(e)
            # if e.args:
            #     data.update(args=[unicode(arg) for arg in e.args])
            # data.update(
            #     username=getpass.getuser(),
            #     host=gethostname()
            # )
            result.update({'exception': data,
                           'frame': self.formatFrame(record.pop('frame'))})
            result.update(record)
            return result
        elif level in (Levels.DEBUG, Levels.WARNING):
            result.update({'msg': record.pop('msg')})
            if record.pop('frame',None):
                result.update({'frame': self.formatFrame(record.get('frame'))})
            result.update(record)
            return result
        elif level == Levels.CACHE:
            result.update(record)
            return result
        elif level == Levels.INFO:
            return {'msg':record}
