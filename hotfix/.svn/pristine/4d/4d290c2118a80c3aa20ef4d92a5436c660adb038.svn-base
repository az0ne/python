# -*- coding: utf-8 -*-
import datetime
import re
from collections import OrderedDict
from django.conf import settings
from django.http.response import Http404

import db.api.lps.student
import db.api.lps.teacher_warning
import db.api.common.new_discuss_post
import db.api.common.new_discuss
import db.api.onevone.study_service
from core.common.utils.serializers import get_week_dict
from mz_common.function_discuss import get_one_question
from mz_lps3.functions_nj import StageTaskInterface
from mz_lps4.class_dict import NORMAL_CLASS_DICT
from mz_lps4.models import OnevoneMeeting
from utils.logger import logger as log

LEVEL_1 = '1'
LEVEL_2 = '2'
LEVEL_3 = '3'
LEVEL_4 = '4'


def get_app_teacher_info(user, is_self=None):
    user_dict = dict(
        token=is_self,
        account=user.username,
        mobile=user.mobile if user.valid_mobile == 1 and user.mobile else '',
        name=user.real_name or user.nick_name,
        teacher_id=user.id,
        avatar=settings.SITE_URL + settings.MEDIA_URL + str(user.avatar_small_thumbnall)
    )
    for k, v in user_dict.iteritems():
        if v is None:
            user_dict[k] = ''
    return user_dict


def get_teacher_warning_backlog_by_teacher_id_interface(teacher_id):
    """
    获取老师处理待处理任务记录接口
    :param teacher_id:
    :return:
    """
    # get db data
    backlog = []
    result = db.api.lps.teacher_warning.get_teacher_warning_backlog_by_teacher_id(teacher_id=teacher_id)
    if result.is_error():
        log.warn("db get_teacher_warning_backlog_by_teacher_id error, teacher_id: %s" % teacher_id)
    else:
        backlog = list(result.result())

    sum_num = '0'
    result = db.api.lps.teacher_warning.get_teacher_warning_backlog_count_by_teacher_id(teacher_id=teacher_id)
    if result.is_error():
        log.warn("db get_teacher_warning_backlog_count_by_teacher_id error, teacher_id: %s" % teacher_id)
    else:
        sum_num = str(result.result()) if result.result() else '0'

    # init data_structure and literal
    list_1, list_2, list_3, list_4 = [], [], [], []
    now = datetime.datetime.now()

    def format_b(ele):
        """
        format db data to api data and add to list
        :param ele:
        :return:
        """
        # catch outer exception
        try:
            deadline = ele['warn_three_date']
            ele['deadline'] = deadline
            warn_two_date = ele['warn_two_date']
            warn_one_date = ele['warn_one_date']
            ele['avatar'] = settings.SITE_URL + settings.MEDIA_URL + ele['avatar']
            del ele['warn_two_date'], ele['warn_one_date'], ele['warn_three_date']
            assert isinstance(deadline, datetime.datetime)
            assert isinstance(warn_two_date, datetime.datetime)
            assert isinstance(warn_one_date, datetime.datetime)
        except (ValueError, KeyError, AssertionError) as e:
            log.warn('forloop in backlog, %s' % e)
            return 1

        # get priority
        if now >= deadline:
            level = LEVEL_1
            l = list_1
        elif now >= warn_two_date:
            level = LEVEL_2
            l = list_2
        elif now >= warn_one_date:
            level = LEVEL_3
            l = list_3
        else:
            level = LEVEL_4
            l = list_4
        ele.setdefault('priority', level)

        # value int, datetime to str
        for k, v in ele.iteritems():
            if isinstance(v, (int, long)):
                v = str(v)
            if isinstance(v, datetime.datetime):
                v = v.strftime('%F %T')
            ele[k] = v
        ele.setdefault('date', deadline.strftime('%Y/%m/%d'))
        week_dict, day_dict = get_week_dict()
        ele.setdefault('weekday',
                         "%s(%s)" % (
                             day_dict.get(deadline.strftime('%F'), "周%s" % week_dict[int(deadline.strftime('%w'))]),
                             deadline.strftime('%m-%d')))
        l.append(ele)

    for b in backlog:
        if format_b(b):
            return {'success': False}

    data = dict(
        sum_num=sum_num,
        list=list_1 + list_2 + list_3 + list_4
    )

    return {'success': True, 'data': data}


def get_meeting_list_interface(teacher_id):
    """
    获取班会列表接口
    :param teacher_id:
    :return:
    """
    now = datetime.datetime.now()

    result = db.api.lps.teacher_warning.get_meeting_list(teacher_id)
    if result.is_error():
        log.warn("db get_meeting_list error, teacher_id %s", teacher_id)
        return dict(success=False, msg=u"服务器开小差了,稍后再试吧")
    meetings = result.result()

    new_list = []
    week_dict, day_dict = get_week_dict()

    def format_d(_dict):
        if _dict['is_new']:
            new_list.append(1)
        start_time = _dict['start_time']
        _dict['start_time'] = start_time.strftime('%R')
        _dict['end_time'] = _dict['end_time'].strftime('%R')
        _dict.setdefault('status', 1 if _dict['user_id'] else 0)
        _dict.setdefault('date', start_time.strftime('%Y/%m/%d'))
        _dict.setdefault('weekday',
                         "%s(%s)" % (
                             day_dict.get(start_time.strftime('%F'), start_time.strftime('%m-%d')),
                             "周%s" % week_dict[int(start_time.strftime('%w'))]))
        _dict['is_new'] = _dict['is_new'] or '0'

        try:
            _dict['avatar'] = settings.SITE_URL + settings.MEDIA_URL + _dict['avatar']
            _dict['create_time'] = _dict['create_time'].strftime('%Y/%m/%d %T')
            if now >= _dict['warn_one_date']:
                _dict.setdefault('priority', LEVEL_2)
            else:
                _dict.setdefault('priority', LEVEL_4)
        except Exception:
            pass
        del _dict['warn_one_date'], _dict['warn_two_date'], _dict['user_id']

        # value int, datetime to str
        for k, v in _dict.iteritems():
            if isinstance(v, (int, long)):
                v = str(v)
            _dict[k] = v

        return _dict

    try:
        data = [format_d(m) for m in meetings]
    except Exception as e:
        log.warn('function format_d, %s' % str(e))
        return dict(success=False, msg=u"服务器开小差了,稍后再试吧")

    data = dict(
        sum_num=str(len(new_list)),
        list=data
    )

    return dict(success=True, data=data)


def get_backlog_detail_by_id_interface(backlog_id):
    """
    获取1v1服务详情接口
    :param backlog_id:
    :return:
    """
    # get db data
    backlog = {}
    result = db.api.lps.teacher_warning.get_backlog_detail_by_id(backlog_id)
    if result.is_error():
        log.warn("db get_backlog_detail_by_id error, backlog_id: %s" % backlog_id)
    else:
        backlog = result.result()

    # init data_structure and literal
    now = datetime.datetime.now()

    def format_b(ele):
        """
        format db data to api data and add to list
        :param ele:
        :return:
        """
        # catch outer exception
        try:
            deadline = ele['warn_three_date']
            warn_two_date = ele['warn_two_date']
            warn_one_date = ele['warn_one_date']
            obj_id = ele['obj_id']
            del ele['warn_two_date'], ele['warn_one_date']
            assert isinstance(deadline, datetime.datetime)
            assert isinstance(warn_two_date, datetime.datetime)
            assert isinstance(warn_one_date, datetime.datetime)
        except (ValueError, KeyError, AssertionError) as e:
            log.warn('forloop in backlog, %s' % e)
            return 1

        # get priority
        if now >= deadline:
            level = LEVEL_1
        elif now >= warn_two_date:
            level = LEVEL_2
        elif now >= warn_one_date:
            level = LEVEL_3
        else:
            level = LEVEL_4
        try:
            ele.clear()
            ele.setdefault('priority', level)
            ele.setdefault('deadline', deadline.strftime('%F %T'))
            ele.setdefault('obj_id', obj_id)
        except Exception as e:
            log.warn('set ele data error, %s' % str(e))
            return 1

    if format_b(backlog):
        log.warn('format_b is error, backlog_id: %s' % backlog_id)
        return {'success': False, 'msg': u"服务器开小差了,稍后再试吧"}

    return {'success': True, 'data': backlog}


def get_question_detail_interface(problem_id, user_id):
    """
    问题详情接口
    :param problem_id:
    :param user_id:
    :return:
    """
    # get db data
    result = db.api.common.new_discuss.get_problem_by_id(problem_id, user_id)
    if result.is_error():
        log.warn('get_problem_by_id not data,problem_id is %s' % problem_id)
        raise Http404
    problem_info = result.result()
    try:
        answer_list = get_one_question(user_id, problem_id)
    except Exception, e:
        log.warn('function get_one_questions is error, user: %s, discuss_id:%s  %s' % (user_id, problem_id, e))
        answer_list = []

    def format_d(_dict):
        """
        序列化字典
        :param _dict:
        :return:
        """
        user_type_dict = {'student': 2, 'teacher': 3}
        new_dict = dict(
            comment_id=_dict['id'],
            name=_dict['nick_name'],
            avatar=settings.SITE_URL + settings.MEDIA_URL + _dict['head'],
            user_type=user_type_dict.get(_dict['group_name'], 1),
            create_time=_dict['create_date'].strftime('%Y/%m/%d %T'),
            content=_dict['comment'],
            user_id=_dict['user_id'],
            problem_id=_dict.get('problem_id', _dict['id']),
            parent_id=_dict.get('parent_id', _dict['id']),
        )

        # value int, datetime to str
        for k, v in new_dict.iteritems():
            if isinstance(v, (int, long)):
                v = str(v)
            new_dict[k] = v

        return new_dict

    # format data
    try:
        data = dict(
            host_comment=dict(
                format_d(problem_info),
                images=[dict(image=settings.SITE_URL + settings.MEDIA_URL + m[0],
                             small_image=settings.SITE_URL + settings.MEDIA_URL + m[1]) for m in
                        problem_info['materials']],
                target_time=problem_info['object_content'] or '',
                source=problem_info['object_name'] or ''
            ),
            list=[dict(
                format_d(l[0]),
                child_list=[dict(
                    format_d(cl),
                    reply_name=cl['answer_nick_name'] or ''
                ) for cl in l[1]]
            ) for l in answer_list]
        )
    except Exception as e:
        log.warn('error format_data, %s' % str(e))
        return {'success': False, 'msg': u'获取问题详情失败'}

    return {'success': True, 'data': data}


def get_project_detail_interface(backlog_id):
    """
    获取项目详情接口
    :param backlog_id:
    :return:
    """
    result = db.api.lps.teacher_warning.get_backlog_detail_by_id(backlog_id)
    if result.is_error():
        log.warn("db get_backlog_detail_by_id error, backlog_id %s", backlog_id)
        return dict(success=False, msg=u"服务器开小差了,稍后再试吧")
    backlog = result.result()
    if not backlog:
        log.warn("backlog has no data %s", backlog_id)
        return dict(success=False, msg=u"无提醒记录")

    project_id = backlog.get('obj_id', None)
    user_id = backlog.get('user_id', None)
    career_id = backlog.get('career_id', None)
    if not (career_id and project_id and user_id):
        log.warn("project_id or user_id is None %s", backlog_id)
        return dict(success=False, msg=u"项目id或用户id没有")

    # get project detail
    result = db.api.lps.teacher_warning.get_project_detail_by_project_id_and_user_id(project_id, user_id, career_id)
    if result.is_error():
        log.warn("db get_project_detail_by_project_id_and_user_id error, backlog_id %s", backlog_id)
        return dict(success=False, msg=u"服务器开小差了,稍后再试吧")
    project_detail = result.result()
    if not project_detail:
        log.warn("project_detail is null, backlog_id %s", backlog_id)
        return dict(success=False, msg=u"没有任务详情数据,请联系带班老师")

    try:
        project_detail['images'] = [{'image': settings.SITE_URL + settings.MEDIA_URL + i} for i in
                                    project_detail['images'].split(',')]
        project_detail.update(
            dict(
                name=backlog['user_name'],
                avatar=settings.SITE_URL + settings.MEDIA_URL + backlog['user_head'],
                user_type='2',
                create_time=backlog['create_date'].strftime('%Y/%m/%d %T')
            )
        )
        project_detail['project_id'] = str(project_detail['project_id'])
    except Exception as e:
        log.warn('format data error, %s' % str(e))
        return dict(success=False, msg=u"服务器开小差了,稍后再试吧")

    return dict(success=True, data=project_detail)


def get_meeting_detail_interface(backlog_id):
    """
    获取班会详情接口
    :param backlog_id:
    :return:
    """
    now = datetime.datetime.now()
    result = db.api.lps.teacher_warning.get_meeting_detail(backlog_id)
    if result.is_error():
        log.warn("db get_meeting_detail error, backlog_id %s", backlog_id)
        return dict(success=False, msg=u"服务器开小差了,稍后再试吧")
    meeting = result.result()

    def format_d(_dict):
        week_dict, day_dict = get_week_dict()
        status_dict = OnevoneMeeting.STATUS_DICT
        start_time = _dict['start_time']
        _dict['avatar'] = settings.SITE_URL + settings.MEDIA_URL + _dict['avatar']
        _dict['start_time'] = start_time.strftime('%R')
        _dict['end_time'] = _dict['end_time'].strftime('%R')
        _dict['create_time'] = _dict['create_time'].strftime('%Y/%m/%d %T')
        _dict.setdefault('weekday', "%s" % day_dict.get(start_time.strftime('%F'), start_time.strftime('%m月%d日')))
        _dict.update({'date': start_time.strftime('%F')})
        # 状态
        _dict['status'] = 4 if _dict['star'] else status_dict[_dict['status']]
        if now >= _dict['warn_one_date']:
            _dict.setdefault('priority', LEVEL_2)
        else:
            _dict.setdefault('priority', LEVEL_4)
        _content = _dict['content']
        _dict['content'] = re.sub('<img src="', '<img src="' + settings.SITE_URL, _content) if _content else ''
        del _dict['warn_one_date'], _dict['warn_two_date']

    try:
        format_d(meeting)

        # value int to str
        for k, v in meeting.iteritems():
            if isinstance(v, (int, long)):
                v = str(v)
            meeting[k] = v
    except Exception as e:
        log.warn('function format_d, %s' % str(e))
        return dict(success=False, msg=u"服务器开小差了,稍后再试吧")

    return dict(success=True, data=meeting)


def app_get_my_student_by_teacher_id_interface(teacher_id):
    """
    获取我的学生by老师
    :param teacher_id:
    :return:
    """
    data = []
    students = ()
    now = datetime.datetime.now()

    # 取基础数据
    _students = db.api.lps.student.app_get_my_student_by_teacher_id(teacher_id)
    if _students.is_error():
        log.warn('app_get_my_student_by_teacher_id is error, teacher_id %s' % teacher_id)
    else:
        students = _students.result()

    # 第一次循环，按专业分类
    data_dict = {}
    for s in students:
        major_name = s['name']
        data_dict.setdefault(major_name, [])
        data_dict[major_name].append(s)

    # 组织最终数据
    for k, v in data_dict.iteritems():
        class_id = 0
        _v = []
        for _s in v:
            user_id = _s['user_id']
            if not class_id:
                class_id = NORMAL_CLASS_DICT.get(_s['career_id'])
                iface = StageTaskInterface(class_id)
                sums_task = iface.count_all_tasks()
            iface.load_student_data(user_id)
            finish_task = iface.count_student_tasks_finished(user_id)
            current_task = iface.get_student_latest_task(user_id)
            task_rid, task_name = 0, ''
            if current_task:
                task_rid, task_name = current_task.task_rid, current_task.task_name
            _v.append(dict(
                student_id=str(user_id),
                avatar=settings.SITE_URL + settings.MEDIA_URL + _s['avatar_small_thumbnall'],
                name=_s['real_name'] or _s['nick_name'],
                graduation_day=str((_s['end_time'] - now).days),
                sums_task=str(sums_task),
                finish_task=str(finish_task),
                current_task=task_name,
                stage_task_id=task_rid,
                career_id=_s['career_id']
            ))
        data.append(dict(
            major_name=k,
            student_list=_v
        ))

    return data


#  ---------------- 新 老师app 1.1--------------------

def app_backlog_history_by_teacher_id_interface(teacher_id, page, order, types):
    """
    获取告警代办历史记录
    :param teacher_id:
    :param page: int
    :param order: int
    :param types: ()
    :return:
    """
    backlog_history = ()
    if order == '0':
        order_type = 'ASC'
    if order == '1':
        order_type = 'DESC'
    # 取基础数据
    result = db.api.lps.teacher_warning.get_backlog_history(teacher_id, types, order_type, page)
    if result.is_error():
        log.warn('app_get_my_student_by_teacher_id is error, teacher_id %s' % teacher_id)
    else:
        backlog_history = result.result()
    backlog_history_dict = OrderedDict()
    for backlog in backlog_history:
        try:
            meeting_time = None  # 班会时间
            if backlog['type'] == 5:
                start_time = backlog['warn_one_date']
                end_time = start_time + datetime.timedelta(minutes=30)
                meeting_time = start_time.strftime('%F %R') + '-' + end_time.strftime('%R')

            _done_date = backlog['done_date']
            # 时间处理
            now_day = datetime.datetime.now().strftime('%Y-%m-%d')
            day_key = _done_date.strftime('%Y-%m-%d')
            if now_day == day_key:
                day_key = '今天'
            backlog_history_dict.setdefault(day_key, {'title': day_key, 'sub_list': []})
            backlog_history_dict[day_key]['sub_list'].append(dict(
                name=backlog['user_name'],
                avatar=settings.SITE_URL + settings.MEDIA_URL + backlog['user_head'],
                content=backlog['content'],
                priority=str(backlog['done_status']),
                service_type=str(backlog['type']),
                backlog_id=str(backlog['id']),
                service_id=str(backlog['obj_id']),
                create_time=meeting_time or backlog['done_date'].strftime('%F %R')
            ))
        except Exception, e:
            log.warn('format data error %s' % str(e))
    return backlog_history_dict.values()
