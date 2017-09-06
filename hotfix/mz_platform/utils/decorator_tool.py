#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import time
from functools import wraps
import cPickle as pickle

from mz_platform.services.core.log_service import log_it
from mz_platform.apis.api_result import ApiResult
from mz_platform.exceptions.mz_exception import MZException
from mz_platform.exceptions.mz_exception import MZSysException
from mz_platform.services.core.cache_service import CacheService


def sys_func_log(func):
    """
    @brief sys level log, log function call info
    @todo
        - record function arg
    """
    @wraps(func)
    def _deco(*args, **kwargs):
        log_it('enter:' + func.__name__)
        t = time.time()
        ret = func(*args, **kwargs)
        d = time.time() - t
        log_it('out:%s, during:%fs' % (func.__name__, d))
        return ret
    return _deco


def business_func_log(func):
    """
    @brief business level log, log business info
    @todo
        - record function arg
    """
    @wraps(func)
    def _deco(*args, **kwargs):
        log_it('enter:' + func.__name__)
        t = time.time()
        ret = func(*args, **kwargs)
        d = time.time() - t
        log_it('out:%s, during:%fs' % (func.__name__, d))
        return ret
    return _deco


def api_except_catcher(func):
    """
    @brief catch api function exception
    @todo
        - record function arg
    """
    @wraps(func)
    def _deco(*args, **kwargs):

        err_code = 0x0000
        err_desc = ""
        ret = None
        try:
            ret = func(*args, **kwargs)
        except MZException, e:
            err_code = e.err_code
            err_desc = e.err_desc
            ret = None
            e.print_exc()
        except Exception, e:
            e = MZSysException(e, "business exception catched")
            err_code = e.err_code
            err_desc = e.err_desc
            ret = None
            e.print_exc()
        except:
            t, n, tb = sys.exc_info()
            e = MZSysException(n, "unknown exception catched")
            err_code = e.err_code
            err_desc = e.err_desc
            ret = None
            e.print_exc()
        finally:
            return ApiResult(err_code, err_desc, ret)
    return _deco


class DataCache(object):
    """
    @brief      数据chache装饰器类

    """
    def __init__(self, ns):
        self.ns = ns

    def data_cacher_get(self, name, *args, **kwargs):
        """
        @brief      获取 name 对应的cache，如果不存在返回None
        """
        return None

    def data_cacher_set(self, name, value, *args, **kwargs):
        """
        @brief      设置 name 对应的cache
        """
        pass

    def is_concern(self, concern, *args, **kwargs):
        """
        @brief      是否是需要cache的关键词
        """
        return False

    def __call__(self, concern):
        """
        @brief      callable 对象， concern为caller设置的需要cache的关键词

        """

        def _wrap(func):
            @wraps(func)
            def _f(*args, **kwargs):
                fn = func.__name__
                fn = '%s:%s' % (self.ns, fn)
                concernd = self.is_concern(concern, *args, **kwargs)
                r = None
                if concernd:
                    r = self.data_cacher_get(fn, *args, **kwargs)
                if r:
                    return r
                r = func(*args, **kwargs)
                if concernd:
                    self.data_cacher_set(fn, r, *args, **kwargs)
                return r
            return _f
        return _wrap


class KWDataCache(DataCache):
    """
    @brief      key/value参数cache类
    """
    def data_cacher_get(self, name, *args, **kwargs):
        dch = CacheService.default_instance().data_cache_handler
        r = dch.get(name, sub_kw_name=kwargs, deserialize_func=pickle.loads)
        return r

    def data_cacher_set(self, name, value, *args, **kwargs):
        dch = CacheService.default_instance().data_cache_handler
        dch.set(name, value, sub_kw_name=kwargs, serialize_func=pickle.dumps)

    def is_concern(self, concern, *args, **kwargs):
        return len(kwargs) == 1 and kwargs.keys()[0] in concern

# #####################################
# example
# @cache_api_data_kw(('key1', 'key2'))
# #####################################
cache_api_data_kw = KWDataCache('api')
