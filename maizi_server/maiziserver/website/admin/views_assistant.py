# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.assistant import assistant as api_assistant
from django.http import HttpResponseNotFound,HttpResponseServerError


def get_query(request):

    page = {}
    query = {}
    return {
        "query": query,
        "page": page
    }

def assistant_query(request):
    query_info = get_query(request)

    result = api_assistant.list_assistant()

    if result.is_error():
        return HttpResponseServerError()

    assistant_list = result.result()["result"]

    context = {
        "menu": "person",
        "url": "/assistant/",
        "page": {},
        "query": query_info["query"],
        "queryString": views_tools.getQueryString(query_info["query"]),
        "assistant_list": assistant_list
    }

    return context

def assistant(request):
    context = assistant_query(request)

    return render(request,'admin/assistant.html',context)

def assistant_start(request):

    assistant_id = views_tools.get_param_by_request(request.GET, "id", "")

    result = api_assistant.start(assistant_id)
    if result.is_error():
        return HttpResponseServerError()

    context = assistant_query(request)
    return render(request,'admin/assistant.html',context)

def assistant_stop(request):

    assistant_id = views_tools.get_param_by_request(request.GET, "id", "")
    result = api_assistant.stop(assistant_id)
    if result.is_error():
        return HttpResponseServerError()

    context = assistant_query(request)
    return render(request, 'admin/assistant.html', context)

def assistant_add(request):
    context = {
        "menu": "person"
    }
    return render(request,'admin/assistant_add.html',context)

@csrf_exempt
def assistant_add_do(request):

    name = views_tools.get_param_by_request(request.POST, "name", "")
    phone = views_tools.get_param_by_request(request.POST, "phone", "")
    qq = views_tools.get_param_by_request(request.POST, "qq", "")

    result = api_assistant.add(name,phone,qq)
    return views_tools.success_json()

def assistant_update(request):

    assistant_id = views_tools.get_param_by_request(request.GET, "id")
    result = api_assistant.get_assistant_by_id(assistant_id)

    if result.is_error():
        return HttpResponseServerError()

    assistant_info = result.result()
    if assistant_info == None:
        return HttpResponseServerError()

    context = {
        "menu": "person",
        "assistant": assistant_info
    }
    return render(request,'admin/assistant_update.html',context)

@csrf_exempt
def assistant_update_do(request):

    assistant_id = views_tools.get_param_by_request(request.POST, "id", "")
    name = views_tools.get_param_by_request(request.POST, "name", "")
    phone = views_tools.get_param_by_request(request.POST, "phone", "")
    qq = views_tools.get_param_by_request(request.POST, "qq", "")

    result = api_assistant.update(assistant_id,name,phone,qq)
    return views_tools.success_json()
