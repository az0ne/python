# -*- coding: utf-8 -*-

"""
@version: 2016/6/12
@author: Jackie
@contact: jackie@maiziedu.com
@file: interface.py
@time: 2016/6/12 15:25
@note:  ??
"""
from django.conf import settings
from db.api.lps import classes as api_free_class
from mz_lps3_free.common.interface import Free488ClassInterface
from utils.sms_manager import send_sms, get_templates_id
from utils.logger import logger as log

def get_free_class_and_class_meeting_list(career_course_id):
    """
    获取免费试学班和班会信息
    :param career_course_id: 职业课程ID
    :return:
    """
    free_class_info_list = []
    # 获取开设了免费试学班的老师信息，和班级ID
    teacher_info = api_free_class.get_free_class_teacher_info_by_career_course_id(career_course_id).result()
    for teacher_info in teacher_info:
        teacher = dict(
            id=teacher_info['id'],
            staff_name=teacher_info['real_name'] or teacher_info['nick_name'],
            show_position=teacher_info['position'] or u'金牌讲师',
            avatar_url=teacher_info['avatar_url'],
            description=teacher_info['description']
        )
        # 老师下所有为开始的试学班级
        free488_class_list = []
        class_id_list = teacher_info['str_class_id'].split(',')[:3]
        for class_id in class_id_list:
            free488_class_list.append(Free488ClassInterface(class_id))
        free_class_info_list.append(dict(teacher=teacher, free488_class_list=free488_class_list))
    return free_class_info_list


def send_sms_ordered_free_class_success(_class, mobile):
    """
    预约班级成功发送短信息
    :param class_obj:
    :return:
    """
    career_course_name = _class.career_course.name
    free488_class = Free488ClassInterface(_class.id)
    meeting_time = free488_class.first_meeting['startline']
    try:
        send_sms.delay(settings.SMS_APIKEY, get_templates_id('ordered_free_class_success'), mobile,
                       career_course_name, meeting_time.strftime('%Y年%m月%d日%H时%M分'))
    except Exception, e:
        log.error("send_sms ordered_free_class_success error message:%s" % str(e))
