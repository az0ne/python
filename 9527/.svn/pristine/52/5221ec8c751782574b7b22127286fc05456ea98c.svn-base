# -*- coding: utf-8 -*-

import datetime
from django.shortcuts import render
# from django.http import HttpResponseRedirect, JsonResponse
# from django.core.urlresolvers import reverse

from db.api.major import major as api_major

# from utils.decorators import dec_login_required
# from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
# from utils.logger import logger as log
# from myproject import settings
from utils.json_response import success_json, failed_json


# @dec_login_required
# @handle_http_response_exception(501)

# 专业课程添加
def add_major(request):
    major_name = get_param_by_request(request.GET, 'major_name', "", str)
    major_state = get_param_by_request(request.GET, 'major_state', "", int)
    major_price = get_param_by_request(request.GET, 'major_price', "", int)

    major = api_major.add_major(major_name, major_state, major_price)

    if major.is_error():
        return failed_json()
    return success_json()


# 专业课程通过name查询
def get_major(request):
    id = get_param_by_request(request.GET, 'id', "", int)

    major = api_major.get_major(id)

    if major.is_error():
        return failed_json()
    return success_json()


# 小课程修改
def update_major(request):
    id = get_param_by_request(request.GET, 'id', "", int)
    major_name = get_param_by_request(request.GET, 'major_name', "", str)
    major_state = get_param_by_request(request.GET, 'major_state', "", int)
    major_price = get_param_by_request(request.GET, 'major_price', "", int)

    major = api_major.update_major(id, major_name, major_state, major_price)

    if major.is_error():
        return failed_json()
    return success_json()
