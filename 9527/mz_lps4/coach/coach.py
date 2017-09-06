# -*- coding:utf-8 -*-
from django.conf import settings
from django.http import Http404
from django.shortcuts import render

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
import db.api.coach.coach_api
from utils.logger import logger as log
from mz_lps4.career.lps4_career import get_lps4_career_course
from mz_lps4.coach.coach_interface import get_coach_status_by_id, coach_excel_export_format

SOURCE_TYPES = {10: u'学生主动发起', 11: u'学生视频问答', 20: u'老师主动发起', 30: u'项目辅导', 40: u'任务球解锁', 50: u'新学员入学沟通'}
IS_DONE_TYPE = {0: u'未完成', 1: u'已完成', 2: u'已取消'}


@dec_login_required
@handle_http_response_exception(501)
def coach_info_list(request):
    action = get_param_by_request(request.GET, 'action', 'query', str)
    keyword_dict = dict()
    page_index = get_param_by_request(request.GET, 'page_index', 1, int)

    if 'search' in action:
        career_id = get_param_by_request(request.GET, 'career_id', 0, int)
        start_date = get_param_by_request(request.GET, 'start_date', '', str)
        end_date = get_param_by_request(request.GET, 'end_date', '', str)
        if career_id:
            keyword_dict.update(dict(career_id=career_id))
        if start_date and end_date:
            if start_date > end_date:
                start_date, end_date = end_date, start_date
            keyword_dict.update(dict(start_date=start_date, end_date=end_date))
        APIResult = db.api.coach.coach_api.list_coach_info(page_index, action=action, keyword=keyword_dict)
    else:
        APIResult = db.api.coach.coach_api.list_coach_info(page_index)
    if APIResult.is_error():
        log.warn('list all coach info from mz_coach failed.')
        return render(request, '404.html')
    result = APIResult.result()

    coachs = result.get("result")
    try:
        if coachs:
            for coach in coachs:
                coach['teacher_name'] = coach.get('teacher_real_name') if coach.get('teacher_real_name') else coach.get(
                    'teacher_nick_name')
                coach['student_name'] = coach.get('student_real_name') if coach.get('student_real_name') else coach.get(
                    'student_nick_name')
                coach['source_type_name'] = SOURCE_TYPES.get(coach.get('source_type'), None)
                coach['done_status'] = get_coach_status_by_id(coach.get('coach_id', 0))
        careers = get_lps4_career_course()
    except Http404:
        return render(request, '404.html')

    if 'excel' in action:
        return coach_excel_export_format(coachs)

    c = {"coachs": coachs, "keyword": keyword_dict, "careers": careers,
         "page": {"page_index": page_index, "rows_count": result["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": result["page_count"]}}
    return render(request, 'mz_lps4/coach/coach_list.html', c)


@dec_login_required
@handle_http_response_exception(501)
def coach_info_edit(request):
    coach_id = get_param_by_request(request.GET, "coach_id", 0, int)
    APIResult = db.api.coach.coach_api.get_coach_info_by_id(coach_id)
    if APIResult.is_error():
        log.warn("get coach info by id failed.")
        return render(request, '404.html')
    coach = APIResult.result()
    coach['source_type_name'] = SOURCE_TYPES.get(coach.get('source_type'), None)
    try:
        coach['done_status'] = get_coach_status_by_id(coach.get('coach_id', 0))
    except Http404:
        return render(request, '404.html')
    return render(request, 'mz_lps4/coach/coach_edit.html', dict(coach=coach))


@dec_login_required
@handle_http_response_exception(501)
def export_all_coach(request):
    APIResult = db.api.coach.coach_api.get_all_coach_info()
    if APIResult.is_error():
        log.warn("get all coach info by id failed.")
        return render(request, '404.html')
    coachs = APIResult.result()
    try:
        if coachs:
            for coach in coachs:
                coach['teacher_name'] = coach.get('teacher_real_name') if coach.get('teacher_real_name') else \
                    coach.get('teacher_nick_name')
                coach['student_name'] = coach.get('student_real_name') if coach.get('student_real_name') else \
                    coach.get('student_nick_name')
                coach['source_type_name'] = SOURCE_TYPES.get(coach.get('source_type'), None)
                coach['done_status'] = get_coach_status_by_id(coach.get('coach_id', 0))
    except Http404:
        return render(request, '404.html')
    return coach_excel_export_format(coachs)
