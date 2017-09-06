#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext

import db.api.ads.career_newad
from utils.logger import logger as log
from utils.decorators import dec_login_required
from db.api.apiutils import APIResult
from utils import tool
from utils.handle_exception import handle_http_response_exception

NEW_AD_DICT = {1: "UI设计", 2: "Web 前端开发", 3: "Python Web 开发", 4: "产品经理", 5: "互联网运营"}

@dec_login_required
@handle_http_response_exception(501)
def career_new_ad_list(request):
    """
    首页职业课程广告
    :param request:
    :return:
    """

    action = tool.get_param_by_request(request.GET, 'action', 'query', str)

    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        new_ad = db.api.ads.career_newad.delete_career_newad(_id)
        if new_ad.is_error():
            # 处理错误
            log.warn("delete_career_newad is error id:{0}".format(_id))
            return render(request, "html404.html")

        if not new_ad.result():
            return render(request, "delete_error.html")

        else:
            return HttpResponseRedirect(reverse("mz_ads:career_newAd_list"))

    if action == "query":
        new_ad_result = db.api.ads.career_newad.get_career_newad_list()

        if new_ad_result.is_error():
            # 处理错误
            log.warn("get_career_newad_list is error")
            return render(request, "404.html")
        new_ad_list = new_ad_result.result()
        for new_ad in new_ad_list:
            new_ad["index_value"] = NEW_AD_DICT.get(new_ad['newad_index'],"")
        c = {"newAds": new_ad_list, "action": "query"}
        return render(request, "mz_ads/newAd_list.html", c)


@dec_login_required
@handle_http_response_exception(501)
def update_career_new_ad(request):
    """
    修改
    :param request:
    :return:
    """

    action = tool.get_param_by_request(request.GET, 'action', "add")
    _id = tool.get_param_by_request(request.GET, 'id', 0, int)
    new_ad_result = db.api.ads.career_newad.get_career_newad_get_by_id(_id)

    if new_ad_result.is_error():
        log.warn("get_career_newad_get_by_id is error id:{0}".format(_id))
        return render(request, "404.html")

    c = {"newAd": new_ad_result.result(), "action": action}

    return render(request, "mz_ads/newAd_save.html", c)


@dec_login_required
@handle_http_response_exception(501)
def save_career_new_ad(request):
    """
    保存
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.POST, 'action', 'add', str)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)  # 当前页
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    img_url = request.FILES.get('image', '')
    old_image_path = tool.get_param_by_request(request.POST, 'old_image_path', "", str)
    image_title = tool.get_param_by_request(request.POST, 'image_title', "", str)
    title1 = tool.get_param_by_request(request.POST, 'title1', "", str)
    title1_url = tool.get_param_by_request(request.POST, 'title1_url', "", str)
    title2 = tool.get_param_by_request(request.POST, 'title2', "", str)
    title2_url = tool.get_param_by_request(request.POST, 'title2_url', "", str)
    index = tool.get_param_by_request(request.POST, 'index', 1, int)

    img_path = old_image_path  # 如果更新数据时，未更改图片，image_url为空，设置图片的路径为老路径
    if img_url:
        img_path = tool.upload(img_url, settings.UPLOAD_IMG_PATH)

    if action == "add":
        new_ad = db.api.ads.career_newad.insert_career_newad(img_path, image_title, title1, title1_url, title2,
                                                             title2_url, index)
        if new_ad.is_error():
            log.warn("insert_career_newad is error")

    elif action == "edit":
        new_ad = db.api.ads.career_newad.update_career_newad(_id, img_path, image_title, title1, title1_url, title2,
                                                             title2_url, index)
        if new_ad.is_error():
            log.warn("update_career_newad is error id:{0}".format(_id))

    if new_ad.result():
        return HttpResponseRedirect(reverse("mz_ads:career_newAd_list")+'?action=query&page_index=' + str(page_index))

    return render(request, "404.html")

