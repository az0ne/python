#!/usr/bin/env python
# -*- coding: utf8 -*-

from mz_platform.apis.base_api_result import BaseApiResult


class ApiResult(BaseApiResult):

    def __init__(self, err_code, err_desc, obj):
        """
        err_code : 错误码
        err_desc ：错误描述
        obj: object Inherited from MZObj depend on callee, otherwise return None
        """
        super(ApiResult, self).__init__(err_code, obj)
        self.err_desc = err_desc
