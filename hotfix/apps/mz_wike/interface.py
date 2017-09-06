# -*- coding: utf-8 -*-
import time
import random
import string
import hashlib
import requests
import json
from xml.etree import ElementTree

from db.api.wike.lesson import update_reply_count, get_reply_count
from db.cores.cache import cache
import db.api.wike.discuss
import db.api.wike.course
import db.api.wike.lesson

from urllib import quote
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http.response import Http404

from utils.logger import logger as log

STATE = 'maiziEDU'


# 授权页面链接
def wechat_outh_redirect():
    app_id = settings.APPID
    redirect_uri = settings.SITE_URL + reverse('wike:wechat_callback')
    redirect_uri = quote(redirect_uri, safe='')
    # redirect_uri = quote('http://www.maiziedu.com/wike/wechat_test/', safe='')
    url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={appid}' \
          '&redirect_uri={redirect_uri}&response_type=code&scope=snsapi_userinfo' \
          '&state={state}#wechat_redirect'.format(appid=app_id, redirect_uri=redirect_uri, state=STATE)
    return url


def get_discuss_data(course_id):
    dis = db.api.wike.discuss.get_discuss_by_course_id(course_id)
    if dis.is_error():
        log.warn('get_discuss_by_lesson_id failed. '
                 'lesson_id: {0}'.format(course_id))
        dis = []
    else:
        dis = dis.result()

    for d in dis:
        child = db.api.wike.discuss.get_child_discuss(d['id'])
        if child.is_error():
            log.warn('get_child_discuss failed. '
                     'parent_id: {0}'.format(d['id']))
            child = []
        else:
            child = child.result()

        d['child_discuss'] = child

    return dis


def get_course_lesson_data(course_id, lesson_id):
    # 更新播放次数
    db.api.wike.course.update_course_play_count(course_id)
    db.api.wike.lesson.update_lesson_play_count(lesson_id)

    # 课程
    course = db.api.wike.course.get_course_by_id(course_id)
    if course.is_error():
        log.warn('get_course_by_id failed. '
                 'course_id: {0}'.format(course_id))
        raise Http404
    else:
        course = course.result()

    price = course['price']
    price_int, price_dec = str(price).split('.') if price else ('00', '00')
    course['price_int'], course['price_dec'] = price_int, price_dec

    # 当前章节
    lesson = db.api.wike.lesson.get_lesson_by_id(course_id, lesson_id)
    if lesson.is_error():
        log.warn('get_lesson_by_id failed. '
                 'lesson_id: {0}'.format(lesson_id))
        raise Http404
    else:
        lesson = lesson.result()

    # 章节列表
    lesson_list = db.api.wike.lesson.get_lessons_by_course_id(course_id)
    if lesson_list.is_error():
        log.warn('get_lessons_by_course_id failed. '
                 'course_id: {0}'.format(course_id))
        lesson_list = []
    else:
        lesson_list = lesson_list.result()

    # 常见提问
    faq = db.api.wike.discuss.get_faq_by_course_id(course_id)
    if faq.is_error():
        log.warn('get_faq_by_course_id failed. '
                 'course_id: {0}'.format(course_id))
        faq = []
    else:
        faq = faq.result()

    # 问答
    discuss_list = get_discuss_data(course_id)

    return dict(
        course=course, lesson=lesson,
        lesson_list=lesson_list, faq=faq,
        discuss_list=discuss_list
    )


COMMENT_COUNT = 'wechat_discuss_count_{c_id}_{u_id}'


def update_comment_count(course_id, discuss_id):
    """
    更新某用户在某课程下的提问的回复次数
    :param course_id: 课程id
    :param discuss_id: 问题id
    :return:
    """
    discuss = db.api.wike.discuss.get_discuss_by_id(discuss_id)
    if discuss.is_error():
        log.warn('get_discuss_by_id is failed. '
                 'discuss_id: {0}'.format(discuss_id))
    else:
        discuss = discuss.result()
        union_id = discuss['union_id']

        update_reply_count(course_id, union_id)


def get_comment_count(course_id, union_id):
    """
    获取某用户在某课程下的提问的回复次数
    :param course_id:
    :param union_id:
    :return:
    """

    count = get_reply_count(course_id, union_id).result()
    if not count or not isinstance(count, int):
        return 0
    return count


class WechatToken(object):
    app_id = settings.APPID
    secret = settings.SECRET

    def _access_token(self):
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
            self.app_id, self.secret)
        r = requests.get(url)
        token = json.loads(r.content)['access_token']
        cache.set('get_weixin_token', token, 6000)
        return token

    def get_access_token(self, from_cache=True):
        if from_cache:
            # 是否从缓存中取token
            val = cache.get('get_weixin_token')
            if not val:
                val = self._access_token()
        else:
            val = self._access_token()
        return val

    def _jsapi_ticket(self, from_cache=True):
        token = self.get_access_token(from_cache)
        url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi' % token
        r = requests.get(url)
        data = json.loads(r.content)
        if data['errcode'] != 0:
            return self._jsapi_ticket(from_cache=False)
        ticket = data['ticket']
        cache.set('get_weixin_jsapi_ticket', ticket, 6000)
        return ticket

    def get_jsapi_ticket(self):
        val = cache.get('get_weixin_jsapi_ticket')
        if not val:
            val = self._jsapi_ticket()
        return val


def random_string(n):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))


def wx_config(url):
    # 微信JS-SDK config
    data = {
        'noncestr': random_string(15),
        'jsapi_ticket': WechatToken().get_jsapi_ticket(),
        'timestamp': int(time.time()),
        'url': url
    }
    sign_string = '&'.join(['%s=%s' % (key, data[key]) for key in sorted(data)])
    data['signature'] = hashlib.sha1(sign_string).hexdigest()
    data['app_id'] = settings.APPID
    return data


def trans_xml_to_dict(xml):
    """
    将微信支付交互返回的 XML 格式数据转化为 Python Dict 对象

    :param xml: 原始 XML 格式数据
    :return: dict 对象
    """
    root = ElementTree.fromstring(xml)
    data = {}
    for child in root:
        data[child.tag] = child.text
    # soup = BeautifulSoup(xml, features='xml')
    # xml = soup.find('xml')
    # if not xml:
    #     return {}
    # # 将 XML 数据转化为 Dict
    # data = dict([(item.name, item.text) for item in xml.find_all()])
    return data


def trans_dict_to_xml(data):
    """
    将 dict 对象转换成微信支付交互所需的 XML 格式数据

    :param data: dict 对象
    :return: xml 格式数据
    """
    xml = []
    for k in sorted(data.keys()):
        v = data.get(k)
        if k == 'detail' and not v.startswith('<![CDATA['):
            v = '<![CDATA[{}]]>'.format(v)
        xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(xml))


def jsapi_pay(request, out_trade_no, body, total_fee, openid, course_id, course_name):
    # 获取用户ip
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        _temp_ip_list = request.META.get('HTTP_X_FORWARDED_FOR').split(',')
        if len(_temp_ip_list) > 0:
            ip = _temp_ip_list[0]
        else:
            ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_WL_PROXY_CLIENT_IP') or request.META.get('REMOTE_ADDR')
    else:
        ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_WL_PROXY_CLIENT_IP') or request.META.get('REMOTE_ADDR')
    if not ip:
        log.warn('wechat_wike_pay_ip_error')
        ip = '8.8.8.8'
    notify_url = settings.SITE_URL + reverse('wike:wechat_pay_notify')
    attach = json.dumps({
        'course_id': course_id,
        'course_name': course_name
    })
    data = dict(
        appid=settings.WEIXIN_PAY_APPID,
        mch_id=settings.WEIXIN_PAY_MCH_ID,
        nonce_str=random_string(15),
        body=body,
        out_trade_no=out_trade_no,
        total_fee=int(total_fee*100),
        spbill_create_ip=ip,
        notify_url=notify_url,
        trade_type='JSAPI',
        openid=openid,
        attach=attach
    )
    sign_string = '&'.join(['%s=%s' % (key, data[key]) for key in sorted(data)])
    sign_string = sign_string + '&key=' + settings.WEIXIN_PAY_KEY
    data['sign'] = hashlib.md5(sign_string).hexdigest().upper()
    xml_data = trans_dict_to_xml(data)
    try:
        r = requests.post(settings.WEIXIN_PAY_URL, data=xml_data,
                          headers={'Content-Type': 'application/xml'})
    except Exception as e:
        log.warn('wechat_pay_order' + str(e))
        return None
    result = trans_xml_to_dict(r.content)
    prepay_id = result.get('prepay_id')
    if not prepay_id:
        log.warn('wechat_wike_pay_order_fail: ' + r.content)
        return None
    log.info('wechat_pay_wike_order_success')
    return prepay_sign(prepay_id)


def prepay_sign(prepay_id):
    data = {
        'nonceStr': random_string(15),
        'timeStamp': int(time.time()),
        'appId': settings.WEIXIN_PAY_APPID,
        'package': 'prepay_id=%s' % prepay_id,
        'signType': 'MD5'
    }
    # 预支付id 签名
    sign_string = '&'.join(['%s=%s' % (key, data[key]) for key in sorted(data)])
    sign_string = sign_string + '&key=' + settings.WEIXIN_PAY_KEY
    data['paySign'] = hashlib.md5(sign_string).hexdigest().upper()
    return data


def verify_sign(data):
    sign_string = '&'.join(['%s=%s' % (key, data[key]) for key in sorted(data) if key != 'sign'])
    sign_string = sign_string + '&key=' + settings.WEIXIN_PAY_KEY
    sign = hashlib.md5(sign_string).hexdigest().upper()
    if sign == data['sign']:
        return True
    return False


def wechat_send_message_pay_success(open_id, attach, total_fee):
    try:
        attach = json.loads(attach)
        url = settings.SITE_URL + reverse('wike:wechat_course', kwargs={'course_id': attach['course_id']})
        data = {
            "touser": open_id,
            "template_id": "R_mtDO1D_QkeiY-rZvej4qoAjw2NgfsBuiU9_qEuku4",
            "url": url,
            "data": {
                "first": {
                    "value": "您已经成功报名麦子学院课程, 立刻开始学习吧！",
                    "color": "#173177"
                },
                "orderMoneySum": {
                    "value": "%s元" % total_fee,
                    "color": "#173177"
                },
                "orderProductName": {
                    "value": attach['course_name'],
                    "color": "#173177"
                },
                "Remark": {
                    "value": "如有问题请直接在微信留言，小麦将在第一时间为您服务！",
                    "color": "#173177"
                }
            }
        }
        data = json.dumps(data)
        token = WechatToken().get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % token
        r = requests.post(url, data=data, headers={'Content-Type': 'application/json'})
        content = json.loads(r.content)
        if content['errcode'] == 40001:
            token = WechatToken().get_access_token(from_cache=False)
            url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % token
            requests.post(url, data=data, headers={'Content-Type': 'application/json'})
    except Exception as e:
        log.warn('wechat_send_message_pay_success: %s' % str(e))
    return True
