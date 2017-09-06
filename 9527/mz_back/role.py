# -*- coding:utf-8 -*-
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception, handle_ajax_response_exception
from utils import tool
from utils.tool import get_correct_url
from db.api.admin import role as api_role
from db.api.admin import menu as api_menu
from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

@dec_login_required
@handle_http_response_exception(501)
def role_save(request):
    name = tool.get_param_by_request(request.POST, 'name', '', str)
    action = tool.get_param_by_request(request.POST, 'action', "add", str)
    if action == 'add':
        insert_role = api_role.insert_role(name)
        if insert_role.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    elif action == 'edit':
        _id = tool.get_param_by_request(request.POST, 'id', 0, int)
        update_role = api_role.update_role_by_id(_id, name)
        if update_role.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect(request.session.get("url_back", reverse("mz_back:role_list")))


@dec_login_required
@handle_http_response_exception(501)
def role_edit(request):
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    role = None
    if action == "edit":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        role = api_role.get_role_by_id(_id)
        if role.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        role = role.result()[0]
    c = {"role": role, "action": action, 'page_index': page_index}
    return render_to_response("mz_back/role_add.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def role_list(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    keyword = ''
    request.session["url_back"] = request.get_full_path()
    if action == 'search':
        keyword = tool.get_param_by_request(request.GET, 'keyword', '', str)
        get_roles = api_role.get_roles_by_keyword(page_index, settings.PAGE_SIZE, '%' + keyword + '%', )
        if get_roles.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    else:
        get_roles = api_role.list_role_by_page(page_index, settings.PAGE_SIZE)
        if get_roles.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

    menus = api_menu.list_menus().result()
    get_roles_ret = get_roles.result()["result"]
    roles = []
    for role in get_roles_ret:
        had_menus = api_menu.get_had_menus_by_role_id(role['id']).result()
        dt = {'role_id': role['id'], 'role_name': role['name'], 'menus': had_menus}
        roles.append(dt)
    c = {"roles": roles, 'menus': menus, 'keyword': keyword,
         "page": {"page_index": page_index, "rows_count": get_roles.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": get_roles.result()["page_count"]}}
    return render_to_response("mz_back/role_list.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def role_menu_save(request):
    role_id = tool.get_param_by_request(request.POST, 'role_id', 0, int)
    menu_id_list = request.POST.getlist("menu")
    new_menus_id_list = []
    count = api_menu.count_role_have_the_menu(role_id).result()

    if count > 0:
        delete_ret = api_menu.delete_role_menu_by_role_id(role_id)
        if delete_ret.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

    if menu_id_list:
        for menu_id in menu_id_list:
            menu = api_menu.get_menu_by_id(menu_id).result()
            if menu:
                new_menus_id_list.append(menu[0]['parent_id'])
        new_menus_id_list = {}.fromkeys(new_menus_id_list).keys() + menu_id_list

    if new_menus_id_list:
        for menu_id in new_menus_id_list:
            api_menu.insert_role_menu(role_id, menu_id)

    return HttpResponseRedirect(request.session.get("url_back", reverse("mz_back:role_list")))


@handle_ajax_response_exception
def role_isHaveTheName(request):
    name = tool.get_param_by_request(request.GET, 'name', '', str)
    is_have = False
    count = api_role.count_have_role_name(name).result()
    if count > 0:
        is_have = True
    result = {'is_have': is_have}
    return result


@dec_login_required
@handle_ajax_response_exception
def get_had_menus_by_role_id(request):
    role_id = tool.get_param_by_request(request.GET, 'role_id')
    menus = api_menu.get_had_menus_by_role_id(role_id).result()
    result = {'menus': menus}
    return result