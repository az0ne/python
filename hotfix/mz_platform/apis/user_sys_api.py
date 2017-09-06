#!/usr/bin/env python
# -*- coding: utf8 -*-
import base_sys_api
from mz_platform.utils.decorator_tool import api_except_catcher


"""
User Api Collection


-   所有的导出外部调用的api，必须用装饰器
    @api_except_catcher 装饰保证捕获所有异常和包装成ApiResult对象
-   直接数据对象
-   经过复杂查询得到的对象
"""


class UserSysApi(base_sys_api.BaseSysApi):
    """
    @brief 用户系统API接口类

    """
    _api = None

    @staticmethod
    def default_instance():
        """
        @brief 默认api对象
        """
        if not UserSysApi._api:
            UserSysApi._api = UserSysApi()
        return UserSysApi._api

    @api_except_catcher
    def get_one_user(self, **kwargs):
        """
        @brief 获取用户对象

        @param kwargs : 查询User对象的条件，多个条件是and的关系
        @retval : 符合条件的User对象，如果存在多个返回第一个，如果没有
        符合条件的对象，返回None
        """
        t = self.user_service.get_user(conditions=self.s_p(kwargs))
        if not t:
            return None
        return self.n_obj('User', t[0])

    @api_except_catcher
    def get_one_teacher(self, **kwargs):
        """
        @brief 获取教师对象

        @param kwargs : 查询Teacher对象的条件，多个条件是and的关系
        @retval : 符合条件的Teacher对象，如果存在多个返回第一个，如果没有
        符合条件的对象，返回None
        """
        t = self.user_service.get_user(conditions=self.s_p(kwargs))
        if not t:
            return None
        return self.n_obj('Teacher', t[0])

    @api_except_catcher
    def get_all_teacher(self, **kwargs):
        """
        @brief 获取所有教师对象

        @param kwargs : 查询Teacher对象的条件，多个条件是and的关系
        @retval : 符合条件的Teacher对象，如果没有符合条件的对象返回[]
        """
        ts = self.user_service.get_teacher(**kwargs)
        return self.n_obj('Teacher', ts)
