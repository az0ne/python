# -*- coding: utf-8 -*-

"""
@version: 2016/3/28
@author: Jackie
@contact: jackie@maiziedu.com
@file: decorators.py
@time: 2016/3/28 11:33
@note:  及时性异步任务统一装饰器
"""


def async(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        return ret

    return wrapper
