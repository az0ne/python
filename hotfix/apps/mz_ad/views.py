# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.core.cache import cache
from django.template import loader, RequestContext
from django.http import HttpResponse, JsonResponse, Http404

from apps.mz_lps4.class_dict import CAREER_ID_TO_SHORT_NAME
from db.api.course.career_course_intro import get_career_course_info, user_class_type


def pm(request):
    """产品经理落地页"""

    # 游客读取首页缓存
    # openid 第三方（QQ,微信）
    # verify_email 验证邮箱
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        html = cache.get('ad_pm_html')
        if html:
            return HttpResponse(html)

    t = loader.get_template('mz_ad/pm.html')
    html = t.render(RequestContext(request, {}))
    # 游客保存首页缓存
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        cache.set('ad_pm_html', html, 5 * 60)

    return HttpResponse(html)


def python(request):
    """python web开发落地页"""

    # 游客读取首页缓存
    # openid 第三方（QQ,微信）
    # verify_email 验证邮箱
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        html = cache.get('ad_python_html')
        if html:
            return HttpResponse(html)
    t = loader.get_template('mz_ad/python.html')
    html = t.render(RequestContext(request, {}))
    # 游客保存首页缓存
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        cache.set('ad_python_html', html, 5 * 60)

    return HttpResponse(html)


def ui(request):
    """ui设计落地页"""
    # 游客读取首页缓存
    # openid 第三方（QQ,微信）
    # verify_email 验证邮箱
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        html = cache.get('ad_ui_html')
        if html:
            return HttpResponse(html)

    t = loader.get_template('mz_ad/ui.html')
    html = t.render(RequestContext(request, {}))
    # 游客保存首页缓存
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        cache.set('ad_ui_html', html, 5 * 60)

    return HttpResponse(html)


def op(request):
    """运营落地页"""
    # 游客读取首页缓存
    # openid 第三方（QQ,微信）
    # verify_email 验证邮箱
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        html = cache.get('ad_op_html')
        if html:
            return HttpResponse(html)

    t = loader.get_template('mz_ad/op.html')
    html = t.render(RequestContext(request, {}))
    # 游客保存首页缓存
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        cache.set('ad_op_html', html, 5 * 60)

    return HttpResponse(html)


def web(request):
    """web前端落地页"""
    # 游客读取首页缓存
    # openid 第三方（QQ,微信）
    # verify_email 验证邮箱
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        html = cache.get('ad_web_html')
        if html:
            return HttpResponse(html)

    t = loader.get_template('mz_ad/web.html')
    html = t.render(RequestContext(request, {}))
    # 游客保存首页缓存
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        cache.set('ad_web_html', html, 5 * 60)

    return HttpResponse(html)


def ai(request):
    """ai落地页"""
    # 游客读取首页缓存
    # openid 第三方（QQ,微信）
    # verify_email 验证邮箱

    #数据库里存的是ml,URL用的是ai
    course_id = u'ml'
    result = get_career_course_info(course_id)
    if result.is_error():
        raise Exception('get_career_course_info')
    career_course = result.result()
    if not career_course:
        raise Http404
    career_id = career_course['id']
    short_name = CAREER_ID_TO_SHORT_NAME.get(career_id)

    data = {}

    # user报名情况判断
    user = request.user
    if user.is_authenticated():
        result = user_class_type(user_id=user.id, career_id=career_id)
        is_normal_class = result.result()['is_normal_class']
        if result.is_error():
            raise Exception('user_class_type')
            data.update(result.result())

    # 购买课程按钮跳转代码結束

    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        html = cache.get('ad_ai_html')
        if html:
            return HttpResponse(html)

    t = loader.get_template('mz_line/ai.html')
    # 推荐课程
    # hot_courses = db.api.common.homepage.get_hot_course_list(_enable_cache=True)
    # if hot_courses.is_error():
    #     hot_course_data_list = []
    # else:
    #     hot_course_data_list = hot_courses.result()
    # try:
    #     hot_course_datas = hot_course_data_list[1][1]
    # except Exception, e:
    #     log.warn('e:{0}'.format(str(e)))
    #     hot_course_datas = []
    # data.update(
    #     {
    #         'career_id': career_id,
    #         'short_name': short_name,
    #         'course_id': course_id,
    #         'hot_course_datas': hot_course_datas,
    #         'is_normal_class': is_normal_class
    #     }
    # )
    html = t.render(RequestContext(request, locals()))
    # 游客保存首页缓存
    if request.user.is_anonymous() and not request.GET.get('openid') and not request.GET.get('verify_email'):
        cache.set('ad_ai_html', html, 5 * 60)

    return HttpResponse(html)