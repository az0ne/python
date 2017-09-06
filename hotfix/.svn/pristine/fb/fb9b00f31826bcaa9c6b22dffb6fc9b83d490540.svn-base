#!/usr/bin/env python
# -*- coding: utf8 -*-

from mz_platform.utils.view_tool import datetime_convert

class SqlResultWrapper(dict):
    """
    @brief wrapper dict object to object like instance

    you can use `ins.attr` no need ins['attr name']
    default search the `dict_obj`, you can create new getter function
    or other functions to implement requirement like alias, or combine
    默认所有的类型都是数据本身设计类型，如果需要类型转换，可以使用property方式改变默认实现
    没有的属性返回None
    """

    def __init__(self, dict_obj):
        (super, self).__init__()
        self.update(dict_obj)

    def __getattr__(self, name):

        if name.lower() == 'pk':
            name = 'id'

        if name in self:
            return self[name]
        return None

    def __getstate__(self):
        d = dict(self)
        d.update(self.__dict__)
        return d

    def __setstate__(self, state):
        self.update(state)

    def _html_publish_date_impl(self, date):
        return datetime_convert(date)
