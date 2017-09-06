# -*- coding: utf-8 -*-

import datetime
from django.shortcuts import render
# from django.http import HttpResponseRedirect, JsonResponse
# from django.core.urlresolvers import reverse

from db.api.major import item as api_item

# from utils.decorators import dec_login_required
# from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
# from utils.logger import logger as log
# from myproject import settings
from utils.json_response import success_json, failed_json


# @dec_login_required
# @handle_http_response_exception(501)

# item添加
def add_item(request):
    item_name = get_param_by_request(request.GET, 'item_name', "", str)
    course_id = get_param_by_request(request.GET, 'course_id', "", int)
    knowledge_id = get_param_by_request(request.GET, 'knowledge_id', "", int)
    item_state = get_param_by_request(request.GET, 'item_state', "", int)
    sequence = get_param_by_request(request.GET, 'sequence', "", int)
    item_type = get_param_by_request(request.GET, 'item_type', "", int)
    resource_id = get_param_by_request(request.GET, 'resource_ids', "", int)

    item = api_item.add_item(item_name,
                             course_id,
                             knowledge_id,
                             item_state,
                             sequence,
                             item_type,
                             resource_id)

    if item.is_error():
        return failed_json()
    return success_json()


# item通过course_id查询
def get_item(request):
    id = get_param_by_request(request.GET, 'id', "", int)
    print id
    item = api_item.get_item(id)

    if item.is_error():
        return failed_json()
    return success_json()


# item修改
def update_item(request):
    id = get_param_by_request(request.GET, 'id', "", int)
    item_name = get_param_by_request(request.GET, 'item_name', "", str)
    course_id = get_param_by_request(request.GET, 'course_id', "", int)
    knowledge_id = get_param_by_request(request.GET, 'knowledge_id', "", int)
    item_state = get_param_by_request(request.GET, 'item_state', "", int)
    sequence = get_param_by_request(request.GET, 'sequence', "", int)
    item_type = get_param_by_request(request.GET, 'item_type', "", int)
    resource_id = get_param_by_request(request.GET, 'resource_ids', "", int)

    print id, item_name, course_id, knowledge_id, item_state, sequence, item_type, resource_id
    item = api_item.update_item(id,
                                item_name,
                                course_id,
                                knowledge_id,
                                item_state,
                                sequence,
                                item_type,
                                resource_id)

    if item.is_error():
        return failed_json()
    return success_json()
