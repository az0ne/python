# -*- coding: utf-8 -*-

"""
@version: 2016/3/28
@author: Jackie
@contact: jackie@maiziedu.com
@file: cache/util.py
@time: 2016/3/28 16:58
@note:  ??
@use:
    Cache.read_from_cache(Cache.CACHE_TYPE_HTML,'www_page_index')
"""

from django.conf import settings
from django.core.cache import caches


class Cache:
    TIMEOUT_S10 = 10
    TIMEOUT_S30 = 30
    TIMEOUT_M1 = 60 * 1
    TIMEOUT_M10 = 0 * 10
    TIMEOUT_D1 = 60 * 60 * 24

    CACHE_TYPE_DEFAULT = 'default'
    CACHE_TYPE_HTML = 'html'
    CACHE_TYPE_DATA = 'data'
    CACHE_TYPE_ATOFUC = 'default'
    CACHE_TYPE_QUEUE = 'queue'

    @classmethod
    def get_connection(cls, cache_type):
        alias = cls.correct_alias(cache_type)
        return caches[alias].client.get_client()

    @classmethod
    def correct_alias(cls, cache_type):
        return cache_type if cache_type in getattr(settings, 'CACHES', {}) else 'default'

    @classmethod
    def get_django_cache_instance(cls, cache_type):
        alias = cls.correct_alias(cache_type)
        cache_instance = caches[alias]
        return cache_instance

    @classmethod
    def get(cls, key, cache_type=CACHE_TYPE_DEFAULT):
        return cls.get_django_cache_instance(cache_type).get(key)

    @classmethod
    def set(cls, key, value, cache_type=CACHE_TYPE_DEFAULT, timeout=None):
        return cls.get_django_cache_instance(cache_type).set(key, value, timeout=timeout)

    @classmethod
    def delete(cls, key, cache_type=CACHE_TYPE_DEFAULT):
        return cls.get_django_cache_instance(cache_type).delete(key)


class CachedFixedQueue:
    '''
    @note: 基于redis的list结构设计一个固定长度的队列
    左进右出！！！！！
    '''

    def __init__(self, key, max_len, time_out=0):
        self.key = "[FixedList]%s" % key
        self.max_len = max_len
        self.time_out = time_out
        self.conn = Cache.get_connection(Cache.CACHE_TYPE_QUEUE)

    def push(self, item):
        if self.conn.llen(self.key) < self.max_len:
            self.conn.lpush(self.key, item)
        else:
            def _push(pipe):
                pipe.multi()
                pipe.rpop(self.key)
                pipe.lpush(self.key, item)

            self.conn.transaction(_push, self.key)
        if self.time_out:
            self.conn.expire(self.key, self.time_out)

    def pop(self):
        return self.conn.rpop(self.key)

    def get(self):
        return self.conn.lrange(self.key, 0, -1)

    def delete(self):
        self.conn.delete(self.key)

    def exists(self):
        return self.conn.exists(self.key)

    def __getslice__(self, start=0, end=-1):
        return self.conn.lrange(self.key, start, end)
