# -*- coding: utf-8 -*-

"""
@version: 2016/3/28
@author: Jackie
@contact: jackie@maiziedu.com
@file: decorators.py
@time: 2016/3/28 11:35
@note: 缓存装饰器, 装饰器可接收参数:
        timeout: 第一个参数为缓存时延,可以不指定,默认settings.CACHES中的默认时延
        cache: 缓存的库名 alias
        key:指定的缓存键值

        方法体中可以另指定参数,如:
        @cache_data
        def get_userinfo(user_id):
            retur xx
        这里想要获取指定用户信息, get_userinfo(user_id,cache_pk=user_id),调用时需要指定缓存的主键
"""
from django.core.cache import caches


def cache_data(*args, **kwargs):
    cache_alias = kwargs.pop('cache', 'default')
    cache_instance = caches[cache_alias]
    cache_timeout = args[0] if args else cache_instance.default_timeout
    key = kwargs.pop('key', '')

    def _cache_data(func):
        def wrapper(*args, **kwargs):
            """对于一些数据"""
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
