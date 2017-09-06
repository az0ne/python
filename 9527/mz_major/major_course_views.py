# -*- coding: utf-8 -*-

# import datetime
# from django.shortcuts import render
# from django.http import HttpResponseRedirect, JsonResponse
# from django.core.urlresolvers import reverse

from db.api.major import major_course as api_major_course

# from utils.decorators import dec_login_required
# from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
# from utils.logger import logger as log
# from myproject import settings
from utils.json_response import success_json, failed_json


# @dec_login_required
# @handle_http_response_exception(501)

# 专业课程和小课程表的关联表添加
def add_major_course(request):
    # major_id = get_param_by_request(request.GET, 'major_id', "", int)
    # course_id = get_param_by_request(request.GET, 'course_id', "", int)
    # major_course = api_major_course.add_major_course(major_id, course_id)
    #
    # if major_course.is_error():
    #     return failed_json()
    # return success_json()
    print "*********************"

# 专业课程和小课程表的关联表查询
def get_major_course(request):
    id = get_param_by_request(request.GET, 'id', "", int)

    major_course = api_major_course.get_major_course(id)

    if major_course.is_error():
        return failed_json()
    return success_json()


# 专业课程和小课程表的关联表修改
def update_major_course(request):
    id = get_param_by_request(request.GET, 'id', "", int)
    major_id = get_param_by_request(request.GET, 'major_id', "", int)
    course_id = get_param_by_request(request.GET, 'course_id', "", int)

    major_course = api_major_course.update_major_course(id, major_id, course_id)

    if major_course.is_error():
        return failed_json()
    return success_json()
