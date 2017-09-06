# -*- coding: utf8 -*-

import functools
import db.api

from django.http.response import HttpResponse, JsonResponse
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render

from utils import tool
from utils.logger import logger as log
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from mz_back.funtions import ExportTryLearnData


# 试学学生列表
@dec_login_required
@handle_http_response_exception(501)
def try_learn_list(request):
    action = tool.get_param_by_request(request.GET, 'action', default_val='show')
    export_type = tool.get_param_by_request(
        request.GET, 'export_type', default_val='current_page')
    mobile = tool.get_param_by_request(request.GET, 'mobile', _type=int)
    try_learn_name = tool.get_param_by_request(request.GET, 'try_learn_name')
    try_learn_time = tool.get_param_by_request(request.GET, 'try_learn_time')

    page_index = tool.safe_positive_int(
        request.GET.get('page_index'), 1)
    page_size = tool.safe_positive_int(
        request.GET.get('page_size'), settings.PAGE_SIZE)

    if action == 'delete':
        user_role = request.session['role']
        if not user_role or user_role.get('name') != u'管理员':
            return JsonResponse(dict(success=False, message=u'删除请联系管理员！'))

        class_id = tool.get_param_by_request(request.GET, 'class_id')
        student_id = tool.get_param_by_request(request.GET, 'student_id')
        result = db.api.del_try_learn_record(class_id, student_id)
        if result.is_error():
            log.warn('del student from class failed. '
                     'class_id: {0}, student_id: {1}'.format(class_id, student_id))
            result = False
        else:
            result = result.result()
        return JsonResponse(dict(success=result))

    if export_type == 'all' and action == 'export':
        learn_data = db.api.get_try_learn_list(
            page_index, page_size, mobile=mobile,
            try_learn_name=try_learn_name,
            try_learn_time=try_learn_time, is_all=True)
    else:
        learn_data = db.api.get_try_learn_list(
            page_index, page_size, mobile=mobile,
            try_learn_name=try_learn_name,
            try_learn_time=try_learn_time)
    if learn_data.is_error():
        log.warn('get try learn list failed. '
                 'mobile: {}'.format(mobile))
        learn_data = dict(try_learn_list=[], page=dict())
    else:
        learn_data = learn_data.result()

    learn_data.update(s_mobile=mobile,
                      s_try_learn_name=try_learn_name,
                      s_try_learn_time=try_learn_time)
    if action == 'export':
        bio = ExportTryLearnData(learn_data['try_learn_list']).export_bio()
        response = HttpResponse(bio.getvalue(), content_type='application/vnd.ms-excel')

        fn = '试学列表'
        condition = [mobile, try_learn_name, try_learn_time]
        try:
            fn += '_' + '_'.join([str(d) for d in condition if d])
        except:
            log.warn('create excel filename failed. '
                     'conditions:{}'.format(condition))
        if export_type != 'all':
            fn += '_第{}页'.format(page_index)
        fn += '.xls'

        response['Content-Disposition'] = 'attachment; filename=' + fn
        response['Content-Length'] = len(bio.getvalue())

        return response
    else:
        return render(request, 'mz_back/try_learn_list.html', learn_data)


@dec_login_required
@handle_http_response_exception(501)
def try_learn_detail(request):
    _render = functools.partial(
        render, request, 'mz_back/try_learn_detail.html')

    class_id = tool.get_param_by_request(request.GET, 'class_id', _type=int)
    student_id = tool.get_param_by_request(request.GET, 'student_id', _type=int)
    show = tool.get_param_by_request(request.GET, 'show')
    back_url = tool.get_back_url(request, reverse('mz_back:try_learn_list'))

    if not (class_id or student_id):
        return _render(dict(error_msg='参数异常！'))

    detail = db.api.get_try_learn_detail(class_id, student_id)
    if detail.is_error():
        log.warn('get try learn detail failed. '
                 'class_id: {}, student_id: {}'.format(class_id, student_id))
        detail = dict()
    else:
        detail = detail.result()

    if show == 'first_meeting':
        # 是否参加会议
        in_meeting = db.api.is_in_meeting(class_id, student_id)
        if in_meeting.is_error():
            log.warn('get is in meeting failed. '
                     'class_id: {}, student_id: {}'.format(class_id, student_id))
        in_first_meeting = in_meeting.result().get('in_first_meeting', 0)

        detail.update(in_first_meeting=in_first_meeting)

    elif show == 'QA_meeting':
        # 是否参加会议
        in_meeting = db.api.is_in_meeting(class_id, student_id)
        if in_meeting.is_error():
            log.warn('get is in meeting failed. '
                     'class_id: {}, student_id: {}'.format(class_id, student_id))
        in_first_meeting = in_meeting.result().get('in_first_meeting', 0)
        in_qa_meeting = in_meeting.result().get('in_QA_meeting', 0)

        # 是否提交作业
        is_submit_task = db.api.is_submit_task(class_id, student_id)
        if is_submit_task.is_error():
            log.warn('get is submit task failed. '
                     'class_id: {}, student_id: {}'.format(class_id, student_id))
        is_submit_task = is_submit_task.result().get('is_submit_task', 0)

        # 是否提交满意度调查表
        is_submit_questionnaire = db.api.is_submit_questionnaire(class_id, student_id)
        if is_submit_questionnaire.is_error():
            log.warn('get is submit questionnaire failed. '
                     'class_id: {}, student_id: {}'.format(class_id, student_id))
        is_submit_questionnaire = is_submit_questionnaire.result().get(
            'is_submit_questionnaire', 0)

        if is_submit_questionnaire:
            # 提交满意度调查表详情
            questionnaire_records = db.api.get_questionnaire_records(class_id, student_id)
            if questionnaire_records.is_error():
                log.warn('get questionnaire records failed. '
                         'class_id: {}, student_id: {}'.format(class_id, student_id))
                questionnaire_records = []
            questionnaire_records = questionnaire_records.result()
        else:
            questionnaire_records = []

        detail.update(in_first_meeting=in_first_meeting,
                      in_QA_meeting=in_qa_meeting,
                      is_submit_task=is_submit_task,
                      is_submit_questionnaire=is_submit_questionnaire,
                      questionnaire_records=questionnaire_records)

    return _render(dict(learn_detail=detail, back_url=back_url, show=show))
