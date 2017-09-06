# -*- coding: utf-8 -*-
import json
import time
import requests

from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, Http404
from django.conf import settings
from django.shortcuts import render, redirect
from decorators import wike_login_required
from mz_wike.interface import get_course_lesson_data, wechat_send_message_pay_success, STATE, wx_config, \
    jsapi_pay, trans_xml_to_dict, verify_sign, get_comment_count, update_comment_count
from core.common.http.response import success_json, failed_json
from utils.logger import logger as log
from utils.tool import generation_order_no

import db.api.wike.user
import db.api.wike.course
import db.api.wike.lesson
import db.api.wike.discuss
import db.api.wike.banner
import db.api.wike.order


# 授权回调处理
def wechat_callback(request):
    if request.GET.get('state') == STATE:
        code = request.GET.get('code')
        if code:
            url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&' \
                  'code={code}&grant_type=authorization_code'.format(appid=settings.APPID, secret=settings.SECRET,
                                                                     code=code)
            r = requests.get(url)
            data = json.loads(r.content)
            if data.get('errcode'):
                log.info('wechat_outh_code_%s_%s' % (data.get('errcode'), data.get('errmsg')))
                return HttpResponse(u'授权失败,请重新授权')
            token = data['access_token']
            openid = data.get('openid')
            url = 'https://api.weixin.qq.com/sns/userinfo?access_token={token}&openid={openid}&lang=zh_CN'.format(
                token=token, openid=openid)
            r = requests.get(url)
            data = json.loads(r.content)
            if data.get('errcode'):
                log.info('wechat_outh_code_%s_%s' % (data.get('errcode'), data.get('errmsg')))
                return HttpResponse(u'授权失败,请重新授权')
            unionid = data.get('unionid')
            nick_name = data.get('nickname')
            avatar = data.get('headimgurl') if data.get('headimgurl') else ''

            # insert mysql
            result = db.api.wike.user.save_user(open_id=openid, union_id=unionid,
                                                nick_name=nick_name, avatar=avatar)
            if result.is_error():
                return HttpResponse(u'授权失败,请重新授权')

            request.session['union_id'] = unionid

            return redirect(reverse('wike:wechat_course_list'))
    return HttpResponse(u'授权失败,请重新授权')


@wike_login_required
def wechat_course_list(request):
    # banner
    result = db.api.wike.banner.get_banners()
    if result.is_error():
        banners = []
    else:
        banners = result.result()
    # 课程分类
    result = db.api.wike.course.get_careers()
    if result.is_error():
        return render(request, 'mz_wike/fail_page.html', {'message': u'服务器开小差了,稍后再试吧'})
    careers = result.result()
    # 所有课程
    result = db.api.wike.course.get_courses()
    if result.is_error():
        return render(request, 'mz_wike/fail_page.html', {'message': u'服务器开小差了,稍后再试吧'})
    courses = result.result()
    course_data = {}
    for course in courses:
        if not course_data.get(course['career_course_id']):
            course_data[course['career_course_id']] = []
        course_data[course['career_course_id']].append(dict(
            image=course['image_url'],
            teacher_name=course['real_name'] if course['real_name'] else course['nick_name'],
            course_name=course['name'],
            course_id=course['id']
        ))
    for career in careers:
        career['courses'] = course_data.get(career['id'], [])
    banners = [dict(
        href=banner['url'],
        src=settings.MEDIA_URL + banner['image_url'],
        alt=banner['title']
    ) for banner in banners]
    return render(request, 'mz_wike/wechat_list.html', {'careers': careers, 'banners': json.dumps(banners)})


@wike_login_required
def wechat_course(request, course_id):
    lesson = db.api.wike.lesson.get_first_lesson_by_course_id(course_id)
    if lesson.is_error():
        log.warn('get_first_lesson_by_course_id failed. '
                 'course_id: {0}'.format(course_id))
        raise Http404
    else:
        lesson = lesson.result()

    return redirect(reverse('wike:wechat_lesson',
                            args=(course_id, lesson.get('id', 0))))


@wike_login_required
def wechat_lesson(request, course_id, lesson_id):
    data = get_course_lesson_data(course_id, lesson_id)

    # 是否购买
    union_id = request.session.get('union_id')
    is_pay = db.api.wike.course.is_pay(union_id, course_id)
    if is_pay.is_error():
        log.warn('is_pay failed. union_id: {0}, '
                 'course_id: {1}'.format(union_id, course_id))
        is_pay = False
    else:
        is_pay = is_pay.result()

    comment_count = get_comment_count(course_id, union_id)

    data.update(is_pay=is_pay, comment_count=comment_count)

    url = '%s%s' % (settings.SITE_URL, request.get_full_path())
    data['wechat_config'] = wx_config(url)
    data['share_img'] = settings.SITE_URL + '/static/images/wapwike/weixin_share_logo.jpg'
    data['share_url'] = url
    data['timestamp'] = int(time.time())
    return render(request, 'mz_wike/course_detail_pay.html', data)


@wike_login_required
def my_course(request):
    union_id = request.session.get('union_id')
    result = db.api.wike.course.get_my_course(union_id)
    if result.is_error():
        return render(request, 'mz_wike/fail_page.html', {'message': u'服务器开小差了,稍后再试吧'})
    courses = result.result()
    return render(request, 'mz_wike/my_course.html', dict(courses=courses))


@wike_login_required
def post_discuss(request):
    union_id = request.session.get('union_id')
    course_id = request.POST.get('course_id')
    parent_id = request.POST.get('parent_id')
    content = request.POST.get('content')

    user = db.api.wike.user.get_user_by_union_id(union_id)
    if user.is_error():
        log.warn('get_user_by_union_id failed. '
                 'union_id: {0}'.format(union_id))
        return failed_json(u'无此用户！')
    else:
        user = user.result()

    post_data = dict(
        course_id=course_id, union_id=union_id,
        nick_name=user.get('nick_name'),
        avatar_url=user.get('avatar'),
        content=content, parent_id=parent_id
    )

    res = db.api.wike.discuss.add_discuss(**post_data)
    if res.is_error():
        log.warn('add_discuss failed. '
                 'post_data: {0}'.format(post_data))
        return failed_json(u'提交失败！')

    # 更新回答次数
    if parent_id != '0':
        update_comment_count(course_id, parent_id)

    del post_data['union_id']
    post_data['id'] = res.result()
    return success_json(post_data)


@wike_login_required
def wechat_course_pay(request):
    course_id = request.GET.get('course_id')
    result = db.api.wike.course.get_course_by_id(course_id=course_id)
    if result.is_error():
        return render(request, 'mz_wike/fail_page.html', {'message': u'服务器开小差了,稍后再试吧'})
    course = result.result()
    if not course:
        raise Http404
    # 是否已经支付
    result = db.api.wike.course.is_pay(union_id=request.session['union_id'], course_id=course_id)
    if result.is_error():
        return render(request, 'mz_wike/fail_page.html', {'message': u'服务器开小差了,稍后再试吧'})
    if result.result():
        return redirect(reverse('wike:wechat_course', kwargs={'course_id': course_id}))
    url = '%s%s' % (settings.SITE_URL, request.get_full_path())
    wechat_config = wx_config(url)
    timestamp = int(time.time())
    return render(request, 'mz_wike/pay.html', {'course': course, 'wechat_config': wechat_config,
                                                'timestamp': timestamp})


@wike_login_required
def wechat_submit_order(request):
    course_id = request.POST.get('course_id')
    union_id = request.session['union_id']
    result = db.api.wike.course.get_course_by_id(course_id=course_id)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    course = result.result()
    if not course:
        return failed_json(u'找不到相关职业课程')
    order_no = generation_order_no()
    pay_price = course['price']
    result = db.api.wike.order.add_order(course_id, union_id, pay_price, order_no, 0)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    result = db.api.wike.user.get_user_by_union_id(union_id=union_id)
    if result.is_error():
        return failed_json(u'服务器开小差了,稍后再试吧')
    open_id = result.result()['open_id']
    prepay = jsapi_pay(request, order_no, course['name'], course['price'], open_id, course_id, course['name'])
    if prepay:
        return success_json(prepay)
    return failed_json(u'服务器错误')


def wechat_pay_notify(request):
    try:
        if request.method == 'POST':
            data = trans_xml_to_dict(request.body)
            verify = verify_sign(data)
            if verify:
                if data['result_code'] == 'SUCCESS':
                    log.info('wike_pay_notify_info: %s' % json.dumps(data))
                    total_fee = float(data['total_fee']) / 100
                    result = db.api.wike.order.update_order(data['out_trade_no'], total_fee,
                                                            data['transaction_id'], 1)
                    if result.is_error():
                        log.error('wike_pay_insert_error: %s' % json.dumps(data))
                    else:
                        result = result.result()
                        if result:
                            # 推送信息到用户订阅号
                            wechat_send_message_pay_success(data['openid'], data['attach'], total_fee)
                        return_xml = """
                                        <xml>
                                            <return_code><![CDATA[SUCCESS]]></return_code>
                                            <return_msg><![CDATA[OK]]></return_msg>
                                        </xml>
                                     """
                        return HttpResponse(return_xml, content_type="application/xml")
    except Exception as e:
        log.error(e)
    return_xml = """
                    <xml>
                        <return_code><![CDATA[FAIL]]></return_code>
                        <return_msg><![CDATA[FAIL]]></return_msg>
                    </xml>
                 """
    return HttpResponse(return_xml, content_type="application/xml")
