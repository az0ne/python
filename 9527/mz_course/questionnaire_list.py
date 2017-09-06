# -*- coding:utf-8 -*-

from utils.decorators import dec_login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from db.api.course import questionnaire as api_questionnaire
from utils import tool
from utils.handle_exception import handle_http_response_exception
from django.http import HttpResponseRedirect
import json


@dec_login_required
@handle_http_response_exception(501)
def questionnaire_item_list(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "")
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        questionnaire = api_questionnaire.delete_questionnaire_item_by_id(_id)
        if questionnaire.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

    if action == "search":
        if key_word == "%":
            key_word1 = '//' + key_word
            questionnaire = api_questionnaire.get_questionnaire_item_by_stem('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)
        else:
            key_word1 = key_word
            questionnaire = api_questionnaire.get_questionnaire_item_by_stem('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)
    else:
        questionnaire = api_questionnaire.list_questionnaire_item_by_page(page_index, settings.PAGE_SIZE)
    if questionnaire.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    c = {"questionnaires": questionnaire.result()["result"],
         "page": {"page_index": page_index, "rows_count": questionnaire.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": questionnaire.result()["page_count"]}}
    return render_to_response("mz_course/questionnaire_item.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def questionnaire_item_add(request):
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    counttwoques_id = api_questionnaire.counttwoques_id()
    c = {"page_index": page_index,"counttwoques":counttwoques_id.result()[0]["counttwoques"],}
    return render_to_response("mz_course/questionnaire_item_add.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def questionnaire_item_save(request):
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)
    ques_stem = tool.get_param_by_request(request.POST, 'stem', "", str)
    ques_anw = tool.get_param_by_request(request.POST, 'ques_options', "", str)
    ques_ind = tool.get_param_by_request(request.POST, 'ques_index', 0, int)
    ques_id = tool.get_param_by_request(request.POST,'questionnaire_id', 0, int)
    ques_check = tool.get_param_by_request(request.POST, 'checkques', 1, int)
    try:
        jsontext = json.loads(ques_anw)
    except ValueError,e:
        return render_to_response("mz_course/questionnaire_item_add.html", {"page_index": page_index,"jsonerror": "请确认json格式！","questionnaires_stem":ques_stem,"questionnaires_ques_options":ques_anw,"questionnaires_index":ques_ind}, context_instance=RequestContext(request))
    if ques_id == 2 and ques_check >=1:
        return render_to_response("mz_course/questionnaire_item_add.html", {"page_index": page_index,"checkerror": "'免费体验班退出学习界面问卷'只能有一个问题！","questionnaires_stem":ques_stem,"questionnaires_ques_options":ques_anw,"questionnaires_index":ques_ind}, context_instance=RequestContext(request))
    questionnaire_item = api_questionnaire.insert_questionnaire_item(ques_stem, ques_anw, ques_ind, ques_id)
    if questionnaire_item.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect("/course/questionnaire/list/?action=query&page_index=" + str(page_index))
