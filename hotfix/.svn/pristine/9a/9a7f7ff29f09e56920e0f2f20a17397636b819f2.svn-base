#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import traceback
from cStringIO import StringIO

from mz_platform.services.core import log_service

"""
errCode定义
0x0000: 正常无错误
0x1000: 系统错误
0x2000: 课程库系统错误
"""


def define_error(errCode, desc):
    return (errCode, dict(desc=desc))

ERROR = dict(
    (define_error(0x0000, "success"),
        define_error(0x1001, "SystemError: IO Error"),
        define_error(0x2001, "CourseSystemError: IO Error"),))


def get_error_desc_with_code(errCode):
    if errCode not in ERROR:
        return 'Not Define Error Description With Code : %d' % (errCode)
    return ERROR[errCode]['desc']


class MZException (Exception):
    """
    @brief : 查询MZ基础异常类，
             包含原始异常对象和描述，产生系统异常log

    """

    def __init__(self, e, err_code, err_desc):
        """
        **参数** :
            - **e** : 原始异常对象
            - **desc** : 异常业务描述
        """
        self.ori_exception = e
        self.err_desc = err_desc
        self.err_code = err_code

    def get_error_code_string(self):
        return get_error_desc_with_code(self.err_code)

    def print_exc(self):
        t, v, tb = sys.exc_info()
        fo = StringIO()
        traceback.print_tb(tb, file=fo)
        val = fo.getvalue()
        fo.close()
        log_service.log_it(val)

    # def get_trace


class MZSysException(MZException):
    """docstring for MZSysException"""

    def __init__(self, e, err_desc):
        super(MZSysException, self).__init__(e, 0x1000, err_desc)

    def print_exc(self):
        t, v, tb = sys.exc_info()
        fo = StringIO()
        traceback.print_tb(tb, file=fo)
        val = fo.getvalue()
        fo.close()
        log_service.log_it("[SysException]err_code:%d, e:%s, desc:%s, tb:%s" % (self.err_code, self.ori_exception, self.err_desc, val))


class MZBusinessException(MZException):
    """docstring for MZSysException"""

    def __init__(self, e, err_desc):
        super(MZSysException, self).__init__(e, 0x2000, err_desc)
