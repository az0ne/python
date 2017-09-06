#!/usr/bin/env python
# -*- coding: utf8 -*-

from mz_platform.services.core.log_service import LogService
from mz_platform.services.core.cache_service import CacheService

# ################################################
# log setting
# ################################################
# sys_logger = LogService.get_sys_logger()
# bu_logger = LogService.get_business_logger()

# ################################################
# cache setting
# ################################################
page_cacher = CacheService.default_instance().page_cache_handler


def ensure_apiresult_obj(func, *args, **kwargs):
    """
    @brief 返回API.obj保证函数返回的ApiReuslt状态为成功，并且保证返回对象可以通过if测试
    如果失败抛出异常

    @param func : 获得ApiResult对象的函数
    @param args : 不定参数输入
    @param kwargs : 不定参数输入
    @retval ApiResult对象包含的实际对象
    """
    obj = func(*args, **kwargs)
    obj = ensure_obj(obj)
    return ensure_obj(obj.obj)


def ensure_obj(obj):
    """
    @brief 检查对象是否为空

    使用if判断,如果失败抛出异常Exception

    @param obj : 被检查对象
    @retval : 返回传入的obj
    """
    if not obj:
        raise AssertionError('obj:{} if test failed'.format(obj))
    return obj


def opt_apiresult_obj(defval, func, *args, **kwargs):
    """
    @brief 返回API.obj结果如果函数返回的ApiReuslt状态为成功，并且返回对象可以通过if测试
    如果失败使用默认值

    @param defval : Api失败之后的返回值
    @param func : 获得ApiResult对象的函数
    @param args : 不定参数输入
    @param kwargs : 不定参数输入
    @retval ApiResult对象包含的实际对象

    @todo 接入log实现
    """
    result = defval
    try:
        result = ensure_apiresult_obj(func, *args, **kwargs)
    except AssertionError, e:
        LogService.log_it('[Exception in opt_apiresult_obj]: %s' % (e,))
    finally:
        return result
