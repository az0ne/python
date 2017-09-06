# -*- coding:utf-8 -*-
from django.conf import settings
import httplib
import urllib
from celery_tasks import app
import requests, json
from utils.yuntongxun.SendTemplateSMS import sendTemplateSMS
from utils.logger import logger as log

# 服务地址
host = settings.SMS_HOST
# 端口号
port = settings.SMS_PORT
# 版本号
version = settings.SMS_VERSION
# 查账户信息的URI
user_get_uri = "/" + version + "/user/get.json"
# 通用短信接口的URI
sms_send_uri = "/" + version + "/sms/send.json"
# 模板短信接口的URI
sms_tpl_send_uri = "/" + version + "/sms/tpl_send.json"

sms_templates_id = {'interest_student_info': '62319',
                    'tel_contact': '62323',
                    'reg_success': '62328',
                    'reserve_success': '62326',
                    'apply_pay_success': '62324',
                    'course_time_change': '62317',
                    'reg_success_notify': '62315',
                    'course_begin': '62312',
                    'suggestion_accept': '62784',
                    'verification_code': '61912',
                    'classmeeting_notify': '76865',
                    'classmeeting_absence': '67403',
                    'join_class_notify': '108665',
                    'join_class_edu_admin': '77913',
                    'studying_reminder': '67397',
                    'studying_paused': '67405',
                    'studying_score_abc': '67393',
                    'studying_score_d': '67395',
                    'student_deadline_quit': '80782',
                    'ordered_free_class_success': '106529',
                    'start_free_class_meeting_3hour': '106531',
                    'public_meeting_success_notify': '106381',
                    'public_meeting_start_notify': '106384',
                    'tel_contact_2': '117113',
                    'interest_student_info_2': '117110',
                    'onevone_meeting_ordered': '117613',
                    'onevone_meeting_start': '117614',
                    'onevone_service_teacher_unread': '119727',
                    'join_class_notify_3_1': '119798',
                    'qa_teacher_5_unread': '126659',
                    'app_join_class_service': '137571',                    
                    'pay_success_4_0': '136875',
                    'perfect_user_info_timeout': '136882',
                    'app_teacher_waring': '132011',

                    'app_teacher_project': '139280',
                    'app_teacher_briefing': '139287',
                    'teacher_meeting': '139282',
                    'student_meeting': '139295',
                    'teacher_meeting_open': '139283',
                    'student_meeting_open': '139297',
                    'teacher_meeting_cancel_student': '139284',
                    'teacher_meeting_cancel_teacher': '139294',
                    'student_meeting_cancel': '139301',

                    'student_order_onevone': '141833',
                    'student_onevone_begin_in_5m': '141834',
                    'student_cancel_onevone': '141836',
					'ops_notify': '144492'
                    }


def get_templates_id(template_name):
    return sms_templates_id[template_name]


def get_user_info(apikey):
    """
    取账户信息
    """
    conn = httplib.HTTPConnection(host, port=port)
    conn.request('GET', user_get_uri + "?apikey=" + apikey)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def disable_sms(func):
    def inner(*args, **kwargs):
        if hasattr(settings, 'MOBILE_WHITELIST'):
            if args[2] in settings.MOBILE_WHITELIST:
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)
    return inner


@app.task(name='sms_manager.send_sms')
@disable_sms
def send_sms(apikey, tpl_id, mobile, *value):
    """
    能用接口发短信
    """
    return sendTemplateSMS(mobile, value, tpl_id)


@app.task(name='sms_manager.tpl_send_sms')
def tpl_send_sms(apikey, tpl_id, tpl_value, mobile):
    """
    模板接口发短信
    """
    return sendTemplateSMS(mobile, [tpl_value], get_templates_id('verification_code'))


def sms_whitelist(func):
    """
    短信白名单
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        if hasattr(settings, 'MOBILE_WHITELIST'):
            if args[0] in settings.MOBILE_WHITELIST:
                return func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper


@sms_whitelist
def send_sms_new(mobile, tmp_name, content_sms):
    """
    新的发送短信接口，依赖于王琦写的后台发送服务
    :param mobile: int
    :param tmp_name: 模板别名
    :param content_sms: list 模板参数
    :return:
    """
    try:
        if not mobile:
            log.warn("send_sms_new method failed. details: mobile is None")
            return
        requests.post(settings.SEND_SMS_URL+"push/", data=json.dumps({
              "sender": "sms",
              "args": {
                  "to": mobile,
                  "tpl_key": get_templates_id(tmp_name),
                  "msg": "[" + ','.join(["\"%s\"" % _c for _c in content_sms]) + "]"
              }
        }), timeout=2)
    except Exception, e:
        log.warn("send_sms_new method failed. details: %s" % str(e))
