# -*- coding: utf-8 -*-

"""
@version: 2016/6/12
@author: Jackie
@contact: jackie@maiziedu.com
@file: interface.py
@time: 2016/6/12 15:25
@note:  ??
"""
import datetime, urllib, re
from django.db import transaction
from collections import OrderedDict
from db.api import get_free_class_list, exist_free_class
from mz_lps3.functions_gt import create_liveroom
from mz_lps3_free.common.interface import get_free_class_weekday
from mz_lps.models import Class, ClassTeachers
from mz_course.models import CareerCourse
from mz_lps3.models import ClassMeeting, ClassMeetingRelation
from mz_user.models import UserProfile

CLASS_MEETING_STATUS = {0: u"未开始", 1: u"已结束", 2: u"进行中"}

@transaction.commit_manually
def create_free_class(career_course_id, first_datetime, answer_datetime, teacher_id):
    """
    添加免费试学班
    :param career_course_id: 职业课程ID（int）
    :param first_datetime: 首次班会时间（datetime）
    :param answer_datetime: 答疑班会时间(datetime)
    :param teacher_id: 老师ID(int)
    :return: class obj
    """


    # 创建试学班级
    if not isinstance(first_datetime, datetime.datetime):
        raise Exception('first_datetime not is datetime')
    if not isinstance(answer_datetime, datetime.datetime):
        raise Exception('answer_datetime not is datetime')
    try:
        career_course = CareerCourse.objects.get(pk=career_course_id)
    except CareerCourse.DoesNotExist:
        return False, u'职业课程不存在'
    try:
        teacher = UserProfile.objects.get(pk=teacher_id)
        if not teacher.is_teacher():
            return False, u'创建者必须是老师'
    except CareerCourse.DoesNotExist:
        return False, u'老师ID不存在'

    name = first_datetime.strftime('%m.%d') + '-' + answer_datetime.strftime('%m.%d')
    coding = career_course.short_name.upper() + name
    meeting_duration = (answer_datetime - first_datetime).days

    try:
        class_obj = Class.objects.create(name=name, career_course=career_course, coding=coding,
                                         class_type=Class.CLASS_TYPE_FREE_488, date_open=datetime.datetime.now(),
                                         meeting_enabled=True, meeting_start=datetime.datetime.now(),
                                         meeting_duration=meeting_duration, student_limit=999, lps_version='3.0')
        ClassTeachers.objects.create(teacher_id=teacher_id, teacher_class=class_obj)
        # 创建首次班会
        classmeeting_first = ClassMeeting.objects.create(startline=first_datetime, status=0, content='首次班会',
                                                         create_id=teacher.id)
        ClassMeetingRelation.objects.create(class_meeting=classmeeting_first, class_id=class_obj.id)
        flags, log = create_liveroom(teacher, classmeeting_first, [class_obj])  # 创建班会后，创建直播室
        if not flags:
            transaction.rollback()
            return False, log
        # 创建答疑班会
        classmeeting_answer = ClassMeeting.objects.create(startline=answer_datetime, status=0, content='答疑班会',
                                                          create_id=teacher.id)
        ClassMeetingRelation.objects.create(class_meeting=classmeeting_answer, class_id=class_obj.id)
        flags, log = create_liveroom(teacher, classmeeting_answer, [class_obj])  # 创建班会后，创建直播室
        if not flags:
            transaction.rollback()
            return False, log
    except Exception,e:
        transaction.rollback()
    else:
        transaction.commit()
    return True, ''


def is_free_class(career_course_id, teacher_id, first_date, answer_date):
    """
    是否已经有了免费试学班级
    :param career_course_id: 职业课程ID（int）
    :param teacher_id: 老师ID(int)
    :param first_date: 首次班会日期（yyyy-mm-dd）
    :param answer_date: 答疑班会日期（yyyy-mm-dd）
    :return: bool
    """
    from mz_course.models import CareerCourse
    from mz_user.models import UserProfile

    pattern = '^((?:19|20)\d\d)/(0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])$'
    # pattern1 = '^((?:19|20)\d\d)-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])$'
    if not re.match(pattern, first_date):
        raise Exception(u'首次班会时间格式不正确')
    if not re.match(pattern, answer_date):
        raise Exception(u'答辩班会时间格式不正确')

    try:
        CareerCourse.objects.get(pk=career_course_id)
    except CareerCourse.DoesNotExist:
        raise Exception(u'职业课程不存在')
    try:
        if not UserProfile.objects.get(pk=teacher_id).is_teacher():
            raise Exception(u'创建者必须是老师')
    except CareerCourse.DoesNotExist:
        raise Exception(u'老师ID不存在')
    api_result = exist_free_class(career_course_id, teacher_id, first_date, answer_date)
    if not api_result.is_error():
        if api_result.result():
            return True, u''
    return False, u'免费试学班不存在'


def get_free_classes_by_teacher(teacher, page_index, page_size):
    """
    获取所有免费试学班的list
    :param teacher: 教师(user)
    :param page_index: 当前页码(int)
    :param page_size: 每页条数(int)
    :return:{}
    """

    from mz_lps3.models import UserTaskRecord

    free_class_dict = OrderedDict()
    api_result = get_free_class_list(teacher.id, page_index, page_size)
    if not api_result.is_error():
        for result in api_result.result():
            values = {'nickname': teacher.real_name or teacher.nick_name, 'token': result['token']}
            class_meeting_dict = dict(
                content=result['content'],
                startline=result['startline'],
                d_week=get_free_class_weekday(result['startline'].weekday()),
                d_date=result['startline'].strftime("%m.%d"),
                d_time=result['startline'].strftime("%H:%M"),
                class_meeting_status=CLASS_MEETING_STATUS.get(result['class_meeting_status'], u'未知状态'),
                join_url=result['join_url'] + '?' + urllib.urlencode(values)
            )
            if free_class_dict.has_key(result['id']):
                class_meeting_list = free_class_dict[result['id']]['class_meeting']
                class_meeting_list.append(class_meeting_dict)
                # 计算班级状态
                free_class_dict[result['id']]['class_status'] = _get_free_class_status(
                    class_meeting_list[0]['class_meeting_status'], class_meeting_dict['class_meeting_status'])
            else:
                data = dict(
                    class_name=result['class_name'],
                    meeting_duration=result['meeting_duration'],
                    career_course_name=result['career_course_name'],
                    new_task_count=UserTaskRecord.objects.values('id').filter(class_id=result['id'],
                                                                              status='DONE').count(),

                    class_meeting=[class_meeting_dict]
                )
                free_class_dict[result['id']] = data

    return free_class_dict


def _get_free_class_status(first_meeting_status, answer_meeting_status):
    """
    获取并且计算免费试学班级状态
    :param first_meeting_status: 首次班会状态(int)
    :param answer_meeting_status: 答辩班会状态(int)
    :return:
    """
    if first_meeting_status == u'未开始':
        return u'未开始'
    if first_meeting_status != u'未开始' and answer_meeting_status != u'已结束':
        return u'进行中'
    if answer_meeting_status == u'已结束':
        return u'已结束'


def get_count_free_class(teacher):
    """
    获取免费试学班的数量
    :param teacher: 教师(user)
    :return:
    """
    from mz_lps.models import Class

    return Class.objects.xall().values('id').filter(teachers=teacher, lps_version='3.0',
                                                    class_type=Class.CLASS_TYPE_FREE_488,
                                                    meeting_enabled=True).count()


def get_career_course_list():
    """
    获取免费试学所以职业课程
    :return:
    """
    from mz_lps.models import CareerCourse

    career_course_list = CareerCourse.objects.values('id', 'name').filter(enable_free_488=True)
    return career_course_list
