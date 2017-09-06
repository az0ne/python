# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.career import book as api_book
from django.http import HttpResponseNotFound,HttpResponseServerError
from maiziserver.settings.local import UPLOAD_DOCUMENT_DIRS


def book(request):
    context = book_query(request)

    return render(request, "admin/career/book.html",context)

def book_query(request):
    query = get_query(request)

    skip = views_tools.get_skip(query['page']['pageIndex'],
                                query['page']['pageSize'])
    result = api_book.list_book(query['query']['name'],skip)
    result_dict = result.result()

    rowsCount = result_dict['rowsCount']

    page = views_tools.get_page(query['page']['pageIndex'],
                                query['page']['pageSize'],
                                rowsCount)

    context = {
        "books":result_dict['books'],
        "name":query['query']['name'],
        'page':page,
        "menu":"career",
        "url":"/book/"
    }

    return context

def get_query(request):
    pageSize = views_tools.get_param_by_request(request.GET,
                                                "pageSize", 10, int)
    pageIndex = views_tools.get_param_by_request(request.GET,
                                                "pageIndex", 1, int)
    name = views_tools.get_param_by_request(request.GET, "name", "")

    page = {
        "pageSize":pageSize,
        "pageIndex":pageIndex
    }

    query = {
        "name":name
    }

    return {"page":page,"query":query}

def book_add(request):
    context = {
        "menu":"career",
    }

    return render(request, "admin/career/book_add.html", context)

@csrf_exempt
def book_add_do(request):
    book_name = views_tools.get_param_by_request(request.POST, "name", "")
    book_description = views_tools.get_param_by_request(request.POST,
                                                        "description", "")
    book_author = views_tools.get_param_by_request(request.POST,
                                                    "book_author", "")
    book_pic = views_tools.get_param_by_request(request.POST, "url", "")

    result = api_book.add_book(book_name, book_author,
                            book_description, book_pic)

    if result.is_error():

        return HttpResponseServerError

    return views_tools.success_json()
