# -*- coding: utf-8 -*-

import time
from datetime import datetime
from utils.logger import logger as log
from db.cores.cache import cache


class APIResult(object):
    def __init__(self, result={}, code=True):
        self._result = result
        self._code = code

    def is_error(self):
        return not self._code

    def result(self):
        return self._result


def dec_get_cache(key):
    def wrap(func):
        def _func(*args, **kwargs):
            # get cache
            val = cache.get(key)
            if val:
                return APIResult(result=val)
            else:
                return func(*args, **kwargs)

        return _func

    return wrap