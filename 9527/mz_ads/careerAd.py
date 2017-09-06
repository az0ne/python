#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from db.api.ads import careerAd as api_careerAd
from db.api.apiutils import APIResult
from utils.decorators import dec_login_required
from utils import tool
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def career_ad_list(request):
    """
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', 'query')
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "")

    careerAd = APIResult()
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        careerAd = api_careerAd.delete_career_ad(_id)
        if careerAd.is_error():
            # 处理错误
            return render_to_response("html404.html", {}, context_instance=RequestContext(request))

        if not careerAd.result():
            return render_to_response("delete_error.html", {}, context_instance=RequestContext(request))

        else:
            return HttpResponseRedirect('/ads/careerAd/list/?action=query&page_index=' + str(page_index))

    if action == "query":
        careerAd = api_careerAd.list_career_ad_by_page(page_index, settings.PAGE_SIZE)

    if action == "search":
        careerAd = api_careerAd.list_career_ad_by_img_title('%' + key_word + '%', page_index, settings.PAGE_SIZE)

    if careerAd.is_error():
        # 处理错误
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    c = {"careerAds": careerAd.result()["result"],
         "page": {"page_index": page_index, "rows_count": careerAd.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": careerAd.result()["page_count"],
                  }, "key_word": key_word}

    return render_to_response("mz_ads/careerAd_list.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def career_ad_edit(request):
    """
    get one data by id from mysql,
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', "add")
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)

    careerAd = None
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        careerAd = api_careerAd.get_career_ad_by_id(_id)

        if careerAd.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

        careerAd = careerAd.result()[0]
    c = {"careerAd": careerAd, "action": action, "page_index": page_index}

    return render_to_response("mz_ads/careerAd_save.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def career_ad_save(request):
    """
    save data to mysql database,from update and add
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.POST, 'action', 'add', str)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)  # 当前页
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    career_id = tool.get_param_by_request(request.POST, 'career_id', 0, int)
    img_url = request.FILES.get('img_url', '') #tool.get_param_by_request(request.FILES.get, 'img_url', "")
    old_image_path = tool.get_param_by_request(request.POST, 'old_image_path', "", str)
    img_title = tool.get_param_by_request(request.POST, 'img_title', "", str)
    is_actived = tool.get_param_by_request(request.POST, 'is_actived', 1, int)
    ad_type = tool.get_param_by_request(request.POST, 'type', "COURSE", str)
    bgcolor = tool.get_param_by_request(request.POST, 'bgcolor', "", str)
    url = tool.get_param_by_request(request.POST, 'url', "", str)

    print img_url
    image_path = old_image_path  # 如果更新数据时，未更改图片，image_url为空，设置图片的路径为老路径
    if img_url:
        image_path = tool.upload(img_url, settings.UPLOAD_IMG_PATH)

    careerAd = APIResult()
    if is_actived:
        api_careerAd.update_career_ad_is_actived()
    if action == "add":
        print url,bgcolor
        careerAd = api_careerAd.insert_career_ad(career_id, image_path, img_title, is_actived, ad_type, url, bgcolor)
    elif action == "edit":
        careerAd = api_careerAd.update_career_ad(_id, career_id, image_path, img_title, is_actived, ad_type, url, bgcolor)

    if careerAd.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    return HttpResponseRedirect('/ads/careerAd/list/?action=query&page_index=' + str(page_index))
