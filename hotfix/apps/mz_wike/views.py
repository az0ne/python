# -*- coding: utf-8 -*-

__author__ = 'changfu'

from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import Http404, JsonResponse
from django.conf import settings
from django.views.decorators.http import require_POST, require_safe

import datetime

import mz_user
import db.api.wike.wike
import mz_wike.functions
from utils.logger import logger as log
from mz_common.functions import safe_int
from mz_wike.forms import LikeWikeAskForm, MicroCourseAskForm

def wike_list(request):
    """

    :param request:
    :return:
    """
    wike_list = db.api.wike.wike.get_wike_list()
    if wike_list.is_error():
        log.error('db query error: wike_list: db.api.wike.wike.get_wike_list')
        raise Http404
    return render(request, 'mz_wike/wikelist.html', dict(wike_list=wike_list.result()))

def wike_detail(request, wike_id):
    """
    微课详情页
    """
    increase_step = 5  # 每次请求增长人数

    # 获取登陆信息
    login = request.GET.get('login', False)  # 当前用户是否登陆
    nick_name = request.GET.get('nick_name', '')  # 当前用户的昵称
    head_image = request.GET.get('head_image', '')  # 当前用户的头像
    openid = request.GET.get('openid', '')  # 当前用户openid

    # 获取weike信息
    wike = db.api.wike.wike.get_wike(wike_id)
    if wike.is_error():
        log.warn('db query error: wike_detail: db.api.wike.wike.get_wike')
        raise Http404
    if not wike.result():
        log.warn('no wike queryed: wike_detail: db.api.wike.wike.get_wike: more info wike_id: %s' % wike_id)
        raise Http404
    wike = wike.result()[0]
    if not wike.get('id'):
        # todo 搞清楚为何微课id对应的微课不存在的情况, 会返回一行全部为None的数据. 研究Mysql
        log.warn('no wike queryed: wike_detail: db.api.wike.wike.get_wike: more info wike_id: %s' % wike_id)
        raise Http404

    # 处理职业课程
    if wike['career_course_info']:
        wike['career_course_info'] = list(item.split('__') for item in wike['career_course_info'].split(','))

    # 计算伪造的学生人数
    student_count = wike.get('student_count') if wike.get('student_count') is not None else 1000
    min_student_count = wike.get('min_student_count') if wike.get('min_student_count') else 1000
    max_student_count = wike.get('max_student_count') if wike.get('max_student_count') else 1500
    wike['student_count'] = mz_wike.functions.increase_student_number_randomly(student_count,
                                                                               increase_step,
                                                                               min_student_count,
                                                                               max_student_count)
    # 更新伪造的学生人数
    result = db.api.wike.wike.update_wike_student_count(wike_id, wike['student_count'])
    if result.is_error():
        log.warn('update student_count fail: wike_detail: db.api.wike.wike.update_wike_student_count')

    # 获取微信网页鉴权页面
    callback_url = '%s%s' % (settings.SITE_URL, reverse("user:get_weixin_auth_token"))
    reference_url = '%s%s' % (settings.SITE_URL, request.path)
    callback_url = mz_user.functions.url_add_params(callback_url, referer=reference_url)
    auth_url = mz_user.mz_oauth.WeiXinAuth2.get_weixin_page_code(callback_url)

    # 获取jsdk授权需要的信息
    url = '%s%s' % (settings.SITE_URL, request.get_full_path())
    wx_config = mz_user.mz_oauth.WeiXinAuth2.generate_weixin_jaspi_signature(url)

    return render(request, 'mz_wike/wike_detail.html', dict(auth_url=auth_url,
                                                            wike=wike,
                                                            login=login,
                                                            nick_name=nick_name,
                                                            head_image=head_image,
                                                            openid=openid,
                                                            SITE_URL=settings.SITE_URL,
                                                            wx_config=wx_config))

@require_safe
def wike_ask_list(request):
    """
    @brief 获取微课问答列表
    :param request:
    :return:
    @note: 微课问答功能并未实现真正的用户登陆, 用openid作为用户登陆的凭据,是不严格的.
    """
    openid = request.GET.get('openid')
    wike_course_id = safe_int(request.GET.get('wike_course_id', 0), 0)
    if openid:  # 如过有openid, 证明用户已登陆
        asks = db.api.wike.wike.get_wike_ask_list(wike_course_id, openid)
    else:  # 如果没有openid, 证明用户未登录
        asks = db.api.wike.wike.get_wike_ask_list(wike_course_id)
    if asks.is_error():
        log.warn('wike_ask_list failed, more info: openid is %s ' % openid if openid else 'null')
        return JsonResponse(dict(status=False, data=''))
    return JsonResponse(dict(status=True, data=asks.result()))

@require_POST
def like_micro_course_ask(request):
    """
    @brief 微课问答点赞
    :return:
    @note 微课问答功能并未实现真正的用户登陆,因此,此处不能要求登陆状态

    @todo: 并未做真正的用户验证登陆,用户可以做恶意提交.目前,仅能验证openid的长度,必须严格等于微信用户openid的长度
    """
    post_data = request.POST.dict()
    form = LikeWikeAskForm(post_data)

    if form.is_valid():
        result = form.do_like()
    else:
        return JsonResponse(dict(status=False, data=dict(msg=form.errors)))

    if result.is_error():
        log.warn('like_micro_course_ask fail. More info: data: %s' % str(post_data))
        return JsonResponse(dict(status=False, data=dict(msg=u'保存失败')))

    like_num = form.get_like_num()

    return JsonResponse(dict(status=True, data=like_num.result()[0]))

@require_POST
def add_wike_ask(request):
    """
    @brief 添加用户的微课问答
    :param request:
    :return:
    @note 微课问答功能并未实现真正的用户登陆,因此,此处不能要求登陆状态

    @todo: 并未做真正的用户验证登陆,用户可以做恶意提交.目前,仅能验证openid的长度,必须严格等于微信用户openid的长度
    """
    post_data = request.POST.dict()
    post_data.update(dict(ask_time=datetime.datetime.now()))
    form = MicroCourseAskForm(post_data)

    if form.is_valid():
        result = form.save()
        if result.is_error():
            log.info('add_wike_ask fail. More info: %s' % str(post_data))
            return JsonResponse(dict(staus=False, data=dict(msg=u'保存失败')))
        return JsonResponse(dict(status=True, data=result.result()[0]))

    return JsonResponse(dict(status=False, data=dict(msg=form.errors)))
