# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from interface import wechat_outh_redirect


def wike_login_required(func):
    def wrapper(request, **kwargs):
        if 'union_id' not in request.session:
            return redirect(wechat_outh_redirect())
        return func(request, **kwargs)
    return wrapper
