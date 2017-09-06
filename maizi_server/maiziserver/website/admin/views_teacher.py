# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.teacher import teacher as api_teacher
from django.http import HttpResponseNotFound,HttpResponseServerError


def get_query(request):

    page = {}
    query = {}
    return {
        "query": query,
        "page": page
    }

def teacher_query(request):
    query_info = get_query(request)

    result = api_teacher.list_teacher()

    if result.is_error():
        return HttpResponseServerError()

    teacher_list = result.result()["result"]

    context = {
        "menu": "person",
        "url": "/teacher/",
        "page": {},
        "query": query_info["query"],
        "queryString": views_tools.getQueryString(query_info["query"]),
        "teacher_list": teacher_list
    }

    return context

def teacher(request):
    context = teacher_query(request)

    return render(request,'admin/teacher.html',context)

def teacher_start(request):

    teacher_id = views_tools.get_param_by_request(request.GET, "id", "")

    result = api_teacher.start(teacher_id)
    if result.is_error():
        return HttpResponseServerError()

    context = teacher_query(request)
    return render(request,'admin/teacher.html',context)

def teacher_stop(request):

    teacher_id = views_tools.get_param_by_request(request.GET, "id", "")
    result = api_teacher.stop(teacher_id)
    if result.is_error():
        return HttpResponseServerError()

    context = teacher_query(request)
    return render(request, 'admin/teacher.html', context)

def teacher_add(request):
    context={
        "menu": "person"
    }
    return render(request,'admin/teacher_add.html',context)

@csrf_exempt
def teacher_add_do(request):

    name = views_tools.get_param_by_request(request.POST, "name", "")
    phone = views_tools.get_param_by_request(request.POST, "phone", "")
    qq = views_tools.get_param_by_request(request.POST, "qq", "")

    result = api_teacher.add(name,phone,qq)
    return views_tools.success_json()

def teacher_update(request):

    teacher_id = views_tools.get_param_by_request(request.GET, "id")
    result = api_teacher.get_teacher_by_id(teacher_id)

    if result.is_error():
        return HttpResponseServerError()

    teacher_info = result.result()
    if teacher_info == None:
        return HttpResponseServerError()

    context = {
        "menu": "person",
        "teacher": teacher_info
    }
    return render(request,'admin/teacher_update.html',context)

@csrf_exempt
def teacher_update_do(request):

    teacher_id = views_tools.get_param_by_request(request.POST, "id", "")
    name = views_tools.get_param_by_request(request.POST, "name", "")
    phone = views_tools.get_param_by_request(request.POST, "phone", "")
    qq = views_tools.get_param_by_request(request.POST, "qq", "")

    result = api_teacher.update(teacher_id,name,phone,qq)
    return views_tools.success_json()
