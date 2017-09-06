#!/usr/bin/env python
# -*- coding: utf8 -*-


class BaseApiResult(object):

    """
    @brief 这个是BaseApiResult

    详细藐视
    """

    def __init__(self, err_code, obj):
        """
        @brief __init__ brief

        detail desc

        @param err_code : 错误码
        @param obj : object Inherited from MZObj depend on callee, otherwise return None
        @note  this is note
        @throw : this is exception
        """
        self.err_code = err_code
        self.obj = obj

    def __nonzero__(self):
        if self.err_code:
            return False
        return True
