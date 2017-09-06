#! /usr/bin/evn python
# -*- coding:utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import render
from utils.tool import get_param_by_request
from db.api.common import userProfile
from utils.logger import logger as log
from utils.handle_exception import handle_http_response_exception
from utils.decorators import dec_login_required


@dec_login_required
@handle_http_response_exception(501)
def get_login_statistical_num(request):
    start_date = get_param_by_request(request.GET, "start_date", "", _type=str)
    end_date = get_param_by_request(request.GET, "end_date", "", _type=str)
    if start_date and end_date:
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        APIResult = userProfile.get_statistical(start_date, end_date)
        if APIResult.is_error():
            log.warn("get last_login and date_joined failed .")
            return render(request, "404.html", dict())
        result = APIResult.result()
        return JsonResponse(dict(status="success", result=result))
    return JsonResponse(dict(status="failed", result=None))


@dec_login_required
@handle_http_response_exception(501)
def login_statistical(request):
    return render(request, "mz_common/login_statistical.html")
