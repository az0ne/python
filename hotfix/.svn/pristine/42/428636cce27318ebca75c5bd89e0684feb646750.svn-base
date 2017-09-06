# -*- coding: utf-8 -*-
"""
@version: 2016/5/17 0017
@author: zhangyunrui
@contact: david.zhang@maiziedu.com
@file: views.py
@time: 2016/5/17 0017 10:48
@note:  老师端自己可见VIEWS
"""
import json
import datetime

import db.api.common.new_discuss
import db.api.onevone.meeting
import db.api.teacher.teacher
import db.api.lps.student
import db.api.lps.teacher_warning

from django.core.urlresolvers import reverse

from core.common.utils.serializers import get_week_dict
from mz_common.functions import paginater, safe_int
from django.http.response import Http404, HttpResponse

from mz_lps4.class_dict import NORMAL_CLASS_DICT
from mz_lps4.interface import cmp_type, LPS4StudentsInterface, cmp_count, update_join_url
from utils.logger import logger as log
from utils.tool import get_param_by_request, strip_tags
from django.shortcuts import render
from mz_common.decorators import teacher_required
from mz_course.models import Course
from mz_usercenter.base.context import get_usercenter_context
from mz_usercenter.teacher.interface import TeacherOverview, show_onevone_meeting, serialize_onevone_meeting
from mz_usercenter.teacher.html_renders import get_teacher_intro_html
from mz_common.function_discuss import get_one_question
from core.common.http.response import success_json, failed_json
from mz_lps4.interface_teacher_warning import update_teacher_backlog_is_done


@teacher_required
def view_index(request):
    """
    老师个人主页
    :param request:
    :return:
    课程名name, 课程图片image, 章节数lesson_set.count, 学习人数student_count
    """
    user_id = request.user.id
    courses = Course.objects.filter(teacher=user_id)
    teacher_intro_html = get_teacher_intro_html(user_id)
    return render(request, 'mz_usercenter/teacher/homepage.html', locals(),
                  context_instance=get_usercenter_context(request))


@teacher_required
def view_processing_classes(request):
    """
    进行中班级
    :param request:
    :return:
    """
    user_id = request.user.id
    class_list = TeacherOverview.processing_classes(user_id)

    return render(request, 'mz_usercenter/teacher/class_ongoing.html', locals(),
                  context_instance=get_usercenter_context(request))


@teacher_required
def view_graduated_classes(request):
    """
    已毕业班级
    :param request:
    :return:
    """
    user_id = request.user.id
    class_list = TeacherOverview.graduated_classes(user_id)

    return render(request, 'mz_usercenter/teacher/class_graduate.html', locals(),
                  context_instance=get_usercenter_context(request))


@teacher_required
def view_lps2_classes(request):
    """
    LPS2.0班级
    :param request:
    :return:
    """
    user_id = request.user.id
    class_list = TeacherOverview.lps2_classes(user_id)

    return render(request, 'mz_usercenter/teacher/class_lps2.html', locals(),
                  context_instance=get_usercenter_context(request))


@teacher_required
def view_student_discuss(request):
    """
    学生问答
    :param request:
    :return:
    """
    user_id = request.user.id
    problem_id = request.GET.get('p_id')
    if problem_id:
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
        return render(request, 'mz_usercenter/teacher/student_discuss_detail.html',
                      {'problem_info': problem_info, 'answer_list': answer_list},
                      context_instance=get_usercenter_context(request))
    else:
        # 进行中的班级
        result = db.api.common.new_discuss.get_student_discuss_list_by_teacher(user_id, class_type=0)
        if result.is_error():
            class_answer_list = []
        class_answer_list = result.result()

        # 免费试学班
        result = db.api.common.new_discuss.get_student_discuss_list_by_teacher(user_id, class_type=1)
        if result.is_error():
            free_class_answer_list = []
        free_class_answer_list = result.result()

        # 毕业班级
        result = db.api.common.new_discuss.get_student_discuss_list_by_teacher(user_id, class_type=2)
        if result.is_error():
            over_class_answer_list = []
        over_class_answer_list = result.result()

        # 普通用户
        result = db.api.common.new_discuss.get_student_discuss_list_by_teacher(user_id, class_type=3)
        if result.is_error():
            not_class_answer_list = []
        not_class_answer_list = result.result()

        return render(request, 'mz_usercenter/teacher/student_discuss.html',
                      {'class_answer_list': class_answer_list, 'free_class_answer_list': free_class_answer_list,
                       'over_class_answer_list': over_class_answer_list,
                       'not_class_answer_list': not_class_answer_list},
                      context_instance=get_usercenter_context(request))


@teacher_required
def onevone_meeting(request):
    """
    老师端 1v1直播列表 往期列表 详情
    :param request:
    :return:
    """
    user = request.user
    user_id = user.id
    back_url = request.environ.get('HTTP_REFERER', reverse('home:teacher:onevone_meeting'))
    if request.method == 'GET':
        # 展示详情
        meeting_id = get_param_by_request(request.GET, 'id', 0, int)
        if meeting_id:
            _onevone_meeting = show_onevone_meeting(meeting_id)

            # update is_new in backlog
            result = db.api.lps.teacher_warning. \
                update_backlog_status_by_obj_id('is_new', meeting_id, 5)  # 5 is meeting
            if result.is_error():
                log.warn('update_backlog_status_by_obj_id error, meeting_id %s', meeting_id)
                
            if not onevone_meeting:
                raise Http404
            return render(request, 'mz_usercenter/teacher/oneVone_line_detail.html',
                          dict(onevone_meeting=_onevone_meeting, back_url=back_url),
                          context_instance=get_usercenter_context(request))

        # 当前没有完成的1v1直播
        is_current = True
        url = reverse('home:teacher:onevone_meeting') + '?'

        # 展示列表
        page_index = safe_int(request.GET.get('page_index', 1), 1)
        # 已完成的1v1直播
        if request.GET.get('old'):
            is_current = False
            url += 'old=true&'
        page_size = 10
        page_aroud = 2
        result = db.api.onevone.meeting.get_onevone_meeting_count_by_teacher_id(user_id, is_current)
        if result.is_error():
            log.warn('get_onevone_meeting_count_by_teacher_id is error teacher_id:%s' % user_id)
        rows_count = result.result() or 0
        result = db.api.onevone.meeting.show_onevone_meeting_list_by_teacher_id(user_id, page_index, page_size,
                                                                                is_current)
        if result.is_error():
            log.warn('show_onevone_meeting_list_by_teacher_id is error teacher_id:%s' % user_id)
        onevone_meeting_list = result.result()
        if not is_current:
            onevone_meeting_list = list(onevone_meeting_list)
            onevone_meeting_list.reverse()
        onevone_meeting_dict = {}

        week_dict, day_dict = get_week_dict()
        for m in onevone_meeting_list:
            _start_time = m['start_time']
            m.update({'content': strip_tags(m.get('question', ''))})
            day_key = _start_time.strftime('%F')
            week_key = int(_start_time.strftime('%w'))
            weekday = week_dict[week_key]
            onevone_meeting_dict.setdefault(day_key,
                                            {'start_day': day_dict.get(day_key, _start_time.strftime('%m月%d号')),
                                             'weekday': weekday, 'data': [], 'start_time': day_key})
            # 更新meeting的join_url
            try:
                is_video = m.get('status', 'CREATE') == 'ENDED'
                join_url = update_join_url(m, is_teacher=True, is_video=is_video)
            except Exception as e:
                log.warn(str(e))
            else:
                m.update({'join_url': join_url})
            onevone_meeting_dict[day_key]['data'].append(m)
        onevone_meeting_list = sorted(onevone_meeting_dict.values(),
                                      key=lambda x: x['start_time'], reverse=not is_current)
        page_count_list, page_index, _, _ = paginater(page_index, page_size, rows_count, page_aroud)
        return render(request, 'mz_usercenter/teacher/oneVone_line.html',
                      dict(onevone_meeting_list=onevone_meeting_list,
                           page_count_list=page_count_list,
                           page_index=page_index,
                           back_url=back_url,
                           url=url,
                           is_current=is_current),
                      context_instance=get_usercenter_context(request))


@teacher_required
def ajax_onevone_add_list(request):
    """
    1v1班会列表
    :param request:
    :return:
    """
    data = {}
    user_id = request.user.id
    date_list = dict(request.POST).get('datelist[]', [])
    time_list = dict(request.POST).get('timelist[]', [])
    if user_id and date_list and time_list:
        data = serialize_onevone_meeting(user_id, time_list, date_list)
    return HttpResponse(success_json(data), content_type='application/json')


@teacher_required
def ajax_del_onevone(request):
    teacher_id = request.user.id
    _meeting_list = request.POST.get('meeting_list', '')
    meeting_list = json.loads(_meeting_list)

    db.api.onevone.meeting.del_onevone_meeting(teacher_id, meeting_list)

    return HttpResponse(success_json(), content_type='application/json')


@teacher_required
def ajax_insert_onevone_attendance(request):
    teacher_id = request.user.id
    meeting_id = get_param_by_request(request.POST, 'meeting_id', 0, int)
    if request.user.is_teacher():
        role_type = 1
    if request.user.is_student():
        role_type = 0
    if meeting_id:
        result = db.api.onevone.meeting.get_onevone_meeting_by_id(meeting_id)
        if result.is_error():
            log.warn('get_onevone_meeting_by_id is error meeting_id:%s user_id:%s' % (meeting_id, teacher_id))
            return failed_json('')
        onevone_meeting = result.result()
        # 开始前60分钟的进入班会的 才记录为完成老师待办
        if datetime.datetime.now() + datetime.timedelta(minutes=60) > onevone_meeting['start_time']:
            update_teacher_backlog_is_done(meeting_id, None, onevone_meeting['teacher_id'],
                                           onevone_meeting['user_id'], 5)
        # 记录所有的老师进入班会的时间
        result = db.api.onevone.meeting.create_onevone_meeting_attendance(meeting_id, teacher_id, role_type)
        if result.is_error():
            log.warn(
                'create_onevone_meeting_attendance is error meeting_id:%s user_id:%s' % (meeting_id, teacher_id))
            return failed_json('')

    return success_json()


@teacher_required
def onevone_service(request):
    s_order = request.GET.get('s_order', 'guarantee')
    teacher_id = request.user.id
    careers = db.api.teacher.teacher.get_careers_by_teacher(teacher_id)
    if careers.is_error():
        log.warn('get_careers_by_teacher failed. teacher_id: {0}'.format(teacher_id))
        careers = []
    else:
        careers = careers.result()

    for career in careers:
        class_id = NORMAL_CLASS_DICT.get(career['id'])
        if not class_id:
            break
        csi = LPS4StudentsInterface(teacher_id, career['id'], class_id)
        career['data'] = csi.data
        if s_order == 'guarantee':
            career['data'].sort(cmp=cmp_type)
        else:
            career['data'].sort(key=lambda x: x['type'])
        career['data'].sort(cmp=cmp_count)

        career['stages'] = csi.iface.get_stages()

        career['s_order'] = s_order

    return render(request, 'mz_usercenter/teacher/oneVone_service.html', dict(careers=careers),
                  context_instance=get_usercenter_context(request))


@teacher_required
def ajax_student_discuss(request, class_type):
    """
    学生问答
    :param request:
    :return:
    """
    user_id = request.user.id
    try:
        class_type = int(class_type)
        status = request.GET.get('status')
        end_id = int(request.GET.get('end_id', 0))
    except Exception, e:
        log.warn(e)
        end_id = 0
    result = db.api.common.new_discuss.get_student_discuss_list_by_teacher(user_id, class_type=class_type,
                                                                           status=status, end_id=end_id)
    if result.is_error():
        discuss_list = []
    discuss_list = result.result()

    return render(request, 'mz_usercenter/student/ajax_div_discuss.html',
                  {'my_discuss_list': discuss_list},
                  context_instance=get_usercenter_context(request))
