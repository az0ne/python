# -*- coding: utf-8 -*-

"""
@version: 2016/3/29
@author: Jackie
@contact: jackie@maiziedu.com
@file: response.py
@time: 2016/3/29 15:57
@note:  ??
"""
from django.http.response import JsonResponse


def success_json(data={}, next_url='', code=200, **kwargs):
    assert isinstance(data, dict)
    result = dict(
        success=True,
        message='',
        data=data,
        next=next_url,
        code=code
    )
    return JsonResponse(result, **kwargs)


def failed_json(message=u'', data={}, code=404, **kwargs):
    assert isinstance(message, unicode)
    result = dict(
        success=False,
        message=message,
        data=data,
        code=code
    )
    return JsonResponse(result, **kwargs)
