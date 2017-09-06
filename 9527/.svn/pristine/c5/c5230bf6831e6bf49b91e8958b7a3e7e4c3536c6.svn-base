# -*- coding:utf-8 -*-
from django.http import Http404
from django.shortcuts import render
import db.api.lps4.teacher_evaluation.teacher_backlog
from django.conf import settings

from mz_lps4.career.lps4_career import get_lps4_career_course
from mz_lps4.teacher_evaluation.interface import DONE_STATUS_DICT, backlog_excel_export_format
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request, get_page_info, get_page_count
from utils.logger import logger as log
from interface import add_not_done_status
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.core.urlresolvers import reverse

@dec_login_required
@handle_http_response_exception(501)
def teacher_back_list(request):
    action = get_param_by_request(request.GET, "action", "query", str)
    page_index = get_param_by_request(request.GET, "page_index", 1, int)
    page_size = settings.PAGE_SIZE
    keyword = get_param_by_request(request.GET, "keyword", "", str)
    is_done = get_param_by_request(request.GET, "is_done", -1, int)
    done_status = get_param_by_request(request.GET, "done_status", 0, int)
    career_id = get_param_by_request(request.GET, "career_id", 0, int)
    start_date = get_param_by_request(request.GET, "start_date", "", str)
    end_date = get_param_by_request(request.GET, "end_date", "", str)
    if "search" in action:
        if keyword == "约课":  # 约课在主站中是写死的，数据库中获取不到该类型名称
            my_keyword = 5
        else:
            my_keyword = "%" + keyword + "%"
        dict_keyword = dict(keyword=my_keyword)
        if not is_done < 0:
            dict_keyword['is_done'] = is_done
        if done_status > 0:
            dict_keyword['done_status'] = done_status
        if career_id > 0:
            dict_keyword['career_id'] = career_id
        if start_date and end_date:
            if start_date > end_date:
                start_date, end_date = end_date, start_date
            dict_keyword['start_date'] = start_date
            dict_keyword['end_date'] = end_date
        APIResult = db.api.lps4.teacher_evaluation.teacher_backlog.get_all_teacher_backlog_by_search(
            page_index=page_index, page_size=page_size, dict_keyword=dict_keyword)
    elif "coach" in action:
        coach_id = get_param_by_request(request.GET, "coach_id", 0, int)
        APIResult = db.api.lps4.teacher_evaluation.teacher_backlog.get_teacher_backlog_by_coach(page_index=page_index,
                                                                                                page_size=page_size,
                                                                                                coach_id=coach_id)
    else:
        APIResult = db.api.lps4.teacher_evaluation.teacher_backlog.get_all_teacher_backlog(page_index=page_index,
                                                                                           page_size=page_size)
    if APIResult.is_error():
        log.warn("get all teacher backlog by page failed.")
        return render(request, "404.html")

    try:
        careers = get_lps4_career_course()
    except Http404:
        return render(request, "404.html")
    result = APIResult.result()
    if is_done < 1 and done_status > 0:
        backlogs = add_not_done_status(result.get('result'))
        backlogs = filter(lambda x: x['done_status'] == done_status, backlogs)
        start_index = get_page_info(page_index, page_size)
        rows_count = len(backlogs)
        backlogs = backlogs[start_index:start_index+page_size]
        page_count = get_page_count(rows_count, page_size)

    else:
        backlogs = result.get('result')
        page_count = result.get('page_count')
        rows_count = result["rows_count"]

    c = {"backlogs": backlogs, "keyword": keyword, 'is_done': is_done, 'done_status': done_status, 'careers': careers,
         'career_id': career_id, 'start_date': start_date, 'end_date': end_date,
         "page": {"page_index": page_index, "rows_count": rows_count,
                  "page_size": page_size,
                  "page_count": page_count}}
    return render(request, "mz_lps4/teacher_evaluation/backlog_list.html", c)


@dec_login_required
@handle_http_response_exception(501)
def teacher_back_show(request):
    _id = get_param_by_request(request.GET, "id", 0, int)
    APIResult = db.api.lps4.teacher_evaluation.teacher_backlog.get_backlog_by_id(_id)
    if APIResult.is_error():
        log.warn("get backlog by id failed.")
        return render(request, "404.html")
    result = APIResult.result()
    if result:
        result['done_status'] = DONE_STATUS_DICT.get(result.get('done_status', 0))
    data = dict(result=result)
    return render(request, "mz_lps4/teacher_evaluation/backlog_show.html", data)


@dec_login_required
@handle_http_response_exception(501)
def teacher_back_excel_export_by_month(request):
    date = get_param_by_request(request.GET, "date", "", str)
    if date:
        APIResult = db.api.lps4.teacher_evaluation.teacher_backlog.get_teacher_backlog_by_date(date)
        if APIResult.is_error():
            log.warn("get backlog by date failed.")
            return render(request, "404.html")
        backlogs = APIResult.result().get('result')
        if backlogs:
            backlogs = add_not_done_status(backlogs)
            for backlog in backlogs:
                backlog['done_status'] = DONE_STATUS_DICT.get(backlog.get('done_status', 0))
    return backlog_excel_export_format(backlogs)


@dec_login_required
@handle_http_response_exception(501)
def teacher_backlog_add_opt_log(request):
    user_id = request.session.get('userid')
    user_name = request.session.get('username')
    backlog_id = get_param_by_request(request.POST, "backlog_id", 0, int)
    content = get_param_by_request(request.POST, "opt_content", '', str)
    result = db.api.lps4.teacher_evaluation.teacher_backlog.insert_backlog_opt_log(user_id, user_name,
                                                                                   content, backlog_id)
    if result.is_error():
        log.warn('insert_backlog_opt_log failed.')
        return render(request, "404.html")
    return HttpResponseRedirect(reverse("mz_lps4:teacherBacklogList"))


@dec_login_required
@handle_http_response_exception(501)
def teacher_backlog_opt_log_list(request):
    backlog_id = get_param_by_request(request.GET, "backlog_id", 0, int)
    result = db.api.lps4.teacher_evaluation.teacher_backlog.get_backlog_opt_log(backlog_id)
    if result.is_error():
        log.warn('insert_backlog_opt_log failed.')
        return JsonResponse(dict(status=False, massage=u'服务器错误'))
    data = result.result()
    return JsonResponse(dict(status=True, data=data))
