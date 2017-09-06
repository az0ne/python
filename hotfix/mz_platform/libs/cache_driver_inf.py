#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
cache lib interface
"""


class CacheDriverInf(object):
    """
    @brief Cache Lib Interface

    接入的cache lib需要实现相应的接口
    """

    def __init__(self):
        super(CacheDriverInf, self).__init__()

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        """
        @brief  设置key相对的value

        key或者value值如果不是str类型，会调用str（）方法产生value

        @param  name    value对应的key值
        @param  value   缓存的value值
        @param  ex   设置key过期时间单位为秒
        @param  px   设置key过期时间单位为毫秒
        @param  nx   设置为True，设置key对应的value如果不存在
        @param  xx   设置为True，设置key对应的value如果存在
        """

        raise NotImplemented('DRIVEN CLASS MUST IMPLEMENT IT')

    def get(self, name):
        """
        @brief      返回name对应的value，如果不存在返回None

        @return     返回name对应的value，如果不存在返回None

        """

        raise NotImplemented('DRIVEN CLASS IMPLEMENT IT')


class DummyCacheClient(CacheDriverInf):
    """
    @brief CacheLib dummy 实现版本
    """

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        print '[DummyCacheClient]:', locals()

    def get(self, name):
        print '[DummyCacheClient]:', locals()


class RedisCacheClient(CacheDriverInf):
    """
    @brief CacheLib Redis 实现版本
    """

    def __init__(self, *args, **kwargs):
        import redis
        self.r = redis.Redis(*args, **kwargs)

    def set(self, name, value, ex=None, px=None, nx=False, xx=False):
        return self.r.set(name, value, ex, px, nx, xx)

    def get(self, name):
        return self.r.get(name)
