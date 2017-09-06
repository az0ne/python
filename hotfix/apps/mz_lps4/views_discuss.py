# -*- coding: utf-8 -*-

from context import get_lps4_context
from django.http.response import HttpResponse
import db.api.common.new_discuss
from mz_common.function_discuss import get_one_question
from django.http.response import Http404

from mz_lps4.class_dict import CAREER_ID_TO_SHORT_NAME
from mz_lps4.interface_lps import lps4_public, authenticate_user_info_interface
from utils.logger import logger
from django.shortcuts import render
from mz_common.decorators import student_required


@student_required
def view_my_discuss(request, career_id):
    """
    :param request:
    :return:
    """
    user_id = request.user.id
    problem_id = request.GET.get('p_id')
    px = lps4_public(career_id)
    authenticate_user_data = authenticate_user_info_interface(user_id, career_id)
    lps_count = authenticate_user_data.get('lps_count', {}),
    if problem_id:
        result = db.api.common.new_discuss.get_problem_by_id(problem_id, user_id)
        if result.is_error():
            logger.warn('get_problem_by_id not data,problem_id is %s' % problem_id)
            raise Http404
        problem_info = result.result()
        try:
            answer_list = get_one_question(user_id, problem_id)
        except Exception, e:
            logger.warn('function get_one_questions is error, user: %s, discuss_id:%s  %s' % (user_id, problem_id, e))
            answer_list = []
        return render(request, 'mz_lps4/stu_ques_ans_detail.html',
                      {'problem_info': problem_info, 'answer_list': answer_list,
                       'career_id': career_id, 'px': px, 'lps_count': lps_count},
                      context_instance=get_lps4_context(request, career_id))
    else:
        # 我的提问（全部）
        my_problem_list = []
        my_problem_result = db.api.common.new_discuss.get_my_problem_list_by_user_id(user_id)
        if not my_problem_result.is_error():
            my_problem_list = my_problem_result.result()
        # 我的回复（全部）
        my_answer_list = []
        my_answer_result = db.api.common.new_discuss.get_my_answer_list_by_user_id(user_id)
        if not my_answer_result.is_error():
            my_answer_list = my_answer_result.result()
        return render(request, 'mz_lps4/stu_ques_ans.html',
                      {'my_problem_list': my_problem_list, 'my_answer_list': my_answer_list,
                       'career_id': career_id, 'px': px, 'lps_count': lps_count},
                      context_instance=get_lps4_context(request, career_id))


@student_required
def ajax_get_my_problem(request):
    user_id = request.user.id
    try:
        status = request.GET.get('status')
        end_id = int(request.GET.get('end_id', 0))
    except Exception, e:
        logger.warn(e)
        end_id = 0

    result = db.api.common.new_discuss.get_my_problem_list_by_user_id(user_id, status=status, end_id=end_id)
    my_problem_list = result.result()
    return render(request, 'mz_lps4/discuss/ajax_div_discuss.html', {'my_discuss_list': my_problem_list})


@student_required
def ajax_get_my_answer(request):
    user_id = request.user.id
    try:
        status = request.GET.get('status')
        end_id = int(request.GET.get('end_id', 0))
    except Exception, e:
        logger.warn(e)
        end_id = 0

    result = db.api.common.new_discuss.get_my_answer_list_by_user_id(user_id, status=status, end_id=end_id)
    my_answer_list = result.result()
    return render(request, 'mz_lps4/discuss/ajax_div_discuss.html', {'my_discuss_list': my_answer_list})


def ajax_get_answer_by_problem_id(request, problem_id):
    """
    获取回复根据问题ID
    :param request:
    :param problem_id:
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
        logger.warn('function get_one_questions is error, user: %s, discuss_id:%s  %s' % (user_id, problem_id, e))
        answer_list = {}, []
    if not answer_list:
        return HttpResponse('')
    return render(request, 'mz_lps4/discuss/ajax_div_discuss_detail.html', {'answer_list': answer_list})