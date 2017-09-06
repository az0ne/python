# -*- coding: utf-8 -*-

"""
@version: 2016/4/7
@author: Jackie
@contact: jackie@maiziedu.com
@file: decorators.py
@time: 2016/4/7 19:02
@note:  ??
"""

import time


def timecost(func):
    def wrapper(*args, **kwargs):
        begin = time.time()
        ret = func(*args, **kwargs)
        print time.time() - begin
        return ret

    return wrapper
