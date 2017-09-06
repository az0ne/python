# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.career import career as api_career
from django.http import HttpResponseNotFound,HttpResponseServerError


def land_query(request):
    query = get_query(request)

    skip = views_tools.get_skip(query['page']['pageIndex'],query['page']['pageSize'])
    result = api_career.list_land(query['query']['name'],skip)

    result_dict = result.result()
    rows_count = result_dict['rows_count']

    page = views_tools.get_page(query["page"]["pageIndex"],
                                query["page"]["pageSize"],
                                rows_count)

    context = {
        "land_list":result.result()['info'],
        'page':page,
        "menu":"career",
        "url":"/author/"
    }

    return context

def get_query(request):
    page_size = views_tools.get_param_by_request(request.GET, "pageSize", 10, int)
    page_index = views_tools.get_param_by_request(request.GET, "pageIndex" ,1, int)
    name = views_tools.get_param_by_request(request.GET, "name", "")

    page = {
    "pageSize":page_size,
    "pageIndex":page_index
    }
    query = {
    "name":name
    }

    return {"page":page,"query":query}

""" 职业课程 """
# def land_page(request):
#     name = views_tools.get_param_by_request(request.GET,"name","")
#     page = api_career.land_page(name)
#
#     if page.is_error():
#         return HttpResponseServerError
#
#     page_count = page.result()
#     rowsCount = page_count['count(id)']
#     page_size = int(views_tools.get_param_by_request(request.GET,'pageSize',10))
#     pageCount = rowsCount/page_size + 1
#     pageIndex = int(views_tools.get_param_by_request(request.GET,'pageIndex',1))
#     page1 = (pageIndex-1)*page_size
#     page2 = pageIndex*page_size
#
#     page_dict = {}
#     page_dict.update({
#         'rowsCount':rowsCount,
#         'pageCount':pageCount,
#         'pageIndex':pageIndex,
#         'page1':page1,
#         'page2':page2
#     })
#
#     return page_dict
#
# def land_query(request):
#     name = views_tools.get_param_by_request(request.GET,"name","")
#     page = land_page(request)
#     result = api_career.list_land(name,page['page1'], page['page2'])
#     land_list = result.result()
#     if result.is_error():
#         return HttpResponseServerError()
#
#     context = {
#     'url':'/land/',
#     'page':page,
#     'menu':'career',
#     "name":name,
#     'land_list':land_list
#     }
#
#     return context

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
    # 'url':'/career/land/update/'
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

def land_course(request):
    land_id = views_tools.get_param_by_request(request.GET, "land_id", "")

    result = api_career.get_course_for_land(land_id)
    courses = result.result()

    context = {
    "menu":"career",
    "courses":courses,
    "land_id":land_id
    }

    return render(request, "admin/career/land_course.html", context)

def land_course_add(request):
    land_id = views_tools.get_param_by_request(request.GET, "land_id", "")

    context = {
    "land_id":land_id,
    "menu":"career"
    }
    return render(request, "admin/career/land_course_add.html", context)

    # result = api_career.add_course_for_land(land_id)
    #
    # if result.is_error():
    #     return HttpResponseServerError
    #
    # return views_tools.success_json()

@csrf_exempt
def land_course_add_do(request):
    land_id = views_tools.get_param_by_request(request.POST,"land_id", "")
    course_id = views_tools.get_param_by_request(request.POST, "course_id", "")

    result = api_career.land_course_add(land_id, course_id)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()

def land_course_update(request):
    land_id = views_tools.get_param_by_request(request.GET, "land_id", "")
    course_id = views_tools.get_param_by_request(request.GET, "course_id", "")

    pass

@csrf_exempt
def land_course_update_do(request):
    pass
