#! /usr/bin/evn python
# -*- coding:utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
import db.api.lps4.course.task
from utils.logger import logger as log
from django.conf import settings
from django.core.urlresolvers import reverse
from functions import get_task_name_by_id, IS_PROJECT


@dec_login_required
@handle_http_response_exception(501)
def task_edit(request):
    action = get_param_by_request(request.GET, "action", "add", str)
    if action == "edit":
        _id = get_param_by_request(request.GET, "id", 0, int)
        APIResult = db.api.lps4.course.task.get_task_by_id(_id)
        if APIResult.is_error():
            log.warn("get task by id failed.")
            return render(request, "404.html", {})
        task = APIResult.result()
    return render(request, "mz_lps4/mz_course/task/task_edit.html", dict(task=task, action=action))


# @dec_login_required
@handle_http_response_exception(501)
def task_list(request):
    action = get_param_by_request(request.GET, "action", "query", str)
    page_index = get_param_by_request(request.GET, "page_index", 1, int)
    keyword = get_param_by_request(request.GET, "keyword", "", str)
    request.session["url_back"] = request.get_full_path()
    if action == "search":
        APIResult = db.api.lps4.course.task.select_lps4_task(page_index=page_index, page_size=settings.PAGE_SIZE,
                                                             keyword='%' + keyword + '%', )
    else:
        APIResult = db.api.lps4.course.task.select_lps4_task(page_index=page_index, page_size=settings.PAGE_SIZE)
    if APIResult.is_error():
        log.warn("list lps4 task failed.")
        return render(request, "404.html", {})
    result = APIResult.result()
    if result:
        taskList = result["result"]
        if taskList:
            for task in taskList:
                task["is_project"] = IS_PROJECT[task["is_project"]]
                task["pre_task_name"] = get_task_name_by_id(request, task["pre_task"])
                task["next_task_name"] = get_task_name_by_id(request, task["next_task"])
    c = {"tasks": result["result"], "keyword": keyword,
         "page": {"page_index": page_index, "rows_count": result["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": result["page_count"]}}

    return render(request, "mz_lps4/mz_course/task/task_list.html", c)


@dec_login_required
@handle_http_response_exception(501)
def task_delete(request):
    _id = get_param_by_request(request.GET, "id", 0, int)
    if _id > 0:
        APIResult = db.api.lps4.course.task.delect_task_by_id(_id)
        if APIResult.is_error():
            log.warn("delete task failed.")
            return render(request, "404.html")
    return HttpResponseRedirect(request.session.get("url_back", reverse('mz_lps4:lps4_task_list')))


@dec_login_required
@handle_http_response_exception(501)
def task_save(request):
    action = get_param_by_request(request.POST, "action", "", str)
    name = get_param_by_request(request.POST, "name", "", str)
    career_id = get_param_by_request(request.POST, "career_id", 0, int)
    stage_id = get_param_by_request(request.POST, "stage_id", 0, int)
    index = get_param_by_request(request.POST, "index", 999, int)
    pre_task = get_param_by_request(request.POST, "pre_task", 0, int)
    next_task = get_param_by_request(request.POST, "next_task", 0, int)
    version = get_param_by_request(request.POST, "version", 0, int)
    is_project = get_param_by_request(request.POST, "is_project", 1, int)
    data = dict(name=name, career_id=career_id, stage_id=stage_id, index=index, pre_task=pre_task,
                next_task=next_task, version=version, is_project=is_project)
    if action in ["add", "edit"]:
        if action == "add":
            APIResult = db.api.lps4.course.task.insert_lps4_task(data)
        else:
            _id = get_param_by_request(request.POST, "id", 0, int)
            data["id"] = _id
            APIResult = db.api.lps4.course.task.update_lps4_task(data)
        result = APIResult.result()
        if APIResult.is_error() or not result:
            log.warn("%s lps4 task failed." % action)
            return render(request, "404.html")
    else:
        message = u"action must be add or edit."
        log.warn(message)
        return render(request, "404.html", dict(message=message))
    return HttpResponseRedirect(request.session.get("url_back", reverse('mz_lps4:lps4_task_list')))
