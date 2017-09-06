# -*- coding:utf-8 -*-

from utils.decorators import dec_login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from db.api.course import questionnairequery as api_questionnairequery
from utils import tool
from utils.handle_exception import handle_http_response_exception
from django.http import HttpResponse
from django.http import JsonResponse
from django.http import HttpResponseRedirect
import json

@dec_login_required
@handle_http_response_exception(501)
def questionnairequery_list(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        questionnairequery = api_questionnairequery.delete_questionnairequery_item_by_id(_id)
        if questionnairequery.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

    if action == "search":
        if key_word == "%":
            key_word1 = '//' + key_word
            questionnaire = api_questionnairequery.get_questionnaire_item_by_stem('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)
        else:
            key_word1 = key_word
            questionnaire = api_questionnairequery.get_questionnaire_item_by_stem('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)
    else:
        questionnaire = api_questionnairequery.list_questionnairequery_item_by_page(page_index, settings.PAGE_SIZE)
    if questionnaire.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    c = {"questionnaires": questionnaire.result()["result"],
         "page": {"page_index": page_index, "rows_count": questionnaire.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": questionnaire.result()["page_count"]}}
    return render_to_response("mz_course/questionnaire_query.html", c, context_instance=RequestContext(request))



@dec_login_required
@handle_http_response_exception(501)
def questionnairequery_edit(request):
    _id = tool.get_param_by_request(request.GET,'id',0,int)
    questionnaireitem = api_questionnairequery.query_questionnaireitem(_id)
    c = {
        "questionnaires": questionnaireitem.result()["result"],
        "ques": questionnaireitem.result()["resultoth"],
        "quesid": _id,
    }
    return render_to_response("mz_course/questionnaire_query_add.html", c, context_instance=RequestContext(request))
