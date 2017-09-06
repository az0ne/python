# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.career import vedio as api_career
from maiziserver.db.api.career import project as api_project
from django.http import HttpResponseNotFound,HttpResponseServerError

def vedio_list(request):
    query = get_query(request)

    skip = views_tools.get_skip(query['page']['pageIndex'],query['page']['pageSize'])
    result = api_career.list_vedio(query['query']['name'],skip)

    result_dict = result.result()

    rows_count = result_dict['rows_count']
    print rows_count

    page = views_tools.get_page(query["page"]["pageIndex"],
                                query["page"]["pageSize"],
                                rows_count)

    context = {
        "vedios":result.result()['info'],
        'page':page,
        "menu":"career",
        "url":"/course/"
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

#视频
def vedio(request):
    context = vedio_list(request)
    # context = {}

    return render(request,"admin/career/vedio.html",context)

# def vedio_list(request):
#     page_dict = vedio_page(request)
#     page1 = page_dict['page1']
#     page2 = page_dict['page2']
#
#     result = api_career.list_vedio(page1,page2)
#     vedios = result.result()
#     context = {
#     "menu":"career",
#     "url":"/vedio/",
#     "page":page_dict,
#     "vedios":vedios
#     }
#     # print context
#     return context
#
# def vedio_page(request):
#     result = api_career.page_vedio()
#     rowsCount = result.result()['count(id)']
#     page_dict = handle_page(rowsCount,request)
#
#     return page_dict

def handle_page(rowsCount,request):

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

    # return page_dict

def item_vedio(request):
    item_id = views_tools.get_param_by_request(request.GET,"item_id","")
    item_type = views_tools.get_param_by_request(request.GET,"item_type","")
    resource_id = views_tools.get_param_by_request(request.GET,'resource_id','')

    if item_type == u"视频":
        item_type = 1
        result = api_career.get_vedio(resource_id)
        vedio = result.result()

        context = {
        "menu":"career",
        "url":"/item/vedio/",
        "vedio":vedio,
        "item_id":item_id
        }

        return render(request,"admin/career/item_vedio.html",context)
    else:
        item_type = 0

        result = api_project.get_project(resource_id)
        project = result.result()

        context = {
        "menu":"career",
        "url":"/item/vedio/",
        "project":project,
        "item_id":item_id
        }

        return render(request,"admin/career/item_project.html",context)


def item_vedio_add(request):
    vedio_id = views_tools.get_param_by_request(request.GET,"vedio_id","")
    item_id = views_tools.get_param_by_request(request.GET,"item_id","")

    context = {
    "menu":"career",
    "vedio_id":vedio_id,
    "item_id":item_id
    }

    return render(request,"admin/career/item_vedio_add.html",context)

@csrf_exempt
def item_vedio_add_do(request):
    url = views_tools.get_param_by_request(request.POST,"url","")
    item_id = views_tools.get_param_by_request(request.POST,"item_id","")
    name = views_tools.get_param_by_request(request.POST, "name","")
    result = api_career.vedio_add(url,name,item_id)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()


def item_vedio_update(request):
    item_id = views_tools.get_param_by_request(request.GET,"item_id","")
    vedio_id = views_tools.get_param_by_request(request.GET,"vedio_id","")
    # name = views_tools.get_param_by_request(request.GET, "name","")
    result = api_career.get_vedio(vedio_id)
    vedio = result.result()

    context = {
    "menu":"career",
    "item_id":item_id,
    "vedio_id":vedio_id,
    "vedio":vedio,

    }

    return render(request,"admin/career/item_vedio_update.html",context)


@csrf_exempt
def item_vedio_update_do(request):
    item_id = views_tools.get_param_by_request(request.POST,"item_id","")
    vedio_id = views_tools.get_param_by_request(request.POST,"vedio_id","")
    name = views_tools.get_param_by_request(request.POST,"name","")
    url = views_tools.get_param_by_request(request.POST,"url","")

    result = api_career.update_vedio(vedio_id,name,url)
    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()
