# -*- coding: utf-8 -*-

import datetime
from django.shortcuts import render
# from django.http import HttpResponseRedirect, JsonResponse
# from django.core.urlresolvers import reverse

from db.api.major import course as api_course

# from utils.decorators import dec_login_required
# from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
# from utils.logger import logger as log
# from myproject import settings
from utils.json_response import success_json, failed_json


# @dec_login_required
# @handle_http_response_exception(501)

# 小课程添加

def add_course(request):
    course_name = get_param_by_request(request.GET, 'course_name', "", str)
    author_id = get_param_by_request(request.GET, 'author_id', "", int)
    sequence = get_param_by_request(request.GET, 'sequence', "", int)
    course_state = get_param_by_request(request.GET, 'course_state', "", int)

    course = api_course.add_course(course_name, author_id, sequence, course_state)

    if course.is_error():
        return failed_json()
    return success_json()


# 小课程通过name查询
def get_course(request):

    id = get_param_by_request(request.GET, 'id', "", int)
    # course_name = get_param_by_request(request.GET, 'course_name', "", str)
    # author_id = get_param_by_request(request.GET, 'author_id', "", int)
    # sequence = get_param_by_request(request.GET, 'sequence', "", int)
    # course_state = get_param_by_request(request.GET, 'course_state', "", int)

    course = api_course.get_course(id)

    if course.is_error():
        return failed_json()
    return success_json()


# 小课程修改
def update_course(request):

    course_id = get_param_by_request(request.GET, 'course_id', "", int)
    course_name = get_param_by_request(request.GET, 'course_name', "", str)
    author_id = get_param_by_request(request.GET, 'author_id', "", int)
    sequence = get_param_by_request(request.GET, 'sequence', "", int)
    course_state = get_param_by_request(request.GET, 'course_state', "", int)

    print course_id, course_name, author_id, sequence, course_state

    course = api_course.update_course(course_id,
                                      course_name,
                                      author_id,
                                      sequence,
                                      course_state)

    if course.is_error():
        return failed_json()
    return success_json()
