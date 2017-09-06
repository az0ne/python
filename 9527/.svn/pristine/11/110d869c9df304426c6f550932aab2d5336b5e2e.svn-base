
from utils.decorators import dec_login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from db.api.homepage import wikilink as api_wikilink
from utils import tool
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def wiki_link(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        wikilink = api_wikilink.delete_wikilink_by_id(_id)
        if wikilink.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

    if action == "search":
        if key_word == "%":
            key_word1 = '//' + key_word
            wikilink = api_wikilink.get_wikilink_by_title('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)
        else:
            key_word1 = key_word
            wikilink = api_wikilink.get_wikilink_by_title('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)
    else:
        wikilink = api_wikilink.list_wikilink_by_page(page_index, settings.PAGE_SIZE)
    if wikilink.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    c = {"wikilinks": wikilink.result()["result"],
         "page": {"page_index": page_index, "rows_count": wikilink.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": wikilink.result()["page_count"]}}
    return render_to_response("mz_seo/mz_wiki_link.html", c, context_instance=RequestContext(request))



@dec_login_required
@handle_http_response_exception(501)
def wiki_link_save(request):
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    action = tool.get_param_by_request(request.POST, 'action', 'query')
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)
    title = tool.get_param_by_request(request.POST, 'title', "", str)
    url = tool.get_param_by_request(request.POST, 'url', "", str)
    index = tool.get_param_by_request(request.POST, 'index', "", str)
    if action == 'add':
        wikilink = api_wikilink.insert_wikilink(title,url,index)
        if wikilink.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    elif action == 'edit':
        wikilink = api_wikilink.updatewikilink(_id,title,url,index)
        if wikilink.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect("/seo/mz_wiki_link/list/?action=query&page_index=" + str(page_index))




@dec_login_required
@handle_http_response_exception(501)
def wiki_link_edit(request):
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    wikilink = None
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        wikilink = api_wikilink.get_wikilink_by_id(_id)
        if wikilink.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        wikilink = wikilink.result()[0]
        c = {"wikilinks": wikilink, "action": action,"page_index": page_index}
    else:
        c = {"wikilinks": wikilink, "action": action,"page_index": page_index}
    return render_to_response("mz_seo/mz_wiki_link_add.html", c, context_instance=RequestContext(request))