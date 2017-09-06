# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.career import knowledge as api_knowledge
from django.http import HttpResponseNotFound,HttpResponseServerError


def knowledge_query(request):
    query = get_query(request)

    skip = views_tools.get_skip(query['page']['pageIndex'],query['page']['pageSize'])
    result = api_knowledge.knowledge_list(query['query']['name'],skip)

    result_dict = result.result()

    rows_count = result_dict['rows_count']


    page = views_tools.get_page(query["page"]["pageIndex"],
                                query["page"]["pageSize"],
                                rows_count)

    context = {
        "knowledge_list":result.result()['info'],
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

def knowledge(request):
    context = knowledge_query(request)

    return render(request, 'admin/career/knowledge.html', context)

def course_knowledge_query(request):

    # page_dict = course_knowledge_page(request)
    # page1 = page_dict['page1']
    # page2 = page_dict['page2']

    course_id = views_tools.get_param_by_request(request.GET,'course_id','')
    result = api_knowledge.get_course_knowledge(course_id)
    knowledges = result.result()

    context = {
    'menu':'career',
    # 'page':page_dict,
    'knowledges':knowledges,
    'url':'/knowledge/'
    }

    return context

def course_knowledge(request):
    context = course_knowledge_query(request)

    return render(request, "admin/career/course_knowledge.html",context)

def course_knowledge_add(request):
    course_id = views_tools.get_param_by_request(request.GET,'course_id','')

    context = {
    'menu':'career',
    'course_id':course_id
    }

    return render(request,'admin/career/course_knowledge_add.html',context)

@csrf_exempt
def course_knowledge_add_do(request):

    course_id = views_tools.get_param_by_request(request.POST,"course_id","")
    knowledge_name = views_tools.get_param_by_request(request.POST,"knowledge_name","")
    knowledge_order_index = views_tools.get_param_by_request(request.POST,"knowledge_order_index","")
    # knowledge_url = views_tools.get_param_by_request(request.POST,"knowledge_url","")

    result = api_knowledge.course_knowledge_add(knowledge_name,course_id,knowledge_order_index)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()

def course_knowledge_update(request):
    knowledge_id = views_tools.get_param_by_request(request.GET,'knowledge_id','')
    result = api_knowledge.get_knowledge_by_id(knowledge_id)
    knowledge = result.result()

    context = {
    "menu":"career",
    "knowledge":knowledge,
    }

    return render(request,"admin/career/course_knowledge_update.html",context)

@csrf_exempt
def course_knowledge_update_do(request):
    course_id = views_tools.get_param_by_request(request.POST,"course_id","")
    knowledge_id = views_tools.get_param_by_request(request.POST,"knowledge_id","")
    knowledge_name = views_tools.get_param_by_request(request.POST,"knowledge_name","")
    knowledge_order_index = views_tools.get_param_by_request(request.POST,"knowledge_order_index","")

    result = api_knowledge.course_knowledge_update(knowledge_name,knowledge_order_index,knowledge_id)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()

def course_knowledge_set(request):
    knowledge_id = views_tools.get_param_by_request(request.GET,"knowledge_id","")
    state = views_tools.get_param_by_request(request.GET,"state","")

    result = api_knowledge.course_knowledge_state_set(knowledge_id,state)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()
