# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.career import career as api_career
from django.http import HttpResponseNotFound,HttpResponseServerError


def get_query(request):

    page = {}
    query = {}
    return {
        "query": query,
        "page": page
    }

def career_query(request):
    query_info = get_query(request)

    result = api_career.list_career()

    if result.is_error():
        return HttpResponseServerError()

    career_list = result.result()["result"]

    context = {
        "menu":"career",
        "url": "/career/",
        "page": {},
        "query": query_info["query"],
        "queryString": views_tools.getQueryString(query_info["query"]),
        "career_list": career_list
    }

    return context

def career(request):
    context = career_query(request)

    return render(request,'admin/career/career.html',context)

def career_start(request):

    career_id = views_tools.get_param_by_request(request.GET, "id", "")

    result = api_career.start(career_id)
    if result.is_error():
        return HttpResponseServerError()

    context = career_query(request)
    return render(request,'admin/career/career.html',context)

def career_stop(request):

    career_id = views_tools.get_param_by_request(request.GET, "id", "")
    result = api_career.stop(career_id)
    if result.is_error():
        return HttpResponseServerError()

    context = career_query(request)
    return render(request, 'admin/career/career.html', context)

def career_add(request):
    context = {
        "menu": "career"
    }
    return render(request,'admin/career/career_add.html',context)

@csrf_exempt
def career_add_do(request):

    name = views_tools.get_param_by_request(request.POST, "name", "")
    type = views_tools.get_param_by_request(request.POST, "type", "0")
    remark = views_tools.get_param_by_request(request.POST, "remark", "")

    result = api_career.add(name,type,remark)
    return views_tools.success_json()

def career_update(request):

    career_id = views_tools.get_param_by_request(request.GET, "id")
    result = api_career.get_career_by_id(career_id)

    if result.is_error():
        return HttpResponseServerError()

    career_info = result.result()
    if career_info == None:
        return HttpResponseServerError()

    context = {
        "menu": "career",
        "career": career_info
    }
    return render(request,'admin/career/career_update.html',context)

@csrf_exempt
def career_update_do(request):

    career_id = views_tools.get_param_by_request(request.POST, "id", "")
    name = views_tools.get_param_by_request(request.POST, "name", "")
    type = views_tools.get_param_by_request(request.POST, "type", "")
    remark = views_tools.get_param_by_request(request.POST, "remark", "")

    result = api_career.update(career_id,name,type,remark)
    return views_tools.success_json()


"""edit by zyf on 05/08/2017"""

""" 职业课程 """
def land_page(request):
    name = views_tools.get_param_by_request(request.GET,"name","")
    page = api_career.land_page(name)

    if page.is_error():
        return HttpResponseServerError

    page_count = page.result()
    rowsCount = page_count['count(id)']
    page_size = int(views_tools.get_param_by_request(request.GET,'pageSize',10))
    pageCount = rowsCount/page_size + 1
    pageIndex = int(views_tools.get_param_by_request(request.GET,'pageIndex',1))
    page1 = (pageIndex-1)*page_size
    page2 = pageIndex*page_size

    page_dict = {}
    page_dict.update({
        'rowsCount':rowsCount,
        'pageCount':pageCount,
        'pageIndex':pageIndex,
        'page1':page1,
        'page2':page2
    })

    return page_dict

def land_query(request):
    name = views_tools.get_param_by_request(request.GET,"name","")
    page = land_page(request)
    result = api_career.list_land(name,page['page1'], page['page2'])
    land_list = result.result()
    if result.is_error():
        return HttpResponseServerError()

    context = {
    'url':'/land/',
    'page':page,
    'menu':'career',
    "name":name,
    'land_list':land_list
    }

    return context

def land(request):
    context = land_query(request)

    return render(request,'admin/career/land.html',context)

def land_add(request):
    context = {'menu':'career'}

    return render(request,'admin/career/land_add.html',context)

@csrf_exempt
def land_add_do(request):

    name = views_tools.get_param_by_request(request.POST, 'name', '')
    remark = views_tools.get_param_by_request(request.POST, 'remark', '')
    # state = views_tools.get_param_by_request(request.POST, 'state', '')

    result = api_career.land_add(name,remark)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()

def land_update(request):

    id = views_tools.get_param_by_request(request.GET, 'land_id', '')
    result = api_career.get_land_by_id(id)
    land = result.result()

    context = {
    'menu':'career',
    'land':land,
    'url':'/land/update/'
    }

    return render(request, 'admin/career/land_update.html',context)

@csrf_exempt
def land_update_do(request):
    # print '1'*100
    name = views_tools.get_param_by_request(request.POST, 'name', '')
    remark = views_tools.get_param_by_request(request.POST, 'remark', '')
    land_id = views_tools.get_param_by_request(request.POST, 'land_id', '')

    result = api_career.land_update(land_id,name,remark)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()

def land_state(request):
    land_id = views_tools.get_param_by_request(request.GET, "land_id", "")
    state = views_tools.get_param_by_request(request.GET, "state", "")

    result = api_career.set_land_state(land_id,state)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()
