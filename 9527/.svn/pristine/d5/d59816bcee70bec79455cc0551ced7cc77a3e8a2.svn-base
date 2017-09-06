# -*- coding:utf-8 -*-
from utils.decorators import dec_login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from db.api.homepage import careerlinkthr as api_careerlink
from utils import tool
from utils.handle_exception import handle_http_response_exception





@dec_login_required
@handle_http_response_exception(501)
def career_link(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        careerlink = api_careerlink.delete_careerlink_by_id(_id)
        if careerlink.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

    if action == "search":
        if key_word == "%":
            key_word1 = '//' + key_word
            careerlink = api_careerlink.get_careerlink_by_title('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)
        else:
            key_word1 = key_word
            careerlink = api_careerlink.get_careerlink_by_title('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)
    else:
        careerlink = api_careerlink.list_careerlink_by_page(page_index, settings.PAGE_SIZE)
    if careerlink.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    c = {"careerlinks": careerlink.result()["result"],
         "page": {"page_index": page_index, "rows_count": careerlink.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": careerlink.result()["page_count"]}}
    return render_to_response("mz_seo/mz_career_link3.0.html", c, context_instance=RequestContext(request))



@dec_login_required
@handle_http_response_exception(501)
def career_link_save(request):
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    action = tool.get_param_by_request(request.POST, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)
    title = tool.get_param_by_request(request.POST, 'title', "", str)
    url = tool.get_param_by_request(request.POST, 'url', "", str)
    index = tool.get_param_by_request(request.POST, 'index', "", str)
    career_id = tool.get_param_by_request(request.POST, 'career_id', "", str)
    if action == 'add':
        careerlink = api_careerlink.insert_careerlink(title,url,index,career_id)
        if careerlink.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    elif action == 'edit':
        careerlink = api_careerlink.updatecareerlink(_id,title,url,index,career_id)
        if careerlink.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect("/seo/mz_career_linkthr/list/?action=query&page_index=" + str(page_index))




@dec_login_required
@handle_http_response_exception(501)
def career_link_edit(request):
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)

    careerlink = None
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        careerlink = api_careerlink.get_careerlink_by_id(_id)
        if careerlink.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        careerlink1 = careerlink.result()[0]
        c = {"careerlinks": careerlink1, "action": action,"page_index": page_index}
    else:
        c = {"careerlinks": careerlink, "action": action,"page_index": page_index}
    return render_to_response("mz_seo/mz_career_link_add3.0.html", c, context_instance=RequestContext(request))