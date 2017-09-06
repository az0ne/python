# -*- coding: utf-8 -*-
"""
@version: 2016/5/17 0017
@author: lewis
@contact: lewis@maiziedu.com
@file: views.py
@time: 2016/5/17 0017 10:48
@note:  老师端第三方可见VIEWS
"""
import db.api.common.new_discuss
from django.shortcuts import render, get_object_or_404
from mz_course.models import Course
from mz_user.models import UserProfile
from ..base.seo import get_seo_info
from django.http.response import Http404
from utils.logger import logger
from mz_usercenter.teacher.html_renders import get_teacher_intro_html
from mz_common.function_discuss import get_one_question


def public_homepage(request, user_id):
    """
    教师 公开的 个人主页
    :param request:
    :param user_id: 被查看用户id(int)
    :return:
    """
    user_id = int(user_id)
    head_user = get_object_or_404(UserProfile, id=user_id)
    courses = Course.objects.filter(teacher=user_id)
    seo = get_seo_info(head_user)
    teacher_intro_html = get_teacher_intro_html(user_id)
    return render(request, 'mz_usercenter/teacher/public_homepage.html', locals())


def public_answer(request, user_id):
    """
    优质解答
    :param request:
    :return:
    """
    cur_user_id = request.user.id
    user_id = int(user_id)
    head_user = get_object_or_404(UserProfile, id=user_id)
    problem_id = request.GET.get('p_id')
    if problem_id:
        result = db.api.common.new_discuss.get_problem_by_id(problem_id, cur_user_id)
        if result.is_error():
            logger.warn('get_problem_by_id not data,problem_id is %s' % problem_id)
            raise Http404
        problem_info = result.result()
        try:
            answer_list = get_one_question(user_id, problem_id)
        except Exception, e:
            logger.warn('function get_one_questions is error, user: %s, discuss_id:%s  %s' % (user_id, problem_id, e))
            answer_list = []
        return render(request, 'mz_usercenter/teacher/public_teacher_answer_detail.html',
                      {'problem_info': problem_info, 'answer_list': answer_list,
                       'head_user': head_user, 'user_id': user_id})
    else:
        answer_result = db.api.common.new_discuss.get_ta_answer_list_by_user_id(user_id, cur_user_id)
        answer_list = answer_result.result()

        return render(request, 'mz_usercenter/teacher/public_teacher_answer.html',
                      {'answer_list': answer_list, 'head_user':head_user, 'user_id': user_id})
