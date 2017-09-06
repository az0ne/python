# -*- coding: utf-8 -*-
"""
@version: 2016/5/17 0017
@author: zhangyunrui
@contact: david.zhang@maiziedu.com
@file: views.py
@time: 2016/5/17 0017 10:48
@note:  学生端第三方可见VIEWS
"""
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from mz_user.models import UserProfile
from mz_usercenter.student.interface_course import StudentOverview
from ..base.seo import get_seo_info
import db.api.common.new_discuss
from utils.logger import logger
from mz_common.function_discuss import get_one_question


def public_mycourse(request, user_id):
    """
    公开的 个人课程
    :param request:
    :param user_id: 被查看用户id(int)
    :return:
    """
    user_id = int(user_id)
    head_user = get_object_or_404(UserProfile, id=user_id)
    lps4_cstudent_list, cstudent_list = StudentOverview.normal_classes(user_id)
    seo = get_seo_info(head_user)

    return render(request, 'mz_usercenter/student/public_my_course.html', locals())


def public_expcourse(request, user_id):
    """
    公开的 体验课程
    :param request:
    :param user_id: 被查看用户id(int)
    :return:
    """
    user_id = int(user_id)
    head_user = get_object_or_404(UserProfile, id=user_id)
    cstudent_dict = StudentOverview.experience_classes(user_id)

    return render(request, 'mz_usercenter/student/public_exp_course.html', locals())


def public_discuss(request, user_id):
    """
    TA的问答
    :param request:
    :return:
    """
    user_id = int(user_id)
    is_login = request.user.is_authenticated()
    cur_user_id = request.user.id
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
        return render(request, 'mz_usercenter/student/public_other_discuss_detail.html',
                      {'problem_info': problem_info, 'answer_list': answer_list,
                       'head_user': head_user, 'user_id': user_id})
    else:
        # TA的提问
        my_problem_result = db.api.common.new_discuss.get_ta_problem_list_by_user_id(user_id, cur_user_id)
        my_problem_list = my_problem_result.result()

        # TA的回复
        my_answer_result = db.api.common.new_discuss.get_ta_answer_list_by_user_id(user_id, cur_user_id)
        my_answer_list = my_answer_result.result()

        return render(request, 'mz_usercenter/student/public_other_discuss.html',
                      {'my_problem_list': my_problem_list, 'my_answer_list': my_answer_list,
                       'head_user': head_user, 'user_id': user_id})


def ajax_public_problem(request, user_id):
    cur_user_id = request.user.id
    try:
        end_id = int(request.GET.get('end_id', 0))
    except Exception, e:
        logger.warn(e)
        end_id = 0

    result = db.api.common.new_discuss.get_ta_problem_list_by_user_id(user_id, cur_user_id, end_id=end_id)
    my_problem_list = result.result()
    return render(request, 'mz_usercenter/student/ajax_div_discuss.html', {'my_discuss_list': my_problem_list})


def ajax_public_answer(request, user_id):
    cur_user_id = request.user.id
    try:
        end_id = int(request.GET.get('end_id', 0))
    except Exception, e:
        logger.warn(e)
        end_id = 0

    result = db.api.common.new_discuss.get_ta_answer_list_by_user_id(user_id, cur_user_id, end_id=end_id)
    my_answer_list = result.result()
    return render(request, 'mz_usercenter/student/ajax_div_discuss.html', {'my_discuss_list': my_answer_list})
