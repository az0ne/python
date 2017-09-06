#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
import datetime

from db.api.course import taskDesc as api_taskDesc
from db.api.course import taskArticle as api_taskArticle
from db.api.course import taskExcellentWorks as api_taskExcellentWorks
from db.api.apiutils import APIResult
from utils.decorators import dec_login_required
from utils import tool
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def task_desc_list(request):
    """
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)

    task_desc = APIResult()
    if "delete" in action:
        task_id = tool.get_param_by_request(request.GET, 'taskId', 0, int)
        task_desc = api_taskDesc.delete_task_desc_by_task_id(task_id)
        if task_desc.is_error():
            # 处理错误
            return render_to_response("html404.html", {}, context_instance=RequestContext(request))

        if not task_desc.result():
            return render_to_response("delete_error.html", {}, context_instance=RequestContext(request))

        else:
            return HttpResponseRedirect('/course/task/taskDesc/list/?action=query&page_index=' + str(page_index))

    if "query" in action:
        task_desc = api_taskDesc.select_task_desc_by_page(page_index, settings.PAGE_SIZE)

    if "search" in action:
        if "%" in action:
            key_word1 = '//' + key_word
        else:
            key_word1 = key_word
        task_desc = api_taskDesc.search_task_desc_by_title('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)

    if task_desc.is_error():
        # 处理错误
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    c = {"taskDescs": task_desc.result()["result"],
         "page": {"page_index": page_index, "rows_count": task_desc.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": task_desc.result()["page_count"],
                  }, "key_word": key_word}

    return render_to_response("mz_course/task/taskDesc_list.html", c, RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def task_desc_edit(request):
    """
    get one data by id from mysql,
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)

    if "show" in action:
        task_id = tool.get_param_by_request(request.GET, 'taskId', 0, int)
        task_desc = api_taskDesc.select_task_desc_by_task_id(task_id)
        task_article = api_taskArticle.select_task_article_by_task_id(task_id)
        task_excellent_works = api_taskExcellentWorks.select_task_excellent_works_by_task_id(task_id)

        if task_desc.is_error() or task_article.is_error() or task_excellent_works.is_error():
            return render_to_response("404.html", {}, RequestContext(request))

        c = {"taskDesc": task_desc.result()[0], "taskArticles": task_article.result(),
             "taskExcellentWorks": task_excellent_works.result(),
             "action": action, "page_index": page_index}

        return render_to_response("mz_course/task/task_show.html", c, RequestContext(request))

    if "edit" in action:
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        task_desc = api_taskDesc.select_task_desc_by_id(_id)

        if task_desc.is_error():
            return render_to_response("404.html", {}, RequestContext(request))

        c = {"taskDesc": task_desc.result()[0], "action": action, "page_index": page_index}

    if "add" in action:
        c = {"action": action}

    return render_to_response("mz_course/task/taskDesc_edit.html", c, RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def task_desc_save(request):
    """
    save data to mysql database,from update and add
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.POST, 'action', 'add', str)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)  # 当前页
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    task_id = tool.get_param_by_request(request.POST, 'task_id', 0, int)
    img1 = request.FILES.get('img1', '')
    img2 = request.FILES.get('img2', '')
    img3 = request.FILES.get('img3', '')
    old_img1_path = tool.get_param_by_request(request.POST, 'old_img1_path', "", str)
    old_img2_path = tool.get_param_by_request(request.POST, 'old_img2_path', "", str)
    old_img3_path = tool.get_param_by_request(request.POST, 'old_img3_path', "", str)
    title = tool.get_param_by_request(request.POST, 'title', "", str)
    operator_id = tool.get_param_by_request(request.POST, 'operator_id', 0, int)
    created_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_time = created_time

    img1_path = old_img1_path  # 如果更新数据时，未更改图片，image_url为空，设置图片的路径为老路径
    img2_path = old_img2_path
    img3_path = old_img3_path
    if img1:
        img1_path = tool.upload(img1, settings.COURSE_IMG_UPLOAD_PATH)
    if img2:
        img2_path = tool.upload(img2, settings.COURSE_IMG_UPLOAD_PATH)
    if img3:
        img3_path = tool.upload(img3, settings.COURSE_IMG_UPLOAD_PATH)

    task_desc = APIResult()

    if action == "add":
        task_desc = api_taskDesc.insert_task_desc(task_id, img1_path, img2_path, img3_path, title, created_time,
                                                  update_time, operator_id)
    elif action == "edit":
        task_desc = api_taskDesc.update_task_desc(_id, task_id, img1_path, img2_path, img3_path, title,
                                                  update_time)

    if task_desc.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    return HttpResponseRedirect('/course/task/taskDesc/list/?action=query&page_index=' + str(page_index))

