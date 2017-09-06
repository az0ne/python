#!/usr/bin/env python
# -*- coding: utf8 -*-

import sys
import cStringIO.StringIO as StringIO
import traceback

from mz_platform.exceptions import mz_exception
from mz_platform.services import log_service


class MZServiceException(mz_exception.MZException):
    """
    **描述** :
            - 服务异常类，处理服务异常，会自动处理记录log的操作。
                此类主要处理业务异常
    """

    def print_exc(self):
        t, v, tb = sys.exc_info()
        fo = StringIO()
        traceback.print_tb(tb, file=fo)
        val = fo.getvalue()
        fo.close()
        log_service.log_it(
            "[ServiceException]err_code:%d, e:%s, desc:%s, tb:%s" % (self.err_code, self.ori_exception, self.err_desc, val))
