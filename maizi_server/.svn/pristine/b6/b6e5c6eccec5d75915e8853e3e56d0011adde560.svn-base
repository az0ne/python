# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.career import author as api_author
from django.http import HttpResponseNotFound,HttpResponseServerError
from maiziserver.settings.local import UPLOAD_DOCUMENT_DIRS

def author(request):
    context = author_query(request)

    return render(request, "admin/career/author.html",context)

def author_add(request):

    context = {
    "menu":"career",
    "url":"/author/add/"
    }

    return render(request,"admin/career/author_add.html",context)

@csrf_exempt
def author_add_do(request):

    name = views_tools.get_param_by_request(request.POST,"name","")
    info = views_tools.get_param_by_request(request.POST,"info","")
    fileName = views_tools.get_param_by_request(request.POST,"fileName","")
    fileExtension = views_tools.get_param_by_request(request.POST,"fileExtension","")

    head_url = UPLOAD_DOCUMENT_DIRS+fileName

    result = api_author.add_author(name,head_url,info)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()

def author_update(request):
    author_id = views_tools.get_param_by_request(request.GET,"author_id","")
    result = api_author.get_author_by_id(author_id)
    author = result.result()

    context = {
    "menu":"career",
    "author":author
    }

    return render(request,"admin/career/author_update.html",context)

@csrf_exempt
def author_update_do(request):
    author_id = views_tools.get_param_by_request(request.POST,"author_id","")
    name = views_tools.get_param_by_request(request.POST,"name","")
    info = views_tools.get_param_by_request(request.POST,"info","")
    file_name = views_tools.get_param_by_request(request.POST,"fileName")

    head_url = UPLOAD_DOCUMENT_DIRS+file_name

    result = api_author.update_author(author_id,name,head_url,info)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()

def author_query(request):
    query = get_query(request)

    skip = views_tools.get_skip(query['page']['pageIndex'],query['page']['pageSize'])
    result = api_author.list_author(query['query']['name'],skip)

    result_dict = result.result()
    rows_count = result_dict['rowsCount']

    page = views_tools.get_page(query["page"]["pageIndex"],
                                query["page"]["pageSize"],
                                rows_count)

    context = {
        "authors":result.result()['info'],
        'name':query['query']['name'],
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
