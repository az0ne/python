#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from db.api.course import taskArticle as api_taskArticle
from db.api.apiutils import APIResult
from utils.decorators import dec_login_required
from utils import tool
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def task_article_list(request):
    """
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    task_id = tool.get_param_by_request(request.GET, 'taskId', 0, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)

    task_article = APIResult()
    if "delete" in action:
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        task_article = api_taskArticle.delete_task_article(_id)
        if task_article.is_error():
            # 处理错误
            return render_to_response("html404.html", {}, context_instance=RequestContext(request))

        if not task_article.result():
            return render_to_response("delete_error.html", {}, context_instance=RequestContext(request))

        else:
            return HttpResponseRedirect(
                '/course/task/taskDesc/edit/?action=show&taskId=' + str(task_id))

    if task_article.is_error():
        # 处理错误
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    c = {"task_articles": task_article.result()["result"],
         "key_word": key_word}

    return render_to_response("mz_course/task/task_show.html", c,
                              context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def task_article_edit(request):
    """
    get one data by id from mysql,
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    task_id = tool.get_param_by_request(request.GET, 'taskId', 0, int)

    c = None

    if "edit" in action and task_id:
        task_article = api_taskArticle.select_task_article_by_task_id(task_id)
        c = {"taskArticles": task_article.result(), "action": action}

        if task_article.is_error():
            return render_to_response("404.html", {}, RequestContext(request))

        return render_to_response("mz_course/task/taskArticle_list.html", c, RequestContext(request))

    if "edit" in action and (not task_id):
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        task_article = api_taskArticle.select_task_article_by_id(_id)
        c = {"taskArticle": task_article.result()[0], "action": action}
        if task_article.is_error():
            return render_to_response("404.html", {}, RequestContext(request))

    if 'add' in action:
        c = {"task_id": task_id, "action": action}

    return render_to_response("mz_course/task/taskArticle_edit.html", c, RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def task_article_save(request):
    """
    save data to mysql database,from update and add
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.POST, 'action', 'add', str)
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    task_id = tool.get_param_by_request(request.POST, 'task_id', 0, int)
    article_title = tool.get_param_by_request(request.POST, 'article_title', '', str)
    article_url = tool.get_param_by_request(request.POST, 'article_url', "", str)
    index = tool.get_param_by_request(request.POST, 'index', 0, int)
    _type = tool.get_param_by_request(request.POST, 'type', 0, int)

    task_article = APIResult()
    if action == "add":
        task_article = api_taskArticle.insert_task_article(task_id, article_title, article_url, index, _type)
    elif action == "edit":
        task_article = api_taskArticle.update_task_article(_id, task_id, article_title, article_url, index, _type)

    if task_article.is_error():
        return render_to_response("404.html", {}, RequestContext(request))

    return HttpResponseRedirect('/course/task/taskDesc/edit/?action=show&taskId=' + str(task_id))
