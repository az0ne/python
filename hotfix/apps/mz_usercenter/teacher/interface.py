# -*- coding: utf-8 -*-
"""
@version: 2016/5/11
@author: zhangyunrui
@contact: david.zhang@maiziedu.com
@file: interface.py
@time: 2016/5/11 13:50
@note:  老师端接口
# """
import urllib, json, datetime
import db.api.onevone.meeting
from mz_eduadmin.students.interface import ClassStudentsInterface
from mz_lps.models import Class, ClassStudents
from mz_lps3.functions_gt import get_classmeeting_list
from mz_lps4.interface import update_join_url
from utils.logger import logger

# 0是可创建/未创建，1是已结束/未创建，2是已创建未被预约（CREATED）/可取消，3是已被预约（DATED）/不能取消（视为未创建）
STATUS_CAN_BE_CREATE = 0
STATUS_END = 1
STATUS_CREATED = 2
STATUS_DATED = 3
STATUS_ENTER = 4
STATUS_REVIEW = 5


class TeacherOverview(object):
    """
    教师信息
    """

    @staticmethod
    def processing_classes(teacher_id):
        """
        接口:一个老师所有进行中的班级
        :param teacher_id: int
        :return:
        class_list = [
            {
                'class_total_done_tasks': 新增作业(int, N),
                'class_id': 班级id(int, N+),
                'class_left_days': 班级倒计时(int, N+ or -1(班级未开始时class_left_days为-1)),
                'about_to_begin_clmt': 即将开始的班会(见mz_lps3.functions_gt.get_classmeeting_list),
                'class_begin_date': 开课日期(str, '%Y-%m-%d'),
                'total_progress': 班级完成度(int, [0, 100]),
                'class_coding': 班级编号(unicode),
                'students_status': {
                    'quit': (int, N),
                    'finish': 完成人数(int, N),
                    'normal': 正常人数(int, N),
                    'graduate': (int, N),
                    'paused': 休学人数(int, N),
                    'behind': 落后人数(int, N),
                    'total': 班级总人数(int, N(以上之和不包括quit和graduate)) @验证
                },
                'careercourse_name': 专业名(unicode)
            },
            ...
        ]
        """
        tclasses = Class.objects.xall().filter(
            teachers__id=teacher_id, lps_version='3.0', class_type=Class.CLASS_TYPE_NORMAL,
            status=Class.STATUS_ONGOING, is_active=True
        )

        class_list = list()
        for tclass in tclasses:
            _students = tclass.students.all().filter(classstudents__status=ClassStudents.STATUS_NORMAL)
            csi = ClassStudentsInterface(tclass.id, students_objs=_students)
            class_id = tclass.id

            iface = csi.iface

            # 包括临时班会.班会过了时间没开的话status会自动变为1.不包括正在进行中的班会
            about_to_begin_clmt = get_classmeeting_list(class_id, teacher_id)

            if about_to_begin_clmt:
                about_to_begin_clmt = about_to_begin_clmt[0]

            # 重新计算
            stu_data = csi.dashboard

            class_list.append(dict(
                careercourse_name=tclass.career_course.name,
                class_coding=tclass.coding,
                class_id=class_id,
                total_progress=iface.get_class_total_progress(),
                class_left_days=tclass.class_left_days or -1,  # 班级未开始时,class_left_days为-1
                class_total_done_tasks=iface.get_class_total_done_tasks(),
                # 开课日期是meeting_start(老师点击'开始班会'时生成),date_open在lps3已弃用
                class_begin_date=tclass.meeting_start.strftime('%Y-%m-%d') if tclass.meeting_start else '',
                about_to_begin_clmt=about_to_begin_clmt,  # 最近班会
                students_status=stu_data,
            ))

        return class_list

    @staticmethod
    def graduated_classes(teacher_id):
        """
        接口:一个老师所有毕业的班级
        :param teacher_id: int
        :return:
        class_list = [
            {
                'class_id': 班级id(int, N+),
                'class_coding': 班级编号(unicode),
                'careercourse_name': 专业名(unicode)
                'class_end_time': 班级毕业时间(str),
                'graduate_students': 毕业人数(int)
            },
            ...
        ]
        """
        tclasses = Class.objects.xall().filter(
            teachers__id=teacher_id, lps_version='3.0', class_type=Class.CLASS_TYPE_NORMAL,
            status=Class.STATUS_OVER, is_active=True
        )
        class_list = list()
        for tclass in tclasses:
            graduate_students = ClassStudents.objects.filter(
                student_class=tclass.id, status=ClassStudents.STATUS_NORMAL
            ).count()

            class_list.append(dict(
                careercourse_name=tclass.career_course.name,
                class_coding=tclass.coding,
                class_id=tclass.id,
                class_end_time=tclass.class_end_time.strftime('%Y-%m-%d') if tclass.class_end_time else '',
                # 毕业人数为:班级毕业时,班级所有未退学学生的人数
                graduate_students=graduate_students,
            ))

        return class_list

    @staticmethod
    def lps2_classes(teacher_id):
        """
        接口:一个老师所有进行中的班级
        :param teacher_id: int
        :return: cstudent_list = [
            {
                'careercourse_image': 职业课程图片url(str),
                'careercourse_name': 专业名(unicode),
                'careercourse_color': 职业课程颜色(str),
                'careercourse_id': 职业课程id(int),
                'class_id': 班级id(int, N+),
                'class_coding': 班级编号(unicode),
            },
            ...
        ]
        """
        tclasses = Class.objects.xall().filter(
            teachers__id=teacher_id, class_type=Class.CLASS_TYPE_NORMAL, is_active=True
        ).exclude(lps_version='3.0')

        class_list = list()
        for tclass in tclasses:
            ccourse = tclass.career_course

            class_list.append(dict(
                careercourse_id=ccourse.id,
                careercourse_name=ccourse.name,
                careercourse_image=ccourse.image.url,
                careercourse_color=ccourse.course_color,
                class_id=tclass.id,
                class_coding=tclass.coding,
            ))

        return class_list


def show_onevone_meeting(meeting_id):
    """
    展示1v1直播详情
    :param meeting_id:
    :return:
    """
    result = db.api.onevone.meeting.get_onevone_meeting_by_id(meeting_id)
    if result.is_error():
        logger.warn('get_onevone_meeting_by_id is error meeting_id:%s' % meeting_id)
        return None
    onevone_meeting = result.result()

    # try:
    #     nick_name = onevone_meeting['teacher_real_name'] or onevone_meeting['teacher_nick_name']
    #     # 加入地址
    #     values = {'nickname': nick_name, 'token': onevone_meeting['teacher_token']}
    #     teacher_join_url = onevone_meeting['teacher_url'] + '?' + urllib.urlencode(values)
    #     onevone_meeting['teacher_join_url'] = teacher_join_url
    #     # 录播地址
    #     if onevone_meeting['video_url']:
    #         video_values = {'nickname': nick_name, 'token': onevone_meeting['video_token']}
    #         video_join_url = onevone_meeting['video_url'] + '?' + urllib.urlencode(video_values)
    #     else:
    #         video_join_url = ''
    #     onevone_meeting['video_join_url'] = video_join_url
    # except Exception as e:
    #     logger.warn(str(e))
    #     return None
    try:
        is_video = onevone_meeting.get('status', 'CREATE') == 'ENDED'
        join_url = update_join_url(onevone_meeting, is_teacher=True, is_video=is_video)
    except Exception as e:
        logger.warn(str(e))
    else:
        onevone_meeting.update({'join_url': join_url})

    return onevone_meeting


def check_onevone_meeting(_start_time, teacher_id):
    """
    检查1v1直播POST数据格式的正确性
    :param _start_time:
    :param teacher_id:
    :return:
    """
    try:
        start_time = datetime.datetime.strptime(_start_time, '%Y-%m-%d %H:%M')
    except Exception:
        raise Exception(u'传入时间格式错误，请联系老师')
    end_time = start_time + datetime.timedelta(minutes=30)
    now = datetime.datetime.now()

    assert start_time > now + datetime.timedelta(minutes=30), u'预约时间离现在小于30分钟或者该时间已过去'

    result = db.api.onevone.meeting.check_meeting_time(teacher_id, start_time, end_time)
    if result.is_error():
        logger.warn('check_meeting_time is error, teacher_id %s' % teacher_id)
        raise Exception(u'查询可预约时间失败，请重新预约')
    assert result.result() is None, u'请重新选择时间，所选时间刚被预约'
    return start_time, end_time


def serialize_onevone_meeting(teacher_id, time_list, date_list, user_id=0):
    """
    序列化1v1直播
    :return:
    """
    meetings, s_meetings, _s_meetings, selected_meetings = [], {}, {}, {}
    now = datetime.datetime.now()
    _begin_date = date_list[0]
    date_len = len(date_list)

    _date = _begin_date.split('-')
    begin_date = datetime.datetime(*map(lambda x: int(x), _date))
    end_date = begin_date + datetime.timedelta(days=date_len)
    now_after_3 = now + datetime.timedelta(hours=3)

    # 如果有用户id，说明是学生在调用
    if user_id:
        _meetings = db.api.onevone.meeting.\
            get_onevone_meeting_by_user_id(teacher_id, now_after_3, user_id, begin_date, end_date)
    else:
        _meetings = db.api.onevone.meeting.get_onevone_meeting_by_teacher_id(teacher_id, begin_date, end_date)

    if _meetings.is_error():
        logger.warn('get_onevone_meeting is error teacher_id is %s' % teacher_id)
    else:
        meetings = list(_meetings.result())

    if meetings:
        is_selected, _is_selected = 0, 0
        if begin_date < now < end_date:
            is_selected = 1
        for m in meetings:
            time_key = '%s-%s' % (m['start_time'].strftime('%H:%M'), m['end_time'].strftime('%H:%M'))
            _s_meetings.setdefault(time_key, {})
            day_key = m['start_time'].strftime('%Y-%m-%d')
            _status = STATUS_CREATED
            # 如果是DATED且不是自己预约的，显示‘已被预约’（学生端）
            if m['status'] == 'DATED' and m['user_id'] != unicode(user_id):
                _status = STATUS_DATED
            # 如果是START或DATED，且自己预约的，显示‘进入’（学生端）
            elif m['status'] in ('START', 'DATED') and m['user_id'] == unicode(user_id):
                _status = STATUS_ENTER
            # 如果有录播地址，显示‘回看’（学生端）
            elif m['user_id'] == unicode(user_id) and m['video_url'] and m['status'] == 'ENDED':
                _status = STATUS_REVIEW
            elif m['start_time'] > now_after_3 and _is_selected == 0 and is_selected == 1:
                _is_selected = is_selected
                is_selected = 0
            else:
                _is_selected = 0
            _s_meetings[time_key].setdefault(day_key, {'id': m['id'], 'status': _status, 'is_selected': _is_selected})

    is_break = False
    is_selected = 0
    if begin_date < now < end_date:
        is_selected = 1
    for d in date_list:
        if is_break:
            break
        else:
            for t in time_list:
                try:
                    _s_meetings[t][d]
                except KeyError:
                    if datetime.datetime.strptime(d + ' ' + t.split('-')[0], '%Y-%m-%d %H:%M') > now_after_3:
                        selected_meetings = {t: {d: is_selected}}
                        is_break = True
                        break

    for t in time_list:
        s_meetings.setdefault(t, {})
        begin_time = t.split('-')[0].split(':')
        hour_dict = dict(
            hour=int(begin_time[0]),
            minute=int(begin_time[1])
        )
        for d in date_list:
            _time = datetime.datetime(*map(lambda x: int(x), d.split('-')), **hour_dict)
            if _time < now_after_3:
                # 如果有班会记录且有录播地址，显示‘回看’
                try:
                    if _s_meetings[t][d]['status'] == STATUS_REVIEW or _s_meetings[t][d]['status'] == STATUS_ENTER:
                        s_meetings[t][d] = _s_meetings[t][d]
                    else:
                        s_meetings[t][d] = {'id': 0, 'status': STATUS_END}
                except KeyError:
                    s_meetings[t][d] = {'id': 0, 'status': STATUS_END}
            else:
                try:
                    s_meetings[t][d] = _s_meetings[t][d]
                except KeyError:
                    try:
                        is_selected_add = selected_meetings[t][d]
                    except KeyError:
                        is_selected_add = 0
                    s_meetings[t][d] = {'id': 0, 'status': STATUS_CAN_BE_CREATE, 'is_selected': is_selected_add}

    return s_meetings
