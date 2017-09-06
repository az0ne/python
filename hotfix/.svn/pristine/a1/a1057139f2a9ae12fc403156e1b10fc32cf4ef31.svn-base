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
    def __init__(self, prefix, host, port, pool_size, password=None):
        self.prefix = prefix
        redis_pool = redis.ConnectionPool(
            host=host, port=port, max_connections=pool_size, password=password)
        self.rds = redis.Redis(connection_pool=redis_pool)

    def _get_key(self, key):
        return "%s_%s" % (self.prefix, key)

    def get(self, key):
        try:
            res = self.rds.get(self._get_key(key))
            if not res:
                return None
            else:
                val = json.loads(res)
        except Exception as e:
            log.warn("redis get failed: exception: %s" % e)
            return None

        return val

    def set(self, key, val, expire=30):
        try:
            self.rds.set(self._get_key(key), json.dumps(val, cls=JsonCommonEncoder), expire)
        except Exception as e:
            log.warn("redis set failed: exception: %s" % e)
            return False

        return True


# 提前声明,否则引用时比较痛苦
cache = None


def make_cache():
    global cache

    if settings.ENABLE_DATA_CACHE == True:
        cache = RedisHandler(
            prefix=settings.CACHE_PREFIX,
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            pool_size=settings.REDIS_POOL_SIZE,
            password=settings.REDIS_PASSWORD)
    else:
        cache = DummyHandler()


# try:        
#     from uwsgidecorators import postfork
# except ImportError:
#     pass
# else:
#     make_redis_handler = postfork(make_redis_handler)

make_cache()

# cache = Cache(settings.CACHE_PREFIX)
# cache.set_handler(redis_cache)
