#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.http import JsonResponse

from db.api.course import careerCatagory as api_careerCatagory
from django.conf import settings
from utils.decorators import dec_login_required
from utils import tool
from db.api.apiutils import APIResult
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def careerCatagory_list(request):
    """
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = ""

    careerCatagory = APIResult()
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        careerCatagory = api_careerCatagory.delete_career_catagory(_id)
        if careerCatagory.is_error():
            # 处理错误
            return render_to_response("html404.html", {}, context_instance=RequestContext(request))

        if not careerCatagory.result():
            return render_to_response("delete_error.html", {}, context_instance=RequestContext(request))

        else:
            return HttpResponseRedirect('/course/careerCatagory/list/?action=query&page_index=' + str(page_index))

    if action == "query":
        careerCatagory = api_careerCatagory.list_career_catagory_by_page(page_index, settings.PAGE_SIZE)

    if action == "search":
        key_word = tool.get_param_by_request(request.GET, 'keyword', '')
        careerCatagory = api_careerCatagory.get_career_catagory_by_name('%' + key_word + '%', page_index,
                                                                        settings.PAGE_SIZE)

    if careerCatagory.is_error():
        # 处理错误
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    c = {"careerCatagories": careerCatagory.result()["result"],
         "page": {"page_index": page_index, "rows_count": careerCatagory.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": careerCatagory.result()["page_count"],
                  }, "key_word": key_word}

    return render_to_response("mz_course/careerCatagory_list.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def careerCatagory_edit(request):
    """
    get one data by id from mysql,
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)

    careerCatagory = None
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        careerCatagory = api_careerCatagory.get_career_catagory_by_id(_id)

        if careerCatagory.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

        careerCatagory = careerCatagory.result()[0]

    c = {"careerCatagory": careerCatagory, "action": action, "page_index": page_index}

    return render_to_response("mz_course/careerCatagory_save.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def careerCatagory_save(request):
    """
    save data to mysql database,from update and add
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.POST, 'action', 'add', str)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)  # 当前页
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    name = tool.get_param_by_request(request.POST, 'name', "", str)

    careerCatagory = APIResult()
    if action == "add":
        careerCatagory = api_careerCatagory.insert_career_catagory(name)
    elif action == "edit":
        careerCatagory = api_careerCatagory.update_career_catagory(_id, name)

    if careerCatagory.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    return HttpResponseRedirect('/course/careerCatagory/list/?action=query&page_index=' + str(page_index))


