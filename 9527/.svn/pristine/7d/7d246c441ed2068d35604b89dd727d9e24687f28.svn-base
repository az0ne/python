#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from db.api.course import taskExcellentWorks as api_taskExcellentWorks
from db.api.apiutils import APIResult
from utils.decorators import dec_login_required
from utils import tool
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def task_excellent_works_list(request):
    """
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', 'delete', str)
    task_id = tool.get_param_by_request(request.GET, 'taskId', 0, int)

    if "delete" in action:
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        task_excellent_works = api_taskExcellentWorks.delete_task_excellent_works(_id)
        if task_excellent_works.is_error():
            # 处理错误
            return render_to_response("404.html", {}, RequestContext(request))

        return HttpResponseRedirect(
            '/course/task/taskDesc/edit/?action=show&taskId=' + str(task_id))


@dec_login_required
@handle_http_response_exception(501)
def task_excellent_works_edit(request):
    """
    get one data by id from mysql,
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    task_id = tool.get_param_by_request(request.GET, 'taskId', 0, int)

    c = None
    if "edit" in action and task_id:
        task_excellent_works = api_taskExcellentWorks.select_task_excellent_works_by_task_id(task_id)
        c = {"taskExcellentWorks": task_excellent_works.result(), "action": action}

        if task_excellent_works.is_error():
            return render_to_response("404.html", {}, RequestContext(request))
        else:
            return render_to_response("mz_course/task/taskExcellentWorks_list.html", c, RequestContext(request))

    if "edit" in action and (not task_id):
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        task_excellent_works = api_taskExcellentWorks.select_task_excellent_works_by_id(_id)
        c = {"taskExcellentWorks": task_excellent_works.result()[0], "action": action}

        if task_excellent_works.is_error():
            return render_to_response("404.html", {}, RequestContext(request))

    if 'add' in action:
        c = {"task_id": task_id, "action": action}

    return render_to_response("mz_course/task/taskExcellentWorks_edit.html", c, RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def task_excellent_works_save(request):
    """
    save data to mysql database,from update and add
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.POST, 'action', 'add', str)
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    task_id = tool.get_param_by_request(request.POST, 'task_id', 0, int)
    title = tool.get_param_by_request(request.POST, 'title', '', str)
    img_url = request.FILES.get('img_url', '')
    old_image_path = tool.get_param_by_request(request.POST, 'old_image_path', '', str)
    code_url = tool.get_param_by_request(request.POST, 'code_url', "", str)
    index = tool.get_param_by_request(request.POST, 'index', 0, int)

    task_excellent_works = APIResult()
    img_path = old_image_path
    if img_url:
        img_path = tool.upload(img_url, settings.COURSE_IMG_UPLOAD_PATH)

    if "add" in action:
        task_excellent_works = api_taskExcellentWorks.insert_task_excellent_works(task_id, title, img_path, code_url,
                                                                                  index)
    elif "edit" in action:
        task_excellent_works = api_taskExcellentWorks.update_task_excellent_works(_id, task_id, title, img_path,
                                                                                  code_url, index)

    if task_excellent_works.is_error():
        return render_to_response("404.html", {}, RequestContext(request))

    return HttpResponseRedirect('/course/task/taskDesc/edit/?action=show&taskId=' + str(task_id))
