# -*- coding: utf-8 -*-
from core.common.http.response import failed_json


def app_user_required(func):
    def wrapper(request, **kwargs):
        if request.user.is_authenticated():
            return func(request, **kwargs)
        return failed_json(u'unauthorized')

    return wrapper


def app_teacher_required(func):
    def wrapper(request, **kwargs):
        if request.user.is_authenticated() and request.user.is_teacher():
            return func(request, **kwargs)
        return failed_json(u'unauthorized')

    return wrapper

