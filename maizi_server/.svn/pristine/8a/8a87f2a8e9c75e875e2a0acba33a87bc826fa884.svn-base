# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.career import item as api_item
from django.http import HttpResponseNotFound,HttpResponseServerError


def item_query(request):
    query = get_query(request)

    skip = views_tools.get_skip(query['page']['pageIndex'],query['page']['pageSize'])
    result = api_item.item_list(query['query']['name'],skip)

    result_dict = result.result()

    rows_count = result_dict['rows_count']
    print rows_count

    page = views_tools.get_page(query["page"]["pageIndex"],
                                query["page"]["pageSize"],
                                rows_count)

    context = {
        "items":result.result()['info'],
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

def item(request):
    context = item_query(request)

    return render(request,"admin/career/item.html",context)


def course_knowledge_item_page(request):
    name = views_tools.get_param_by_request(request.GET,"name","")
    result = api_item.item_page(name)
    rowsCount = result.result()['count(id)']
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

def course_knowledge_item_query(request):
    # page_dict = course_knowledge_item_page(request)
    # page1 = page_dict['page1']
    # page2 = page_dict['page2']

    name = views_tools.get_param_by_request(request.GET,"name","")
    course_id = views_tools.get_param_by_request(request.GET,"course_id","")
    knowledge_id = views_tools.get_param_by_request(request.GET,"knowledge_id","")
    result = api_item.item_list_for_course(name,knowledge_id,course_id)
    items = result.result()

    context = {
    "menu":"career",
    "url":"/course/knowledge/item/",
    "items":items,
    # "page":page_dict
    }

    return context

def course_knowledge_item(request):
    context = course_knowledge_item_query(request)

    return render(request,"admin/career/course_knowledge_item.html",context)

def course_knowledge_item_update(request):
    item_id = views_tools.get_param_by_request(request.GET,"item_id","")
    course_id = views_tools.get_param_by_request(request.GET,"course_id","")
    knowledge_id = views_tools.get_param_by_request(request.GET,"knowledge_id","")

    result = api_item.get_item_by_knowledge_id(item_id,knowledge_id,course_id)
    item = result.result()

    context = {
    "menu":"career",
    "item":item
    }

    return render(request,"admin/career/course_knowledge_item_update.html",context)

@csrf_exempt
def course_knowledge_item_update_do(request):
    item_id = views_tools.get_param_by_request(request.POST,"item_id","")
    knowledge_id = views_tools.get_param_by_request(request.POST,"knowledge_id","")
    course_id = views_tools.get_param_by_request(request.POST,"course_id","")
    item_name = views_tools.get_param_by_request(request.POST,"item_name","")
    item_order_index = views_tools.get_param_by_request(request.POST,"item_order_index","")
    # item_type = views_tools.get_param_by_request(request.POST,"item_type","")

    result = api_item.update_item(item_name,item_order_index,item_id,knowledge_id,course_id)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()

def course_knowledge_item_add(request):
    course_id = views_tools.get_param_by_request(request.GET,"course_id","")
    knowledge_id = views_tools.get_param_by_request(request.GET,"knowledge_id","")

    context = {
    "menu":"career",
    "course_id":course_id,
    "knowledge_id":knowledge_id
    }

    return render(request,"admin/career/course_knowledge_item_add.html",context)

@csrf_exempt
def course_knowledge_item_add_do(request):
    course_id = views_tools.get_param_by_request(request.POST, "course_id", "")
    knowledge_id = views_tools.get_param_by_request(request.POST, "knowledge_id", "")
    item_name = views_tools.get_param_by_request(request.POST, "item_name", "")
    item_type = views_tools.get_param_by_request(request.POST, "item_type", "")
    order_index = views_tools.get_param_by_request(request.POST, "order_index", "")


    result = api_item.add_item(item_name,item_type,order_index,knowledge_id,course_id)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()

def course_knowledge_item_set(request):
    knowledge_id = views_tools.get_param_by_request(request.GET,"knowledge_id","")
    course_id = views_tools.get_param_by_request(request.GET,"course_id","")
    item_id = views_tools.get_param_by_request(request.GET,"item_id","")
    state = views_tools.get_param_by_request(request.GET,"state","")
    # print "*"*100
    # print state
    # print "*"*100
    result = api_item.set_item_state(course_id,knowledge_id,item_id,state)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()
