#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from db.api.ads import newAd as api_newAd
from utils.decorators import dec_login_required
from db.api.apiutils import APIResult
from utils import tool
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def new_ad_list(request):
    """

    :param request:
    :return:
    """

    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "")

    new_ad = APIResult()
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        new_ad = api_newAd.delete_new_ad(_id)
        if new_ad.is_error():
            # 处理错误
            return render_to_response("html404.html", {}, context_instance=RequestContext(request))

        if not new_ad.result():
            return render_to_response("delete_error.html", {}, context_instance=RequestContext(request))

        else:
            return HttpResponseRedirect('/ads/newAd/list/?action=query&page_index=' + str(page_index))

    if action == "query":
        new_ad = api_newAd.list_new_ad_by_page(page_index, settings.PAGE_SIZE)

    if action == "search":
        new_ad = api_newAd.list_new_ad_by_img_title('%' + key_word + '%', page_index, settings.PAGE_SIZE)

    if new_ad.is_error():
        # 处理错误
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    c = {"newAds": new_ad.result()["result"],
         "page": {"page_index": page_index, "rows_count": new_ad.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": new_ad.result()["page_count"],
                  }, "key_word": key_word}

    return render_to_response("mz_ads/newAd_list.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def new_ad_edit(request):
    """
    get one data by id from mysql,
    :param request:
    :return:
    """

    action = tool.get_param_by_request(request.GET, 'action', "add")
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)

    new_ad = None
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        new_ad = api_newAd.get_new_ad_by_id(_id)

        if new_ad.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

        new_ad = new_ad.result()[0]

    c = {"newAd": new_ad, "action": action, "page_index": page_index}

    return render_to_response("mz_ads/newAd_save.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def new_ad_save(request):
    """
    save data to mysql database,from update and add
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.POST, 'action', 'add', str)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)  # 当前页
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    img_url = tool.get_param_by_request(request.FILES, 'img_url')
    ad_type = tool.get_param_by_request(request.POST, 'type', "", str)
    old_image_path = tool.get_param_by_request(request.POST, 'old_image_path', "", str)
    img_title = tool.get_param_by_request(request.POST, 'img_title', "", str)
    url = tool.get_param_by_request(request.POST, 'url', "", str)
    is_actived = tool.get_param_by_request(request.POST, 'is_actived', 0, int)

    img_path = old_image_path  # 如果更新数据时，未更改图片，image_url为空，设置图片的路径为老路径
    if img_url:
        img_path = tool.upload(img_url, settings.UPLOAD_IMG_PATH)

        new_ad = APIResult()
    if is_actived:
        api_newAd.update_new_ad_is_actived()  # 当is_actived等于1时，更改数据库is_actived字段为0

    if action == "add":
        new_ad = api_newAd.insert_new_ad(ad_type, img_title, img_path, url, is_actived)

    elif action == "edit":
        new_ad = api_newAd.update_new_ad(_id, ad_type, img_title, img_path, url, is_actived)

    if new_ad.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    return HttpResponseRedirect('/ads/newAd/list/?action=query&page_index=' + str(page_index))
