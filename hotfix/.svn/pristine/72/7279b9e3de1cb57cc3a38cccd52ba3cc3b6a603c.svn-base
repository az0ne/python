# -*- coding: utf-8 -*-

"""
@version: 2016/5/16
@author: Jackie
@contact: jackie@maiziedu.com
@file: views_home.py
@time: 2016/5/16 17:57
@note:  ??
"""

import mz_usercenter.student.views_public
import mz_usercenter.teacher.views_public
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.http.response import Http404
from django.shortcuts import get_object_or_404, render
from mz_user.models import UserProfile
from mz_usercenter.student.views_course import view_index as student_view_index
from mz_usercenter.teacher.views import view_index as teacher_view_index
from mz_usercenter.eduadmin.views import view_index as eduadmin_view_index
from mz_common.function_discuss import answer_post_api, get_one_question, log
from core.common.http.response import success_json, failed_json
from django.http.response import HttpResponse


@login_required(login_url='/')
def home_index(request):
    """
    登陆后个人中心入口,由此判断角色并跳转
    :return:跳转
    """
    user = request.user
    if user.is_edu_admin():
        return eduadmin_view_index(request)
    elif user.is_teacher():
        return teacher_view_index(request)
    elif user.is_student():
        return student_view_index(request)
    raise Http404


def u_index(request, user_id):
    """
    查看他人的信息,无需校验是否自己,,逻辑独立
    :return:跳转
    """
    user = get_object_or_404(UserProfile, id=user_id)
    if user.is_edu_admin():  # 教务
        from mz_usercenter.eduadmin.views_public import public_homepage as ea_public_homepage

        return ea_public_homepage(request, user_id)
    elif user.is_teacher():  # 教师
        from mz_usercenter.teacher.views_public import public_homepage as teacher_public_homepage

        return teacher_public_homepage(request, user_id)
    elif user.is_student():  # 学生
        from mz_usercenter.student.views_public import public_mycourse

        return public_mycourse(request, user_id)

    else:
        raise Http404


def u_discuss(request, user_id):
    """
    查看他人的问答,无需校验是否自己,,逻辑独立
    :return:跳转
    """
    user = get_object_or_404(UserProfile, id=user_id)
    if user.is_teacher():  # 教师
        return mz_usercenter.teacher.views_public.public_answer(request, user_id)

    elif user.is_student():  # 学生
        return mz_usercenter.student.views_public.public_discuss(request, user_id)

    else:
        raise Http404


def ajax_get_answer_by_problem_id(request, problem_id):
    """
    获取回复根据问题ID
    :param request:
    :param discuss_id:
    :param last_id:
    :return:
    """
    if request.user.is_authenticated():
        user_id = request.user.id
    else:
        user_id = 0
    end_id = request.GET.get('end_id', 0)
    try:
        answer_list = get_one_question(user_id, problem_id, end_id)
    except Exception, e:
        log.warn('function get_one_questions is error, user: %s, discuss_id:%s  %s' % (user_id, problem_id, e))
        answer_list = {}, []
    if not answer_list:
        return HttpResponse('')
    return render(request, 'mz_usercenter/ajax_div_discuss_detail.html', {'answer_list': answer_list})

@require_POST
@login_required(login_url='/')
def ajax_discuss_post(request):
    """
    异步提交回复
    :param request
    :return:
    """
    user = request.user
    _post = request.POST

    user_id = user.id
    nick_name = user.nick_name
    head = user.avatar_small_thumbnall

    comment = _post['comment']
    parent_id = _post['parent_id']
    problem_id = _post['problem_id']
    answer_user_id = _post['answer_user_id']
    answer_nick_name = _post['answer_nick_name']

    flags, msg, data = answer_post_api(user, comment, parent_id, problem_id, answer_user_id,
                                       answer_nick_name)

    result_data = dict(
        user_id=user_id,
        user_url=reverse('u:index', args=[user_id]),
        nick_name=nick_name,
        head=settings.MEDIA_URL+head.name
    )
    result_data.update(data)

    if flags:
        return success_json(result_data)
    else:
        return failed_json(msg, result_data)
