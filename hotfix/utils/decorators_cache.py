# -*- coding: utf-8 -*-
from django.core.cache import caches


def cache_data(*args, **kwargs):
    cache_alias = kwargs.pop('cache', 'default')
    cache_instance = caches[cache_alias]
    cache_timeout = args[0] if args else cache_instance.default_timeout
    key = kwargs.pop('key', '')

    def _cache_data(func):
        def wrapper(*args, **kwargs):
            cache_key = key or func.__module__ + '.' + func.func_name
            cache_pk = kwargs.pop('cache_pk', None)
            if cache_pk is not None:
                cache_key = cache_key + '_%s' % cache_pk
            data = cache_instance.get(cache_key)
            if data:
                return data
            else:
                ret = func(*args, **kwargs)
                if ret:
                    cache_instance.set(cache_key, ret, cache_timeout)
                return ret

        return wrapper

    return _cache_data
