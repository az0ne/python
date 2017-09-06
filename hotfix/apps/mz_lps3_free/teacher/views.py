# -*- coding: utf-8 -*-
"""
@version: 2016/6/12
@author: Jackie
@contact: jackie@maiziedu.com
@file: views.py
@time: 2016/6/12 15:26
@note:  ??
"""
import datetime
import interface
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from mz_lps3.functions_gt import update_attendance_info
from mz_lps3.models import ClassMeeting
from mz_lps3_free.common.interface import Free488ClassInterface
from utils.logger import logger as log
import db.api

from mz_common.decorators import teacher_required
from django.core.urlresolvers import reverse
from mz_usercenter.base.context import get_usercenter_context
from django.http import JsonResponse
from mz_common.functions import paginater, safe_int


@teacher_required
def view_free_classes(request):
    """
    展示当前用户免费试学班的信息
    :param request:
    :return:
    """
    user = request.user
    if request.method == 'GET':
        page_index = safe_int(request.GET.get('page_index', 1), 1)
        page_size = 4
        page_aroud = 2
        rows_count = interface.get_count_free_class(user)
        free_class_dict = interface.get_free_classes_by_teacher(user, page_index, page_size)
        page_count_list, page_index, start_index, end_index = paginater(page_index, page_size, rows_count, page_aroud)
        career_course_list = interface.get_career_course_list()
        url = reverse('home:teacher:free_classes')+'?'
        return render(request, 'mz_lps3_free/teacher/trycourse.html', locals(),
                      context_instance=get_usercenter_context(request))
    # 创建班会
    if request.method == 'POST':
        career_course_id = request.POST.get('career_course', '')
        first_date = request.POST.get('first_date', '').strip()
        first_time = request.POST.get('first_time', '').strip()
        answer_date = request.POST.get('answer_date', '').strip()
        answer_time = request.POST.get('answer_time', '').strip()
        if career_course_id == '':
            return JsonResponse({'status': False, "message": u"专业不能为空"})
        if first_date == '':
            return JsonResponse({'status': False, "message": u"首次班会日期不能为空"})
        if first_time == '':
            return JsonResponse({'status': False, "message": u"首次班会时间不能为空"})
        if answer_date == '':
            return JsonResponse({'status': False, "message": u"答疑班会日期不能为空"})
        if answer_time == '':
            return JsonResponse({'status': False, "message": u"答疑班会时间不能为空"})
        try:
            first_datetime = datetime.datetime.strptime(first_date + ' ' + first_time, '%Y/%m/%d %H:%M')
        except Exception, e:
            # print e
            return JsonResponse({'status': False, "message": u"首次班会时间格式不正确"})

        try:
            answer_datetime = datetime.datetime.strptime(answer_date + ' ' + answer_time, '%Y/%m/%d %H:%M')
        except Exception, e:
            # print e
            return JsonResponse({'status': False, "message": u"答疑班会时间格式不正确"})

        try:
            result, msg = interface.is_free_class(career_course_id, user.id, first_date, answer_date)
        except Exception, e:
            return JsonResponse({'status': False, "message": str(e)})
        if result:
            return JsonResponse(dict(status=False, message=u'同一时间点已有试学班，请重新选择日期或时间'))
        try:
            status, msg = interface.create_free_class(career_course_id, first_datetime, answer_datetime, user.id)
        except Exception, e:
            # print e
            return JsonResponse({'status': False, "message": u"创建试学班级失败，请稍后再试"})
        return JsonResponse(dict(status=status, message=msg))
    return JsonResponse(dict(status=False, message='method is error'))


@teacher_required
def ajax_check_free_class(request):
    """
    检查是否能够创建免费试学班级
    :param request:
    :return:
    """
    user_id = request.user.id
    career_course_id = request.POST.get('career_course', '')
    first_date = request.POST.get('first_date', '').strip()
    answer_date = request.POST.get('answer_date', '').strip()
    if career_course_id == '':
        return JsonResponse({'status': False, "message": u"专业不能为空"})
    if first_date == '':
        return JsonResponse({'status': False, "message": u"首次班会日期不能为空"})
    if answer_date == '':
        return JsonResponse({'status': False, "message": u"答疑班会日期不能为空"})

    try:
        result, msg = interface.is_free_class(career_course_id, user_id, first_date, answer_date)
    except Exception, e:
        return JsonResponse({'status': False, "message": str(e)})
    if result:
        return JsonResponse(dict(status=False, message=u'同一时间点已有试学班，请重新选择日期或时间'))
    return JsonResponse(dict(status=True, message=u'可以创建免费试学班'))


@teacher_required
def class_index(request, class_id):
    try:
        class_id = int(class_id)
    except ValueError:
        log.warn('class_id is not a int')
        raise Http404

    class_rel = db.api.get_free_teacher_class(class_id)
    if class_rel.is_error():
        log.warn('get_free_teacher_class is error')
        raise Http404
    class_rel = class_rel.result()
    if class_rel:
        class_rel = class_rel[0]
        stage_task_id = class_rel.get('stage_task_id', 0)
    else:
        log.warn('get_free_teacher_class returns none')
        raise Http404

    student_rel = db.api.get_free_class_student(class_id, stage_task_id)
    if student_rel.is_error():
        log.warn('get_free_class_student is error')
        raise Http404
    student_rel = student_rel.result()

    is_ongoing = Free488ClassInterface(class_id).is_ongoing()

    return render(request, 'mz_lps3_free/teacher/trymanage.html', locals())


@teacher_required
def teacher_task(request, class_id, student_id, stagetask_id):
    try:
        class_id = int(class_id)
        student_id = int(student_id)
        stagetask_id = int(stagetask_id)
    except ValueError:
        log.warn('class_id/student_id/stagetask_id is not a int')
        raise Http404

    rel = db.api.get_user_task_detail(stagetask_id, class_id, student_id)
    if rel.is_error():
        log.warn('get_user_task_detail is error')
        raise Http404
    rel = rel.result()
    if rel:
        rel = rel[0]

    return render(request, 'mz_lps3_free/teacher/div_student_stage.html', locals())


@teacher_required
def flush_meeting(request, class_id, class_meeting_id):
    try:
        class_id = int(class_id)
        class_meeting_id = int(class_meeting_id)
    except ValueError:
        log.warn('class_id/class_meeting_id is not a int')
        raise Http404

    try:
        class_meeting = ClassMeeting.objects.get(id=class_meeting_id)
    except:
        log.warn('get ClassMeeting object error')
        raise Http404

    update_attendance_info(class_meeting)

    return HttpResponseRedirect(reverse('lps3f:teacher:class_index', kwargs={'class_id': class_id}))
