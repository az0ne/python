#!/usr/bin/env python
# coding=utf-8

__author__ = 'revol'


class BaseHandler(object):
    def __init__(self):
        pass

    def emit(self, record, level):
        pass

    def formatException(self, e):
        data = {'type': str(e.__class__)[7:-2],
                'message': str(e)}
        return data

    def formatFrame(self, frame):
        result = dict(filename=frame.f_code.co_filename,
                      method=frame.f_code.co_name,
                      line_num=frame.f_lineno)
        return result
