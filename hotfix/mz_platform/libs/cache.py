#!/usr/bin/env python
# -*- coding: utf8 -*-

from mz_platform.libs.cache_driver_inf import *


class CacheClientFactory():

    registed = {
        "redis": RedisCacheClient,
        "dummy": DummyCacheClient
    }

    @staticmethod
    def create(cln, *args, **kwargs):
        """
        @brief      工厂方式创建cache客户端

        @param      cln     CacheLibName @see list_support
        @param      args     cache客户端所需参数
        @param      kwargs     cache客户端所需参数
        """
        return CacheClientFactory.registed.get(cln)(*args, **kwargs)

    @staticmethod
    def list_support():
        """
        @brief      列举所有支持的CacheLibName
        """
        return CacheClientFactory.registed.keys
