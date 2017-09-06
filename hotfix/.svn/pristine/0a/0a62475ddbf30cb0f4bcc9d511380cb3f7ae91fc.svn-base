#!/usr/bin/env python
# -*- coding: utf8 -*-


class ApiException(Exception):
    """
    @brief 处理ApiResult出错不能继续下去抛出异常，方便view层集中处理

    """

    def __init__(self, api_result):
        """
        @param api_result : ApiResult对象
        """
        name = api_result.__class__.__name__
        err_code = api_result.err_code
        err_desc = api_result.err_desc
        s = "Api Error On:%s(%d,%s)" % (name, err_code, err_desc)
        super(ApiException, self).__init__(s)
