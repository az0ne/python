# -*- coding: utf-8 -*-

import traceback
from django.http.response import JsonResponse
from django.shortcuts import render
from django.conf import settings
from maiziserver.utils.logger import logger as log


def get_param_by_request(request, param_name, default_val=None, _type=None):

    try:
        if param_name in request:
            _val = request[param_name]
        else:
            _val = default_val
        if _type:
            _val = _type(_val)
        return _val
    except Exception as e:
        # log.warn("get param failed, %s" % e)
        return default_val

def success_json(code = 200, message='',data={}):
    result = dict(
        code = code,
        success=True,
        message=message,
        data=data
    )
    return JsonResponse(result)


def failed_json(code = 500, message='', data={}):
    result = dict(
        code=code,
        success=False,
        message=message,
        data=data
    )

    return JsonResponse(result)

def get_session(request):
    if(request.session.get("user_id") != None and request.session.get("user_name") != None):
        return {"user_id":request.session.get("user_id"), "user_name": request.session.get("user_name")}
    return None


def get_user_info(request):
    user_info = get_session(request)
    if(user_info == None):
        if(need_auto_login(request)):
            request.session["user_id"] = request.COOKIES["user_id"]
            request.session["user_name"] = request.COOKIES["user_name"]
            request.session["password"] = request.COOKIES["password"]
            return get_session(request)
    return user_info

def get_skip(pageIndex,pageSize):

    return {
        "limit": (pageIndex - 1) * pageSize,
        "offset": pageSize
    }

def get_page(pageIndex,pageSize,rowsCount):
    startIndex = 0
    endIndex = 0
    if rowsCount % pageSize == 0:
        pageCount = rowsCount / pageSize
    else:
        pageCount = rowsCount / pageSize + 1

    startIndex = (pageIndex - 1) * pageSize
    endIndex = startIndex + pageSize - 1

    return {
        "startIndex": startIndex,
        "endIndex": endIndex,
        "pageIndex": pageIndex,
        "pageSize": pageSize,
        "rowsCount": rowsCount,
        "pageCount": pageCount
    }

def getQueryString(query):
    queryString = ""
    for key in query:
        queryString += key + "=" + query[key] + "&"
    return queryString[0:len(queryString) - 1]


def catch_views_exception(func):

    def _func(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception as e:
            if settings.DEBUG:
                traceback.print_exc()

            log.warn("views except. detail: %s" % e)
            return render(request,'500.html', {}, status=500)

    return _func

def catch_ajax_exception(func):

    def _func(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception as e:
            if settings.DEBUG:
                traceback.print_exc()

            log.warn("views except. detail: %s" % e)
            return failed_json()

    return _func
