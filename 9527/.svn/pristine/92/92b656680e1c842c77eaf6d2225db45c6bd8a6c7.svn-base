#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import JsonResponse

from db.api.course import objTagRelation as api_objTagRelation
from db.api.apiutils import APIResult
from utils.decorators import dec_login_required
from utils import tool
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def obj_tag_relation_list(request):
    """
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)

    obj_tag_relation = APIResult()
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        obj_tag_relation = api_objTagRelation.delete_obj_tag_relation(_id)
        if obj_tag_relation.is_error():
            # 处理错误
            return render_to_response("html404.html", {}, context_instance=RequestContext(request))

        if not obj_tag_relation.result():
            return render_to_response("delete_error.html", {}, context_instance=RequestContext(request))

        else:
            return HttpResponseRedirect('/course/objTagRelation/list/?action=query&page_index=' + str(page_index))

    if action == "query":
        obj_tag_relation = api_objTagRelation.list_obj_tag_relation_by_page(page_index, settings.PAGE_SIZE)

    if action == "search":
        obj_tag_relation = api_objTagRelation.list_obj_tag_relation_by_name('%' + key_word + '%', page_index, settings.PAGE_SIZE)

    if obj_tag_relation.is_error():
        # 处理错误
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    c = {"objTagRelationes": obj_tag_relation.result()["result"],
         "page": {"page_index": page_index, "rows_count": obj_tag_relation.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": obj_tag_relation.result()["page_count"],
                  }, "key_word": key_word}

    return render_to_response("mz_course/objTagRelation_list.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def obj_tag_relation_edit(request):
    """
    get one data by id from mysql,
    :param request:
    :return:
    """

    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    obj_tag_relation = None
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        obj_tag_relation = api_objTagRelation.get_obj_tag_relation_by_id(_id)

        if obj_tag_relation.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

        obj_tag_relation = obj_tag_relation.result()[0]
    c = {"objTagRelation": obj_tag_relation, "action": action, "page_index": page_index}

    return render_to_response("mz_course/objTagRelation_save.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def obj_tag_relation_save(request):
    """
    save data to mysql database,from update and add
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.POST, 'action', 'add', str)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)  # 当前页
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    obj_type = tool.get_param_by_request(request.POST, 'obj_type', "", str)
    obj_id = tool.get_param_by_request(request.POST, 'obj_id', 0, int)
    tag_id = tool.get_param_by_request(request.POST, 'tag_id', 0, int)
    careercatagory_id = tool.get_param_by_request(request.POST, 'careercatagory_id', 0, int)

    obj_tag_relation = APIResult()
    if action == "add":
        obj_tag_relation = api_objTagRelation.insert_obj_tag_relation(obj_type, obj_id, tag_id, careercatagory_id)
    elif action == "edit":
        obj_tag_relation = api_objTagRelation.update_obj_tag_relation(_id, obj_type, obj_id, tag_id, careercatagory_id)

    if obj_tag_relation.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    return HttpResponseRedirect('/course/objTagRelation/list/?action=query&page_index=' + str(page_index))


