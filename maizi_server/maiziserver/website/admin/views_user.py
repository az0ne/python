# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.user import user as api_user
from django.http import HttpResponseNotFound,HttpResponseServerError

def index(request):

    return render(request,'login.html')

def get_query(request):

    page_index = views_tools.get_param_by_request(request.GET, "page_index", 1, int)
    page_size = views_tools.get_param_by_request(request.GET, "page_size", 10, int)

    user_name = views_tools.get_param_by_request(request.GET, "user_name", "")
    real_name = views_tools.get_param_by_request(request.GET, "real_name", "")

    page = {
        "page_index":page_index,
        "page_size":page_size
    }

    query = {
        "user_name": user_name,
        "real_name": real_name
    }

    return {
             "query":query,
             "page":page
            }

def user_query(request):
    query_info = get_query(request)

    skip = views_tools.get_skip(query_info["page"]["page_index"], query_info["page"]["page_size"])
    result = api_user.list_user(query_info["query"]["user_name"], query_info["query"]["real_name"], skip)

    if result.is_error():
        return HttpResponseServerError()

    rows_count = result.result()["rows_count"]
    user_list = result.result()["result"]
    page = views_tools.get_page(query_info["page"]["page_index"],
                                query_info["page"]["page_size"],
                                rows_count)
    context = {
        "menu":"person",
        "url": "/user/",
        "page": page,
        "query": query_info["query"],
        "queryString": views_tools.getQueryString(query_info["query"]),
        "user_list": user_list
    }

    return context

def user(request):

    context = user_query(request)
    return render(request,'admin/user.html',context)

def user_start(request):

    user_id = views_tools.get_param_by_request(request.GET, "id", "")
    result = api_user.start(user_id)
    if result.is_error():
        return HttpResponseServerError()

    context = user_query(request)
    return render(request,'admin/user.html',context)

def user_stop(request):

    user_id = views_tools.get_param_by_request(request.GET, "id", "")
    result = api_user.stop(user_id)
    if result.is_error():
        return HttpResponseServerError()

    context = user_query(request)
    return render(request, 'admin/user.html', context)

def user_add(request):
    context = {
        "menu": "person"
    }
    return render(request,'admin/user_add.html',context)

@csrf_exempt
def user_add_do(request):

    user_name = views_tools.get_param_by_request(request.POST, "user_name", "")
    real_name = views_tools.get_param_by_request(request.POST, "real_name", "")
    password = views_tools.get_param_by_request(request.POST, "password", "")
    remark = views_tools.get_param_by_request(request.POST, "remark", "")

    result = api_user.get_user_by_name(user_name)

    if result.is_error():
        return views_tools.failed_json()

    user_info = result.result()
    if user_info != None:
        return views_tools.failed_json(200, "用户已存在")

    result = api_user.add(user_name,real_name,password,remark)
    return views_tools.success_json()

@views_tools.catch_views_exception
def user_update(request):
    user_id = views_tools.get_param_by_request(request.GET, "id")

    result = api_user.get_user_by_id(user_id)

    if result.is_error():
        return HttpResponseServerError()

    user_info = result.result()
    if user_info == None:
        return HttpResponseServerError()

    context = {
        "menu": "person",
        "user": user_info
    }
    return render(request,'admin/user_update.html',context)

@csrf_exempt
def user_update_do(request):

    user_id = views_tools.get_param_by_request(request.POST, "id", "")
    user_name = views_tools.get_param_by_request(request.POST, "user_name", "")
    real_name = views_tools.get_param_by_request(request.POST, "real_name", "")
    password = views_tools.get_param_by_request(request.POST, "password", "")
    remark = views_tools.get_param_by_request(request.POST, "remark", "")

    result = api_user.update(user_id,user_name,real_name,password,remark)
    return views_tools.success_json()


@csrf_exempt
@views_tools.catch_ajax_exception
def user_login(request):
    user_name = views_tools.get_param_by_request(request.POST, "user_name")
    password = views_tools.get_param_by_request(request.POST, "password")
    result = api_user.get_user_by_name(user_name)

    remark = result.result()["remark"]

    if result.is_error():
        return views_tools.failed_json()

    user_info = result.result()
    if user_info == None:
        return views_tools.failed_json(200, "用户不存在")

    if (user_info["is_delete"] == "1"):
        return views_tools.failed_json(200, "用户被禁用")

    if (user_info["password"] == password):

        request.session["user_id"] = user_info["id"]
        request.session["user_name"] = user_info["user_name"]
        request.session["real_name"] = user_info["real_name"]
        return views_tools.success_json(200, remark)

    return views_tools.failed_json(200, "用户名或密码错误")

@csrf_exempt
def user_login_out(request):
    # response = views_tools.success_json()
    #
    del request.session["user_id"]
    del request.session["user_name"]
    del request.session["real_name"]
    #
    # response.delete_cookie("user_id")
    # response.delete_cookie("user_name")
    # response.delete_cookie("password")

    return views_tools.success_json()
