#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from utils.decorators import dec_login_required
from db.api.apiutils import APIResult
from db.api.seo import objSEO as api_objSEO
from utils import tool
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def obj_seo_list(request):
    """

    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', '', str)

    obj_seo = APIResult()
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        obj_seo = api_objSEO.delete_obj_seo(_id)
        if obj_seo.is_error():
            # 处理错误
            return render_to_response("html404.html", {}, context_instance=RequestContext(request))

        if not obj_seo.result():
            return render_to_response("delete_error.html", {}, context_instance=RequestContext(request))

        else:
            return HttpResponseRedirect('/seo/objSEO/list/?action=query&page_index=' + str(page_index))

    if action == "query":
        obj_seo = api_objSEO.list_obj_seo_by_page(page_index, settings.PAGE_SIZE)

    if action == "search":
        obj_seo = api_objSEO.list_obj_seo_by_seo_title('%' + key_word + '%', page_index, settings.PAGE_SIZE)

    if obj_seo.is_error():
        # 处理错误
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    c = {"obj_seoes": obj_seo.result()["result"],
         "page": {"page_index": page_index, "rows_count": obj_seo.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": obj_seo.result()["page_count"],
                  }, "key_word": key_word}

    return render_to_response("mz_seo/objSEO_list.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def obj_seo_edit(request):
    """
    get one data by id from mysql,
    :param request:
    :return:
    """

    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)

    obj_seo = None
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        obj_seo = api_objSEO.get_obj_seo_by_id(_id)
        print obj_seo.result(), obj_seo.is_error()
        if obj_seo.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

        obj_seo = obj_seo.result()[0]
    c = {"objseo": obj_seo, "action": action, "page_index": page_index}

    return render_to_response("mz_seo/objSEO_save.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def obj_seo_save(request):
    """
    save data to mysql database,from update and add
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.POST, 'action', 'add', str)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)  # 当前页
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    obj_type = tool.get_param_by_request(request.POST, 'obj_type', '', str)
    obj_id = tool.get_param_by_request(request.POST, 'obj_id', 0, int)
    seo_title = tool.get_param_by_request(request.POST, 'seo_title', "", str)
    seo_keyword = tool.get_param_by_request(request.POST, 'seo_keywords', "", str)
    seo_description = tool.get_param_by_request(request.POST, 'seo_description', "", str)

    obj_seo = APIResult()
    if action == "add":
        obj_seo = api_objSEO.insert_obj_seo(obj_type, obj_id, seo_title, seo_keyword, seo_description)

    elif action == "edit":
        obj_seo = api_objSEO.update_obj_seo(_id, obj_type, obj_id, seo_title, seo_keyword, seo_description)

    if obj_seo.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    return HttpResponseRedirect('/seo/objSEO/list/?action=query&page_index=' + page_index)
