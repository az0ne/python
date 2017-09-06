# -*- coding:utf-8 -*-

import re
from functools import wraps

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render


def dec_login_required(func):
    def _func(request, *args, **kwargs):
        session_name = request.session.get('username')
        role_menus = request.session.get('role_menus')
        url = re.search(r'(\w+)/(\w+)/', request.path).group()
        got_url = False
        if role_menus:
            for menu in role_menus:
                if url in menu['url']:
                    got_url = True
        if session_name is None or not got_url:
            if request.method == 'GET':
                return render(request, 'loginindex.html')
            return HttpResponseRedirect(reverse('admin_login'))
        else:
            return func(request, *args, **kwargs)

    return _func


def ajax_login_required(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        session_name = request.session.get('username')
        role_menus = request.session.get('role_menus')
        url = re.search(r'(\w+)/(\w+)/', request.path).group()
        got_url = False
        if role_menus:
            for menu in role_menus:
                if url in menu['url']:
                    got_url = True
        if session_name is None or not got_url:
            return JsonResponse({'success': False,
                                 'msg': u'登录状态已过期，请重新登录。',
                                 'code': 403})
        else:
            return func(request, *args, **kwargs)

    return _func


def ajax_login_required_post(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        session_name = request.session.get('username')
        role_menus = request.session.get('role_menus')
        url = re.search(r'(\w+)/(\w+)/', request.path).group()
        got_url = False
        if role_menus:
            for menu in role_menus:
                if url in menu['url']:
                    got_url = True
        if session_name is None or not got_url:
            if request.method == 'POST':
                return JsonResponse({'success': False,
                                     'msg': u'登录状态已过期，请重新登录。',
                                     'code': 403})
            return render(request, 'loginindex.html')
        else:
            return func(request, *args, **kwargs)

    return _func


def ajax_login_required_get(func):
    @wraps(func)
    def _func(request, *args, **kwargs):
        session_name = request.session.get('username')
        role_menus = request.session.get('role_menus')
        url = re.search(r'(\w+)/(\w+)/', request.path).group()
        got_url = False
        if role_menus:
            for menu in role_menus:
                if url in menu['url']:
                    got_url = True
        if session_name is None or not got_url:
            if request.method == 'GET':
                return JsonResponse({'success': False,
                                     'msg': u'登录状态已过期，请重新登录。',
                                     'code': 403})
            return HttpResponseRedirect(reverse('admin_login'))
        else:
            return func(request, *args, **kwargs)

    return _func


# 验证是否有用户登录

def dec_login_validate(func):
    def _func(request, *args, **kwargs):
        session_name = request.session.get('username')
        if not session_name:
            if request.method == 'GET':
                return render(request, 'loginindex.html')
            return HttpResponseRedirect(reverse('admin_login'))
        else:
            return func(request, *args, **kwargs)

    return _func