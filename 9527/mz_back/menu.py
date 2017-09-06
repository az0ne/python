# -*- coding:utf-8 -*-
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception, handle_ajax_response_exception
from utils import tool
from db.api.admin import menu as api_menu
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from utils.handle_exception import handle_http_response_exception
from django.template import RequestContext

#menu 的功能暂时隐藏

@dec_login_required
@handle_http_response_exception(501)
def menu_save(request):
    name = tool.get_param_by_request(request.POST, 'name')
    url = tool.get_param_by_request(request.POST, 'url')
    page_index = tool.get_param_by_request(request.GET, 'page_index', "1", str)
    action = tool.get_param_by_request(request.POST, 'action', "add")
    if action == 'add':
        insert_menu = api_menu.insert_menu(name, url)
        if insert_menu.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    elif action == 'edit':
        _id = tool.get_param_by_request(request.POST, 'id', 0, int)
        update_menu = api_menu.update_menu_by_id(name, url, _id)
        if update_menu.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect("/backAdmin/menu/list/?action=query&page_index=" + page_index)


@dec_login_required
@handle_http_response_exception(501)
def menu_edit(request):
    action = tool.get_param_by_request(request.GET, 'action', "add")
    menu = None
    if action == "edit":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        get_menu = api_menu.get_menu_by_id(_id)
        if get_menu.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        menu = get_menu.result()[0]
    c = {"menu": menu, "action": action}
    return render_to_response("mz_back/menu_add.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def menu_list(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query')
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    get_menus = api_menu.list_menu_by_page(page_index, settings.PAGE_SIZE)
    if get_menus.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    c = {"menus": get_menus.result()["result"],
         "page": {"page_index": page_index, "rows_count": get_menus.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": get_menus.result()["page_count"]}}
    return render_to_response("mz_back/menu_list.html", c, context_instance=RequestContext(request))





