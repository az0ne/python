# -*- coding:utf-8 -*-
from django.conf import settings
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
import db.api.coach.task_lib
from utils.logger import logger as log
from mz_lps4.career.lps4_career import get_lps4_career_course


@dec_login_required
@handle_http_response_exception(501)
def task_lib_list(request):
    action = get_param_by_request(request.GET, 'action', 'query', str)
    keyword = get_param_by_request(request.GET, 'keyword', '', str)
    page_index = get_param_by_request(request.GET, 'page_index', 1, int)
    request.session["coach_task_back_url"] = request.get_full_path()
    if action == 'search':
        format_keyword = "%" + keyword + "%"
        APIResult = db.api.coach.task_lib.list_coach_task_lib_by_search(page_index=page_index, keyword=format_keyword)
    else:
        APIResult = db.api.coach.task_lib.list_coach_task_lib(page_index)
    if APIResult.is_error():
        log.warn('list coach task lib failed.')
        return render(request, '404.html')
    result = APIResult.result()
    c = {"tasks": result.get("result"), "keyword": keyword,
         "page": {"page_index": page_index, "rows_count": result["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": result["page_count"]}}
    return render(request, 'mz_lps4/coach/task_lib_list.html', c)


@dec_login_required
@handle_http_response_exception(501)
def task_lib_edit(request):
    action = get_param_by_request(request.GET, 'action', 'add', str)
    try:
        if action == "edit":
            _id = get_param_by_request(request.GET, 'id', 0, int)
            APIResult = db.api.coach.task_lib.get_coach_task_lib_by_id(_id)
            if APIResult.is_error():
                log.warn("get coach task lib by id failed.")
                raise Http404
            task = APIResult.result()
        else:
            task = dict()
        career_courses = get_lps4_career_course()
    except Http404:
        return render(request, '404.html')
    return render(request, 'mz_lps4/coach/task_lib_edit.html',
                  dict(task=task, career_courses=career_courses, action=action))


@dec_login_required
@handle_http_response_exception(501)
def get_task_by_career(request):
    career_id = get_param_by_request(request.GET, 'career_id', 0, int)
    if career_id:
        APIResult = db.api.coach.task_lib.get_task_by_career_id(career_id=career_id)
        if APIResult.is_error():
            log.warn('get task by career id failed.')
            return JsonResponse(dict(status='failed'))
        tasks = APIResult.result()
        # APIResult = db.api.coach.task_lib.get_teacher_by_career(career_id=career_id)
        # if APIResult.is_error():
        #     log.warn('get task by career id failed.')
        #     return JsonResponse(dict(status='failed'))
        # teachers = APIResult.result()
        # print teachers
        # return JsonResponse(dict(status='success',tasks=tasks, teachers=teachers))
        return JsonResponse(dict(status='success', tasks=tasks))
    return JsonResponse(dict(status='failed'))


@dec_login_required
@handle_http_response_exception(501)
def task_lib_save(request):
    action = get_param_by_request(request.POST, 'action', 'add', str)
    content = get_param_by_request(request.POST, 'content', '', str)
    if action == 'edit':
        coach_id = get_param_by_request(request.POST, 'coach_id', 0, int)
        APIResult = db.api.coach.task_lib.update_task_lib_content(_id=coach_id, content=content)
    else:
        career_id = get_param_by_request(request.POST, 'career_id', 0, int)
        task_id = get_param_by_request(request.POST, 'task_id', 0, int)
        teacher_id = get_param_by_request(request.POST, 'teacher_id', 0, int)
        coach_dict = dict(content=content, career_id=career_id, task_id=task_id, teacher_id=teacher_id)
        APIResult = db.api.coach.task_lib.insert_task_lib(coach_dict)
    if APIResult.is_error():
        log.warn('insert or update coach_task_lib failed.')
        return render(request, '404.html')
    return HttpResponseRedirect(request.session.get('coach_task_back_url', reverse('mz_lps4:tasklibList')))


@dec_login_required
@handle_http_response_exception(501)
def task_lib_delete(request):
    _id = get_param_by_request(request.GET, 'id', 0, int)
    APIResult = db.api.coach.task_lib.delete_coach_task_by_id(_id)
    if APIResult.is_error():
        log.warn('delete coach task lib by id failed.')
        return render(request, '404.html')
    return HttpResponseRedirect(request.session.get('coach_task_back_url', reverse('mz_lps4:tasklibList')))


@dec_login_required
@handle_http_response_exception(501)
def check_is_have_content_by_task(request):
    task_id = get_param_by_request(request.GET, 'task_id', 0, int)
    career_id = get_param_by_request(request.GET, 'career_id', 0, int)
    if task_id > 0:
        APIResult = db.api.coach.task_lib.check_content_by_task_id(task_id, career_id)
        if APIResult.is_error():
            log.warn('get count by task_id from mz_coach_task_lib failed')
            return JsonResponse(dict(status='failed', msg='服务器获取数据失败。'))
        count = APIResult.result().get('count')
        is_have = False if count == 0 else True
        return JsonResponse(dict(status='success', is_have=is_have))
    return JsonResponse(dict(status='failed', msg='任务球ID值错误！'))
