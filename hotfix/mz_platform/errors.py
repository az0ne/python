#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
errCode定义
0x0000: 正常无错误

0x1000: 系统错误
0x2000: 课程库系统错误
"""


def defineError(errCode, desc):
    return (errCode, dict(desc=desc))

ERROR = dict(
    (defineError(0x0000, "success"),
     defineError(0x1000, "SystemError"),
     defineError(0x2000, "CourseSystemError"),))
