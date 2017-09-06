# -*- coding: utf-8 -*-

import datetime
from django.shortcuts import render
# from django.http import HttpResponseRedirect, JsonResponse
# from django.core.urlresolvers import reverse

from db.api.major import knowledge as api_knowledge

# from utils.decorators import dec_login_required
# from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
# from utils.logger import logger as log
# from myproject import settings
from utils.json_response import success_json, failed_json


# @dec_login_required
# @handle_http_response_exception(501)

# 专业课程添加
def add_knowledge(request):
    knowledge_name = get_param_by_request(request.GET, 'knowledge_name', "", str)
    course_id = get_param_by_request(request.GET, 'course_id', "", int)
    sequence = get_param_by_request(request.GET, 'sequence', "", int)
    knowledge_state = get_param_by_request(request.GET, 'knowledge_state', "", int)

    knowledge = api_knowledge.add_knowledge(knowledge_name, course_id, sequence, knowledge_state)

    if knowledge.is_error():
        return failed_json()
    return success_json()


# 专业课程通过name查询
def get_knowledge(request):
    id = get_param_by_request(request.GET, 'id', "", int)

    knowledge = api_knowledge.get_knowledge(id)

    if knowledge.is_error():
        return failed_json()
    return success_json()


# 小课程修改
def update_knowledge(request):

    id = get_param_by_request(request.GET, 'id', "", int)
    knowledge_name = get_param_by_request(request.GET, 'knowledge_name', "", str)
    course_id = get_param_by_request(request.GET, 'course_id', "", int)
    sequence = get_param_by_request(request.GET, 'sequence', "", int)
    knowledge_state = get_param_by_request(request.GET, 'knowledge_state', "", int)

    knowledge = api_knowledge.update_knowledge(id,
                                               knowledge_name,
                                               course_id,
                                               sequence,
                                               knowledge_state)

    if knowledge.is_error():
        return failed_json()
    return success_json()
