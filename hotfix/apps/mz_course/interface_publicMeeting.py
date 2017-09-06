# -*- coding: utf-8 -*-
from core.common.http.response import success_json, failed_json
from utils.sms_manager import tpl_send_sms, send_sms, get_templates_id
from django.utils.crypto import get_random_string
from django.conf import settings
import datetime
from mz_common.models import MobileVerifyRecord
from django.db.models import Q
from mz_user.interface import UserBaseInterface
import db.api.course.careerPublicMeeting
from utils.tool import get_param_by_request
from utils.logger import logger as log


def mobile_send_captcha(request):
    """
    手机发送短信
    :param request:
    :return:
    """
    # 手机校验
    mobile = get_param_by_request(request.POST, "mobile", "", str)
    class_time = get_param_by_request(request.POST, "class_time", "", str)
    career_id = get_param_by_request(request.POST, "career_id", 0, int)
    random_str = get_random_string(length=6, allowed_chars='0123456789')
    if not mobile:
        return failed_json(u'请输入手机号')
    data = db.api.course.careerPublicMeeting.get_my_public_meeting_data(mobile, career_id, class_time)
    if data.is_error():
        log.warn("get public meeting data failed. mobile:%s,career_id:%s" % (mobile, career_id))
        return failed_json(u'server error ')
    if data.result():
        return failed_json(u'您输入的手机号已预约')
    ip = request.META.get('HTTP_X_REAL_IP') or request.META.get('REMOTE_ADDR', "")
    result = UserBaseInterface.can_send_sms(mobile, ip)
    if not result[0]:
        return failed_json(result[1])

    # 短信发送记录写入数据库
    mobile_record = MobileVerifyRecord()
    mobile_record.code = random_str
    mobile_record.mobile = mobile
    mobile_record.type = 2  # 课程预约
    mobile_record.ip = ip
    mobile_record.source = 1  # 来自PC
    try:
        mobile_record.save()
    except Exception as e:
        log.warn("MobileVerifyRecord save failed %s" % e)

    # 发送短信
    tpl_send_sms(
        settings.SMS_APIKEY, settings.SMS_TPL_ID, random_str, mobile)

    return success_json({})


def mobile_verify_captcha(request):
    """
    验证手机验证码
    :param request:
    :return:
    """

    mobile = get_param_by_request(request.POST, "mobile", "", str)
    mobile_code = get_param_by_request(request.POST, "mobile_code", "", str)
    class_time = get_param_by_request(request.POST, "class_time", "", str)
    career_id = get_param_by_request(request.POST, "career_id", 0, int)
    data = db.api.course.careerPublicMeeting.get_my_public_meeting_data(mobile, career_id, class_time)
    if data.is_error():
        log.warn("get public meeting data failed. mobile:%s,career_id:%s" % (mobile, career_id))
        return failed_json(u'server error ')

    if data.result():
        return failed_json(u'您输入的手机号已预约')

    if not mobile_code:
        return failed_json(u'请输入验证码')

    record = MobileVerifyRecord.objects.filter(Q(mobile=mobile), Q(code=mobile_code), Q(type=2)).order_by("-created")
    if record:
        if datetime.datetime.now() - datetime.timedelta(minutes=30) > record[0].created:
            return failed_json(u'验证码已过期')
    else:
        return failed_json(u'验证码不正确')

    return success_json({})


def public_meeting_send_success_sms(task_title, mobile, class_time, qq_group, template_name):
    '''
    发送预约课程成功的通知短信
    :param task_title: 课程标题
    :param template_name: 短信模板名称
    :param mobile:  手机
    :param class_time: 开课时间
    :param qq_group: qq群
    :return:
    '''
    try:
        format_class_time = datetime.datetime.strptime(class_time, '%Y-%m-%d %H:%M')
        send_sms(settings.SMS_APIKEY, get_templates_id(template_name),
                 mobile.encode('utf-8'), task_title.encode('utf-8'), qq_group.encode('utf-8'),
                 format_class_time.strftime('%Y年%m月%d日%H时%M分'))

    except Exception as e:
        log.warn("send sms error.info:%s" % e)


def public_meeting_send_sms_3hours_ago():
    '''
    开课前三个小时发通知短信
    :return:
    '''
    get_not_started_meetings = db.api.course.careerPublicMeeting.get_not_started_meeting()  # 看是否有未开始的直播课程，如果有则循环查看开课时间，进行判断
    if get_not_started_meetings.is_error():
        log.warn("get not started meeting fail.")
    meetings = get_not_started_meetings.result()
    if meetings:
        for meet in meetings:
            if datetime.timedelta(minutes=180) > meet["class_time"] - datetime.datetime.now() > datetime.timedelta(
                    minutes=150):   #  如果当前时间距离开课时间在150-180分钟之间则进行下一步判断
                career_id = meet["id"]
                class_time = meet["class_time"]
                free_task_id = meet["free_task_id"]
                get_task = db.api.course.careerPublicMeeting.get_public_meeting_task_info_by_task_id(free_task_id)
                if get_task.is_error():
                    log.warn("get task info fail. free_task_id:%s" % free_task_id)
                    continue
                task_info = get_task.result()
                task_title = task_info["title"]
                get_meeting_data = db.api.course.careerPublicMeeting.get_meeting_data_by_course(career_id=career_id)
                if get_meeting_data.is_error():
                    log.warn("get meeting data fail.career_id=%s" % career_id)
                    continue
                meeting_data = get_meeting_data.result()
                if meeting_data:
                    for data in meeting_data:
                        mobile = data["mobile"]
                        qq_group = data["qq_group"]
                        template_name = "public_meeting_start_notify"
                        str_class_time = datetime.datetime.strftime(class_time, '%Y年%m月%d日%H时%M分')
                        try:
                            send_sms(settings.SMS_APIKEY, get_templates_id(template_name),
                                     mobile.encode('utf-8'), task_title.encode('utf-8'), str_class_time,
                                     qq_group.encode('utf-8'))
                        except Exception as e:
                            log.warn("send notify sms error.info:%s" % e)
