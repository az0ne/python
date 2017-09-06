# -*- coding:utf-8 -*-

from utils.decorators import dec_login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from db.api.mngteacher import employ_teacher as api_employteacher
from utils import tool
from utils.handle_exception import handle_http_response_exception


WORK_TIME = {
    1: '3年以下',
    2: '3至5年',
    3: '5至8年',
    4: '8年以上',
}


@dec_login_required
@handle_http_response_exception(501)
def employ_teacher(request):
    '''

    :param request:
    :return:
    '''
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "",str)
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        employteacher = api_employteacher.delete_employteacher_by_id(_id)
        if employteacher.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

    if action == "search":
        if key_word == "%":
            key_word1 = '//'+key_word
        else:
            key_word1 = key_word
        employteacher = api_employteacher.list_employteacher_by_resume('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)
    else:
        employteacher = api_employteacher.list_employteacher_by_page(page_index, settings.PAGE_SIZE)

    if employteacher.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    employteachers = employteacher.result()["result"]

    for e in employteachers:
        e['work_time_display'] = WORK_TIME.get(e['work_time'], 'N/A')

    c = {"employteachers": employteachers,
         "page": {"page_index": page_index, "rows_count": employteacher.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": employteacher.result()["page_count"]}}
    return render_to_response("mz_back/employteacher_list.html", c, context_instance=RequestContext(request))




# 查看
@dec_login_required
@handle_http_response_exception(501)
def employ_teacher_edit(request):
    action = tool.get_param_by_request(request.GET, 'action', "show", str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    employteacher = None
    if action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        employteacher = api_employteacher.get_employteacher_by_id(_id)
        if employteacher.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    employteacher = employteacher.result()
    employteacher['work_time_display'] = WORK_TIME.get(employteacher['work_time'], 'N/A')
    c = {"employteachers": employteacher, "action": action, "page_index": str(page_index)}
    return render_to_response("mz_back/employteacher_add.html", c, context_instance=RequestContext(request))
