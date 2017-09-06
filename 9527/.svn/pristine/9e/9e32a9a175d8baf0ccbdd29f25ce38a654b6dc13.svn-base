
from utils.decorators import dec_login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
import json
from db.api.course import objTagRelation as api_objTagRelation
from db.api.homepage import homepagelink as api_homepagelink
from utils import tool
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def homepage_link(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        homepagelink = api_homepagelink.delete_homepagelink_by_id(_id)
        if homepagelink.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

    if action == "search":
        if key_word == "%":
            key_word1 = '//' + key_word
            homepagelink = api_homepagelink.get_homepagelink_by_title('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)
        else:
            key_word1 = key_word
            homepagelink = api_homepagelink.get_homepagelink_by_title('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)
    else:
        homepagelink = api_homepagelink.list_homepagelink_by_page(page_index, settings.PAGE_SIZE)
    if homepagelink.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    c = {"homepagelinks": homepagelink.result()["result"],
         "page": {"page_index": page_index, "rows_count": homepagelink.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": homepagelink.result()["page_count"]}}
    return render_to_response("mz_seo/tb_ homepage_link.html", c, context_instance=RequestContext(request))



@dec_login_required
@handle_http_response_exception(501)
def homepage_link_save(request):
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    action = tool.get_param_by_request(request.POST, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)
    title = tool.get_param_by_request(request.POST, 'title', "", str)
    url = tool.get_param_by_request(request.POST, 'url', "", str)
    index = tool.get_param_by_request(request.POST, 'index', "", str)
    if action == 'add':
        homepageink = api_homepagelink.insert_homepagelink(title,url,index)
        if homepageink.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    elif action == 'edit':
        homepageink = api_homepagelink.updatehomepageink(_id,title,url,index)
        if homepageink.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect("/seo/tb_homepage_link/list/?action=query&page_index=" + str(page_index))




@dec_login_required
@handle_http_response_exception(501)
def homepage_link_edit(request):
    action = tool.get_param_by_request(request.GET, 'action', "add")
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    homepageink = None
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        homepageink = api_homepagelink.get_homepageink_by_id(_id)
        if homepageink.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        homepageink = homepageink.result()[0]
        c = {"homepagelinks": homepageink, "action": action,"page_index": page_index}
    else:
        c = {"homepagelinks": homepageink, "action": action,"page_index": page_index}
    return render_to_response("mz_seo/tb_homepage_link_add.html", c, context_instance=RequestContext(request))