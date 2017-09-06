# -*- coding: utf8 -*-
from django.http.response import JsonResponse


def success_json(data=None, next_url='', code=200, **kwargs):

    result = dict(
        success=True,
        msg='',
        data=data if data else {},
        next=next_url,
        code=code
    )
    return JsonResponse(result, **kwargs)


def failed_json(message=u'', data=None, code=404, **kwargs):

    result = dict(
        success=False,
        msg=message,
        data=data if data else {},
        code=code
    )
    return JsonResponse(result, **kwargs)
