#!/usr/bin/env python
# -*- coding:utf-8 -*-
from utils.tool import get_param_by_request
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
import db.api.mz_wechat.menu
from utils.logger import logger as log
import db.api.mz_wechat.reply
from django.core.urlresolvers import reverse
from mz_wechat.constants import MenuType, ReplyType
from mz_wechat.functions import get_reply_data
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
import json

MENU_TYPE = (u"菜单跳转", u"菜单点击事件", u"主菜单")


@dec_login_required
@handle_http_response_exception(501)
def wechat_menu_list(request):
    APIResult = db.api.mz_wechat.menu.list_wechat_menu()
    if APIResult.is_error():
        log.warn("list wechat menu failed.")
        return render(request, "404.html", {})
    menus = APIResult.result()
    if menus:
        for menu in menus:
            menu["type_name"] = MENU_TYPE[menu["type"] - 1]
    return render(request, "mz_wechat/menu_list.html", dict(menus=menus))


@dec_login_required
@handle_http_response_exception(501)
def wechat_menu_edit(request):
    action = get_param_by_request(request.GET, "action", "edit", str)
    menu = None
    if "edit" in action:
        _id = get_param_by_request(request.GET, "id", 0, int)
        menu = get_menu_by_id(request, _id)
    return render(request, "mz_wechat/wechat_menu_edit.html", dict(menu=menu, action=action))


@dec_login_required
@handle_http_response_exception(501)
def wechat_menu_save(request):
    type = get_param_by_request(request.POST, "type", 0, int)
    name = get_param_by_request(request.POST, "name", "", str)
    _id = get_param_by_request(request.POST, "id", 0, int)
    key = ""
    menu = get_menu_by_id(request, _id)
    if type == MenuType.TARGET:
        key = get_param_by_request(request.POST, "key", "", str)
    elif type == MenuType.CLICK:
        if menu:
            key = "%s_%s" % (menu["location_x"], menu["location_y"])
    elif menu["type"] == MenuType.MENU:
        type = MenuType.MENU

    data = dict(type=type, key=key, name=name, id=_id)
    update_result = db.api.mz_wechat.menu.update_wechat_menu_by_id(data)
    if update_result.is_error():
        log.warn("update menu failed. id=%s" % _id)
        return render(request, "404.html", {})

    if type == MenuType.CLICK and menu["type"] == MenuType.TARGET:  # 发送链接菜单更改为发送消息菜单,跳转到新增消息页面
        action = "add"
        return HttpResponseRedirect(reverse("mz_wechat:menu_reply_edit") + "?action=%s&menu_id=%s" % (action, _id))
    elif type == MenuType.TARGET and menu["type"] == MenuType.CLICK:  # 发送消息菜单更改为发送链接菜单，删除原菜单对应的消息
        delete_replys_by_menu(request, _id)
    return HttpResponseRedirect(reverse("mz_wechat:wechat_menu_list"))


@dec_login_required
@handle_http_response_exception(501)
def menu_reply_list(request):
    menu_id = get_param_by_request(request.GET, "id", 0, int)
    get_reply = db.api.mz_wechat.menu.get_wechat_menu_reply_by_id(menu_id)
    if get_reply.is_error():
        log.warn("get all reply by menu id failed. menu_id=%s" % menu_id)
        return render(request, "404.html", {})
    replys = get_reply.result()
    for reply in replys:
        reply["type_name"] = ReplyType.map[reply["type"]]
    return render(request, "mz_wechat/reply_menu_list.html", dict(replys=replys, menu_id=menu_id))


@dec_login_required
@handle_http_response_exception(501)
def menu_reply_edit(request):
    action = get_param_by_request(request.GET, "action", "add", str)
    menu_id = get_param_by_request(request.GET, "menu_id", 0, int)
    reply = None
    if "show" in action:
        _id = get_param_by_request(request.GET, "id", 0, int)
        reply = get_reply_by_id(request, _id)
    return render(request, "mz_wechat/reply_edit.html", dict(menu_id=menu_id, action=action, reply=reply))


@dec_login_required
@handle_http_response_exception(501)
def menu_reply_save(request):
    action = get_param_by_request(request.POST, "action", "add", str)
    menu_id = get_param_by_request(request.POST, "menu_id", 0, int)
    _type = get_param_by_request(request.POST, "reply_type", 0, int)
    reply_data = get_reply_data(request, request.POST, _type)
    if "add" in action:
        if menu_id > 0 and _type > 0:
            add_reply_menu(request, menu_id, _type, reply_data)
        else:
            log.warn("get menu_id or _type failed. menu_id=%s,_type=%s." % (menu_id, _type))
    return HttpResponseRedirect(reverse("mz_wechat:menu_reply_list") + "?id=%s" % menu_id)


@dec_login_required
@handle_http_response_exception(501)
def menu_reply_delete(request):
    _id = get_param_by_request(request.GET, "id", 0, int)
    menu_id = get_param_by_request(request.GET, "menu_id", 0, int)
    delete_reply(request, _id, menu_id)
    return HttpResponseRedirect(reverse("mz_wechat:menu_reply_list") + "?id=%s" % menu_id)


def get_menu_by_id(request, _id):
    menu = dict()
    if _id > 0:
        APIResult = db.api.mz_wechat.menu.get_wechat_menu_by_id(_id)
        if APIResult.is_error():
            log.warn("get wechat menu by id failed. id=%s" % _id)
            return render(request, "404.html", {})
        menu = APIResult.result()
    return menu


def add_reply_menu(request, menu_id, reply_type, content):
    insert_menu_reply = db.api.mz_wechat.menu.insert_wechat_menu_reply(reply_type, content, menu_id)
    if insert_menu_reply.is_error():
        log.warn("insert menu reply failed. menu_id=%s,reply_type=%s" % (menu_id, reply_type))
        return render(request, "404.html", {})
    result = insert_menu_reply.result()
    return result


def delete_reply(request, _id, menu_id):
    del_menu_reply = db.api.mz_wechat.menu.delete_wechat_menu_reply(menu_id, _id)
    if del_menu_reply.is_error():
        log.warn("delete menu_reply failed. menu_id=%s,reply_id=%s" % (menu_id, _id))
        return render(request, "404.html", {})
    result = del_menu_reply.result()
    return result


def delete_replys_by_menu(request, menu_id):
    del_replys = db.api.mz_wechat.menu.delete_replys_by_menu_id(menu_id)
    if del_replys.is_error():
        log.wran("delete replys by menu failed.menu_id=%s" % menu_id)
        return render(request, "404.html", {})


def get_reply_by_id(request, _id):
    get_reply = db.api.mz_wechat.reply.get_reply(_id)
    if get_reply.is_error():
        log.warn("get reply failed.id=%s" % _id)
        return render(request, "404.html", {})
    reply = get_reply.result()
    if reply['type'] == ReplyType.NEWS:
        content = json.loads(reply['content'])
        reply['titles'] = {ni['title']: ni['content_url'] for ni in content['news_info']['list']}
    return reply
