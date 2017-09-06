# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.career import project as api_project
from django.http import HttpResponseNotFound,HttpResponseServerError


def project(request):
    context = project_query(request)

    return render(request, "admin/career/project.html", context)

def project_query(request):
    query = get_query(request)
    skip = views_tools.get_skip(query['page']["pageIndex"],query['page']['pageSize'])
    result = api_project.list_project(query['query']['query'], skip)

    result_dict = result.result()
    rowsCount = result_dict['rowsCount']
    page = views_tools.get_page(query["page"]["pageIndex"],
                                query["page"]["pageSize"],
                                rowsCount)

    context = {
        "projects":result.result()['info'],
        'name':query['query']['query'],
        'page':page,
        "menu":"career",
        "url":"/project/"
    }

    return context

def get_query(request):
    pageSize = views_tools.get_param_by_request(request.GET, "pageSize", 10, int)
    pageIndex = views_tools.get_param_by_request(request.GET, "pageIndex", 1, int)
    name = views_tools.get_param_by_request(request.GET, "name", "")

    page = {
    "pageSize":pageSize,
    "pageIndex":pageIndex
    }
    query = {
    "query":name
    }

    return {"page":page,"query":query}

def project_add(request):
    item_id = views_tools.get_param_by_request(request.GET, "item_id", "")
    context = {
    "item_id":item_id,
    "menu":"career"
    }
    return render(request, "admin/career/project_add.html", context)

@csrf_exempt
def project_add_do(request):
    item_id = views_tools.get_param_by_request(request.POST, "item_id", "")
    name = views_tools.get_param_by_request(request.POST, "name", "")
    url = views_tools.get_param_by_request(request.POST, "url", "")

    result = api_project.add_project(item_id,name,url)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()


def project_update(request):
    project_id = views_tools.get_param_by_request(request.GET,"project_id","")
    result = api_project.get_project_by_id(project_id)

    context = {
    "menu":"career",
    "project":result.result()
    }

    return render(request, "admin/career/project_update.html",context)

@csrf_exempt
def project_update_do(request):
    project_id = views_tools.get_param_by_request(request.POST, "project_id", "")
    url = views_tools.get_param_by_request(request.POST, "url", "")
    name = views_tools.get_param_by_request(request.POST, "name", "")

    result = api_project.update_project(url,name,project_id)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()
