# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.core.cache import cache
from django.template import loader, RequestContext
from django.http import HttpResponse, JsonResponse


def pm(request):
    """产品经理落地页"""

    # 游客读取首页缓存
    # openid 第三方（QQ,微信）
    # verify_email 验证邮箱
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        html = cache.get('wap_ad_pm_html')
        if html:
            return HttpResponse(html)

    t = loader.get_template('mz_wap/mz_ad/pm.html')
    html = t.render(RequestContext(request, {}))
    # 游客保存首页缓存
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        cache.set('wap_ad_pm_html', html, 5 * 60)

    return HttpResponse(html)


def python(request):
    """python web开发落地页"""

    # 游客读取首页缓存
    # openid 第三方（QQ,微信）
    # verify_email 验证邮箱
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        html = cache.get('wap_ad_python_html')
        if html:
            return HttpResponse(html)
    t = loader.get_template('mz_wap/mz_ad/python.html')
    html = t.render(RequestContext(request, {}))
    # 游客保存首页缓存
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        cache.set('wap_ad_python_html', html, 5 * 60)

    return HttpResponse(html)


def ui(request):
    """ui设计落地页"""
    # 游客读取首页缓存
    # openid 第三方（QQ,微信）
    # verify_email 验证邮箱
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        html = cache.get('wap_ad_ui_html')
        if html:
            return HttpResponse(html)

    t = loader.get_template('mz_wap/mz_ad/ui.html')
    html = t.render(RequestContext(request, {}))
    # 游客保存首页缓存
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        cache.set('wap_ad_ui_html', html, 5 * 60)

    return HttpResponse(html)


def op(request):
    """运营落地页"""
    # 游客读取首页缓存
    # openid 第三方（QQ,微信）
    # verify_email 验证邮箱
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        html = cache.get('wap_ad_op_html')
        if html:
            return HttpResponse(html)

    t = loader.get_template('mz_wap/mz_ad/op.html')
    html = t.render(RequestContext(request, {}))
    # 游客保存首页缓存
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        cache.set('wap_ad_op_html', html, 5 * 60)

    return HttpResponse(html)


def web(request):
    """web前端落地页"""
    # 游客读取首页缓存
    # openid 第三方（QQ,微信）
    # verify_email 验证邮箱
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        html = cache.get('wap_ad_web_html')
        if html:
            return HttpResponse(html)

    t = loader.get_template('mz_wap/mz_ad/web.html')
    html = t.render(RequestContext(request, {}))
    # 游客保存首页缓存
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        cache.set('wap_ad_web_html', html, 5 * 60)

    return HttpResponse(html)
