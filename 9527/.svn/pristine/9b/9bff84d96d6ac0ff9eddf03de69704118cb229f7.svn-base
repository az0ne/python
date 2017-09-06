#!/usr/bin/env python
# -*- coding: utf8 -*-
import db.api.micro.wechat_course.wechat_course_discuss
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from wechat_discuss_interface import *
from django.http import HttpResponseRedirect
from django.conf import settings
from utils.tool import get_param_by_request
from django.shortcuts import render
from django.core.urlresolvers import reverse


@dec_login_required
@handle_http_response_exception(501)
def list_parent_discuss(request):
    page_index = get_param_by_request(request.GET, "page_index", 1, int)
    action = get_param_by_request(request.GET, "action", "query", str)
    get_keyword = get_param_by_request(request.GET, "keyword", "", str)
    try:
        if "search" in action:
            keyword = "%" + get_keyword + "%"
            result = list_wechat_parent_dicuss_by_search(page_index=page_index, page_size=settings.PAGE_SIZE,
                                                         keyword=keyword)
        else:
            result = list_wechat_parent_dicuss(page_index=page_index, page_size=settings.PAGE_SIZE)
        request.session["parent_discuss_list_url"] = request.get_full_path()
    except Http404:
        return render(request, "404.html")
    c = {"action": action, "discusses": result["result"], "keyword": get_keyword,
         "page": {"page_index": page_index, "page_size": settings.PAGE_SIZE,
                  "rows_count": result["rows_count"], "page_count": result["page_count"],
                  }}
    return render(request, "mz_micro/wechat_course/wechat_discuss_parent_list.html", c)


@dec_login_required
@handle_http_response_exception(501)
def list_child_discuss(request):
    parent_id = get_param_by_request(request.GET, "parent_id", -1, int)
    try:
        result = list_wechat_child_discuss(parent_id)
        request.session["child_discuss_list_url"] = request.get_full_path()

    except Http404:
        return render(request, "404.html")
    return render(request, "mz_micro/wechat_course/wechat_discuss_child_list.html", dict(discusses=result,
                                                                                         parent_id=parent_id))


@dec_login_required
@handle_http_response_exception(501)
def delete_parent_discuss(request):
    _id = get_param_by_request(request.GET, "discuss_id", 0, int)
    try:
        del_wechat_parent_discuss(_id)
    except Http404:
        return render(request, "404.html")
    return HttpResponseRedirect(
        request.session.get("parent_discuss_list_url", reverse("mz_wechat:wechat_parent_discuss_list")))


@dec_login_required
@handle_http_response_exception(501)
def delete_child_discuss(request):
    _id = get_param_by_request(request.GET, "discuss_id", 0, int)
    try:
        del_wechat_child_discuss(_id)
    except Http404:
        return render(request, "404.html")
    return HttpResponseRedirect(
        request.session.get("child_discuss_list_url", reverse("mz_wechat:wechat_parent_discuss_list")))


@dec_login_required
@handle_http_response_exception(501)
def insert_wechat_child_discuss(request):
    course_id = get_param_by_request(request.POST, "course_id", 0, int)
    parent_id = get_param_by_request(request.POST, "parent_id", 0, int)
    union_id = get_param_by_request(request.POST, "union_id", "", str)
    nick_name = u"老师"
    content = get_param_by_request(request.POST, "content", "", str)
    discuss_dict = dict(course_id=course_id, parent_id=parent_id, nick_name=nick_name, content=content)
    try:
        insert_wechat_discuss(discuss_dict=discuss_dict)
        db.api.micro.wechat_course.wechat_course_discuss.update_reply_count(course_id, union_id)
    except Http404:
        return render(request, "404.html")
    return HttpResponseRedirect(
        request.session.get("child_discuss_list_url", reverse("mz_wechat:wechat_parent_discuss_list")))


@dec_login_required
@handle_http_response_exception(501)
def edit_wechat_discuss(request):
    _id = get_param_by_request(request.GET, "discuss_id", 0, int)
    try:
        result = get_parent_discuss_by_id(_id)
    except Http404:
        return render(request, "404.html")
    return render(request, "mz_micro/wechat_course/wechat_discuss_edit.html", dict(discuss=result))


@dec_login_required
@handle_http_response_exception(501)
def back_to_parent_discuss(request):
    url = request.session.get("parent_discuss_list_url", reverse("mz_wechat:wechat_parent_discuss_list"))
    return HttpResponseRedirect(url)
