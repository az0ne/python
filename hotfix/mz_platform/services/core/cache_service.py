#!/usr/bin/env python
# -*- coding: utf8 -*-

from mz_platform.objects.mz_object import MZObject
from mz_platform.libs import cache


class CacheService(MZObject):
    """
    @brief      cahce service
    """

    _default_instance = None
    _config = {
        # 'page': dict(cln='redis', args=[], kwargs={}),
        # 'data': dict(cln='redis', args=[], kwargs={})
        'page': dict(cln='dummy', args=[], kwargs={}),
        'data': dict(cln='dummy', args=[], kwargs={})
    }

    @staticmethod
    def default_instance():
        """
        @brief 默认 cache service 对象

        @return     返回单例CacheService对象
        """

        if not CacheService._default_instance:
            CacheService._default_instance = CacheService()
        return CacheService._default_instance

    def __init__(self):
        self._page_cacher = None
        self._data_cacher = None

    @property
    def page_cache_handler(self):
        """
        @brief      获取*html*缓存处理器

        @return     返回CacheHandler对象
        """

        if self._page_cacher is None:
            self._page_cacher = CacheHandler(
                self.get_cache_client('page'),
                'page')
        return self._page_cacher

    @property
    def data_cache_handler(self):
        """
        @brief      data 缓存处理器

        @return     返回CacheHandler对象
        """

        if self._data_cacher is None:
            self._data_cacher = CacheHandler(
                self.get_cache_client('data'),
                'data')
        return self._data_cacher

    def get_cache_client(self, name):
        """
        @brief      获取cache lib客户端对象

        根据 `_config` 中的配置生成

        @return     返回配置指定的cachelib对象
        """
        config = self._config[name]
        cln = config['cln']
        args = config['args']
        kwargs = config['kwargs']
        return cache.CacheClientFactory.create(cln, *args, **kwargs)


class CacheHandler(object):
    """
    @brief      cache消息处理器
    """

    def __init__(self, client, namespace, prefix='', postfix=''):
        """
        @param  client  object implement CacheDriverInf
        @param  namespace   cache域
        @param  prefix   key 的前缀
        @param  postfix   key 的后缀
        """
        super(CacheHandler, self).__init__()
        self.prefix = prefix
        self.postfix = postfix
        self.namespace = namespace
        self.client = client

    def set(self, name, value, ex=None, objective_func=str):
        """
        @brief      设置以name为key的缓存值

        以格式化的key存储value
        格式化处理key 详细查看 @see format_key
        如果value非str类型，会使用str方法获得value

        @param  name   缓存key
        @param  value   缓存值
        @param  ex   设置key过期时间单位为秒，默认为None,不限制时间
        @param  objective_func  value序列化函数,默认使用str, func(obj)返回str对象
        """

        key = self.format_key(name)
        value = objective_func(value)
        self.client.set(key, value, ex=ex)

    def get(self, name, defval=None, objective=False):
        """
        @brief      获取以name为key的缓存值

        以格式化的key获取value
        格式化处理key 详细查看 @see format_key
        objective为True，使用eval转化str为python对象，转化失败会抛出异常
        目前仅支持python内建对象,

        @param  name   缓存key
        @param  defval   获取失败时的默认值
        @param  objective   默认False返回str类型，True使用eval转化为python对象
        @return     返回key对应value，如果失败返回默认值，如果设置objective，转化为python对象。
        """

        key = self.format_key(name)
        val = self.client.get(key)
        if val is None:
            return defval
        if objective:
            val = eval(val)
        return val

    def format_key(self, key):
        return "{ns}:{pre}{key}{post}".format(ns=self.namespace,
                                              pre=self.prefix,
                                              key=key,
                                              post=self.postfix)
