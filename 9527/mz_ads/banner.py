#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from db.api.ads import banner as api_banner
from db.api.apiutils import APIResult
from utils.decorators import dec_login_required
from utils import tool
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def banner_list(request):
    """
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', 'query')
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "")

    banner = APIResult()
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        banner = api_banner.delete_banner(_id)
        if banner.is_error():
            # 处理错误
            return render_to_response("html404.html", {}, context_instance=RequestContext(request))

        if not banner.result():
            return render_to_response("delete_error.html", {}, context_instance=RequestContext(request))

        else:
            return HttpResponseRedirect('/ads/bannermng/list/?action=query&page_index=' + str(page_index))

    if action == "query":
        banner = api_banner.list_banner_by_page(page_index, settings.PAGE_SIZE)

    if action == "search":
        if key_word == "%":
            key_word1 = '//'+key_word
        else:
            key_word1 = key_word
        banner = api_banner.list_banner_by_image_title('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)

    if banner.is_error():
        # 处理错误
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    c = {"banners": banner.result()["result"],
         "page": {"page_index": page_index, "rows_count": banner.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": banner.result()["page_count"],
                  }, "key_word": key_word}

    return render_to_response("mz_ads/banner_list.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def banner_edit(request):
    """
    get one data by id from mysql,
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', "add")
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)

    banner = None
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        banner = api_banner.get_banner_by_id(_id)

        if banner.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

        banner = banner.result()[0]
    c = {"banner": banner, "action": action, "page_index": page_index}

    return render_to_response("mz_ads/banner_save.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def banner_save(request):
    """
    save data to mysql database,from update and add
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.POST, 'action', 'add', str)
    page_index = tool.get_param_by_request(request.POST, 'page_index', "1", str)  # 当前页
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    image_url = request.FILES.get('image_url', '')
    old_image_path = tool.get_param_by_request(request.POST, 'old_image_path', "", str)
    image_title = tool.get_param_by_request(request.POST, 'image_title', "", str)
    url = tool.get_param_by_request(request.POST, 'url', "", str)
    index = tool.get_param_by_request(request.POST, 'index', 0, int)
    bgcolor = tool.get_param_by_request(request.POST, 'bgcolor', "", str)
    type = tool.get_param_by_request(request.POST, 'type', 1, int)

    image_path = old_image_path  # 如果更新数据时，未更改图片，image_url为空，设置图片的路径为老路径
    if image_url:
        image_path = tool.upload(image_url, settings.UPLOAD_IMG_PATH)

    banner = APIResult()
    if action == "add":
        banner = api_banner.insert_banner(image_title, image_path, url, index, bgcolor, type)
    elif action == "edit":
        banner = api_banner.update_banner(_id, image_title, image_path, url, index, bgcolor, type)

    if banner.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    return HttpResponseRedirect('/ads/bannermng/list/?action=query&page_index=' + page_index)
