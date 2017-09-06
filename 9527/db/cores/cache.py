# -*- coding: utf-8 -*-

import json
import redis
from django.conf import settings
from utils.tool import JsonCommonEncoder
from utils.logger import logger as log

class DummyHandler(object):
    def __init__(self):
        pass
        
    def get(self, key):
        return None
        
    def set(self, key, val, expire=None):
        return True

        
class RedisHandler(object):
    def __init__(self, host, port, pool_size, password=None):
        redis_pool = redis.ConnectionPool(
            host=host,
            port=port,
            max_connections=pool_size,
            password=password)
        self.rds = redis.Redis(connection_pool=redis_pool)

    def get(self, key):
        try:
            val = json.loads(self.rds.get(key))
        except Exception as e:
            log.warn("redis get error: exception: %s" % e)            
            return None
            
        return val

    def set(self, key, val, expire=None):
        try:
            self.rds.set(key, json.dumps(val, cls=JsonCommonEncoder), expire)
        except Exception as e:
            log.warn("redis set error: exception: %s" % e)
            return False

        return True

    def keys(self):
        return self.rds.keys()

    def delete(self, key):
        return self.rds.delete(key)
        
class Cache(object):
    def __init__(self, prefix):
        self.prefix = prefix

    def set_handler(self, handler):
        self.handler = handler

    def get_key(self, key):
        return "%s_%s" % (self.prefix, key)
        
    def get(self, key):
        return self.handler.get(self.get_key(key))

    def set(self, key, val, expire=None):
        return self.handler.set(self.get_key(key), val, expire)

    def keys(self):
        return self.handler.keys()

    def delete(self, key):
        return self.handler.delete(key)
        
redis_cache = RedisHandler(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        pool_size=settings.REDIS_POOL_SIZE,
        password=settings.REDIS_PASSWORD)

dummy_cache = DummyHandler()

cache = Cache(settings.CACHE_PREFIX)
cache.set_handler(redis_cache)
