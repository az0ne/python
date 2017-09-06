# -*- coding: utf-8 -*-

"""
@version: 2016/6/12
@author: Jackie
@contact: jackie@maiziedu.com
@file: views.py
@time: 2016/6/12 15:25
@note:  ??
"""
import interface
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.http import JsonResponse
from mz_common.models import ObjSEO
from mz_lps3_free.student.interface_questionnaire import student_free_questionnaire_is_done, \
    short_name_to_questionnaire_id

from db.api.lps import struct as api_lps_struct
from db.api.lps import task as api_task
from db.api.lps import usertask as api_user_task
from db.api.course import career_course_intro as api_ccourse_intro
from django.shortcuts import render, get_object_or_404, redirect
from mz_common.decorators import student_required
from mz_course.models import CareerCourse
from mz_lps.models import ClassStudents, Class
from mz_lps3.decorators import check_student_status
from mz_user.models import UserProfile
from mz_lps3_free.common.interface import Free488ClassInterface, FREE488_TEACHER, unlock_free_task


def syllabus_index(request, course_short_name):
    """
    大纲页面
    :param course_id:课程的short_name!!!!!
    :return:
    """
    show_guide = 'True'
    course = get_object_or_404(CareerCourse, short_name=course_short_name)
    if not course.enable_free_488:
        raise Http404
    if request.user.is_authenticated():
        if ClassStudents.objects.filter(
                user_id=request.user.id, student_class__career_course_id=course.id,
                status=ClassStudents.STATUS_NORMAL,
                student_class__class_type=Class.CLASS_TYPE_FREE_488).exists():
            show_guide = 'False'
    stages = api_lps_struct.get_course_syllabus(course.id).result()
    guide_task_id = course.guide_task_id
    for stage in stages:
        tasks = stage['tasks']
        for i in range(len(tasks))[::-1]:
            if tasks[i]['id'] == guide_task_id:
                tasks.pop(i)
    try:
        seo = ObjSEO.objects.get(obj_type='CAREERCOURSELINE', obj_id=course.id)
    except ObjSEO.DoesNotExist:
        pass

    return render(request, 'mz_lps3_free/student/syllabus_index.html', locals())


def appointment_index(request, course_short_name):
    """
    预约页面
    :param request:
    :param course_id:
    :return:
    """
    user = request.user
    ccourse = get_object_or_404(CareerCourse, short_name=course_short_name, enable_free_488=True)
    if user.is_authenticated() and user.is_student():
        try:
            cstudent = ClassStudents.objects.get(
                user_id=user.id, student_class__career_course_id=ccourse.id,
                status=ClassStudents.STATUS_NORMAL,
                student_class__class_type=Class.CLASS_TYPE_FREE_488)
            return redirect(
                reverse("lps3f:student:class_index", kwargs={'class_id': cstudent.student_class_id})
            )
        except ClassStudents.DoesNotExist:
            pass
        try:
            cstudent = ClassStudents.objects.get(
                user_id=user.id, student_class__career_course_id=ccourse.id,
                status=ClassStudents.STATUS_NORMAL,
                student_class__class_type=Class.CLASS_TYPE_NORMAL)
            if cstudent.student_class.lps_version == "3.0":
                return redirect(reverse("lps3:student_class", kwargs={'class_id': cstudent.student_class_id}))
            else:
                return redirect(reverse("lps2:lps2_learning_plan", kwargs={'careercourse_id': ccourse.id}))
        except ClassStudents.DoesNotExist:
            pass
    tmp = api_task.get_free488_task_id(ccourse.id)
    if tmp.is_error():
        raise Http404
    task_id, stagetask_id = tmp.result()
    # 原始任务的in系
    task_info = api_task.get_task_info(task_id).result()
    # 免费任务的相关描述
    free488_task_desc = api_task.get_free488_task_desc(task_id).result()
    # 免费试学班预约的信息
    free_class_info_list = interface.get_free_class_and_class_meeting_list(ccourse.id)
    # 免费试学班时默认显示的介绍老师
    if not free_class_info_list:
        user_id = FREE488_TEACHER.get(course_short_name)
        if user_id:
            teacher = get_object_or_404(UserProfile, id=user_id)
    return render(request, 'mz_lps3_free/student/appointment_index.html', locals())


@student_required
@check_student_status
def class_index(request, class_id):
    """
    学习面板
    :param request:
    :param class_id:
    :return:
    """
    user_id = request.user.id
    cclass = request.cclass
    career_course_id = cclass.career_course_id
    if not cclass.is_free488_class():
        raise Http404
    course_short_name = cclass.career_course.short_name
    tmp = api_task.get_free488_task_id(career_course_id)
    if tmp.is_error():
        raise Http404
    task_id, stagetask_id = tmp.result()
    # 解锁第一个免费任务,写入usertask
    unlock_free_task(request.user.id, class_id, stagetask_id)
    # 原始任务的in系
    task_info = api_task.get_task_info(task_id).result()
    # 免费任务的相关描述
    free488_task_desc = api_task.get_free488_task_desc(task_id).result()
    # 带班老师
    teacher = cclass.teacher
    # 试学班的模型封装
    free488_class = Free488ClassInterface(class_id, student_name=request.user.real_name or request.user.nick_name)
    # 基础资料
    articles_materials = api_task.get_task_rel_articles(task_id, api_task.TASK_ARTICLE_TYPE_BASE).result()
    # 课后展示文章
    articles_advanced = api_task.get_task_rel_articles(task_id, api_task.TASK_ARTICLE_TYPE_AFTER_TASK).result()
    # 用户任务详情
    user_task_detail = api_user_task.get_user_task_detail(stagetask_id, class_id, user_id).result()
    # 用户任务信息
    user_task_info = api_user_task.get_user_task_info(stagetask_id, class_id, user_id).result()
    # 优秀作品
    task_good_works = api_task.get_task_excellent_works(task_id).result()

    # 免费试学班满意度问卷short_name为try_satis
    questionnaire_id = short_name_to_questionnaire_id('try_satis')
    has_questionnaire = student_free_questionnaire_is_done(class_id, user_id, questionnaire_id)

    if free488_class.is_finished():  # 班会结束后才会需要以下内容
        # 课程大纲
        course_syllabus = api_lps_struct.get_course_syllabus(career_course_id).result()
        # 课程广告图
        course_intro = api_ccourse_intro.get_career_intro(career_course_id).result()
        if course_intro:
            course_intro['students'] = course_intro['students'][:3]

    free488_class_stage = free488_class.get_stage()
    if free488_class_stage == 2 and user_task_info['status'] in ('DONE', 'PASS'):
        free488_class_stage = 3
    return render(request, 'mz_lps3_free/student/learning_index.html', locals())


def study_video(request):
    return render(request, 'mz_lps3_free/student/study_video.html', locals())


def ajax_appointment_free_class(request):
    """
    异步预约免费试学班
    :param request:
    :return:
    """
    if not request.user.is_authenticated() or not request.user.is_student():
        return JsonResponse({'status': False, "message": u"只有学生才能预约哦^_^"})
    class_id = request.POST.get('class_id', '')
    if class_id == '':
        return JsonResponse({'status': False, "message": u"班级ID不能为空"})
    try:
        _class = Class.objects.xall().get(id=class_id, class_type=Class.CLASS_TYPE_FREE_488, lps_version='3.0')
    except Class.DoesNotExist:
        return JsonResponse({'status': False, "message": u"班级不存在或者不是试学班"})

    if ClassStudents.objects.filter(
            user_id=request.user.id, student_class__career_course_id=_class.career_course_id,
            status=ClassStudents.STATUS_NORMAL,
            student_class__class_type__in=[Class.CLASS_TYPE_NORMAL, Class.CLASS_TYPE_FREE_488],
            ).exists():
        return JsonResponse({'status': False, "message": u"你已经加入过该课程下的班级"})

    try:
        ClassStudents.objects.create(student_class=_class, user=request.user)
        interface.send_sms_ordered_free_class_success(_class, request.user.mobile)
    except Exception, e:
        return JsonResponse({'status': False, "message": u"创建班级失败,请稍后再试或者联系客服哟^_^"})
    return JsonResponse({'status': True, "message": ""})
