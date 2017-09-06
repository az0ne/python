# -*- coding: utf-8 -*-
"""
@version: 2016/5/17 0017
@author: zhangyunrui
@contact: david.zhang@maiziedu.com
@file: views.py
@time: 2016/5/17 0017 10:48
@note:  学生端学习相关个人可见VIEWS
"""
from django.shortcuts import render
from mz_common.decorators import student_required
from mz_usercenter.base.context import get_usercenter_context
from mz_usercenter.student.interface_course import StudentOverview
from mz_usercenter.student.interface_record import first_signup_recommend


@student_required
def view_index(request):
    """
    第一次进入时,根据角色判断进入的暂时主页,会向真正指定的主页跳转
    :param request:
    :return:
    """
    return view_mycourse(request)


@student_required
def view_mycourse(request):
    """
    已报名课程
    :param request:
    :return:
    """
    student_id = request.user.id
    lps4_cstudent_list, cstudent_list = StudentOverview.normal_classes(student_id)

    # 新注册用户推荐课程弹窗
    recommend_careers = first_signup_recommend(request.user)

    return render(request, 'mz_usercenter/student/my_course.html', locals(),
                  context_instance=get_usercenter_context(request))


@student_required
def view_expcourse(request):
    """
    体验课程
    :param request:
    :return:
    """
    student_id = request.user.id
    cstudent_dict = StudentOverview.experience_classes(student_id)

    return render(request, 'mz_usercenter/student/exp_course.html', locals(),
                  context_instance=get_usercenter_context(request))


@student_required
def view_old_course(request):
    """
    LPS2.0企业直通班
    :param request:
    :return:
    """
    student_id = request.user.id
    cstudent_list = StudentOverview.old_classes(student_id)

    return render(request, 'mz_usercenter/student/my_course_2.html', locals(),
                  context_instance=get_usercenter_context(request))
