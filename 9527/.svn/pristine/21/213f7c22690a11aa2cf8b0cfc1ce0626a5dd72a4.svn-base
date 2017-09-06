#!/usr/bin/env python
# -*- coding: utf8 -*-
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request, upload
from utils.logger import logger as log
from django.shortcuts import render
from django.core.urlresolvers import reverse
import db.api.micro.wechat_course.wechat_banner


@dec_login_required
@handle_http_response_exception(501)
def wechat_banner_list(request):
    action = get_param_by_request(request.GET, "action", "query", str)
    page_index = get_param_by_request(request.GET, "page_index", 1, int)
    APIResult = db.api.micro.wechat_course.wechat_banner.list_wechat_all_banner(page_index=page_index,
                                                                                page_size=settings.PAGE_SIZE)
    if APIResult.is_error():
        log.warn("list wechat banner failed.")
        return render(request, "404.html")
    result = APIResult.result()
    c = {"action": action, "banners": result["result"],
         "page": {"page_index": page_index, "page_size": settings.PAGE_SIZE,
                  "rows_count": result["rows_count"], "page_count": result["page_count"]}}
    return render(request, "mz_micro/wechat_course/wechat_banner_list.html", c)


@dec_login_required
@handle_http_response_exception(501)
def wechat_banner_edit(request):
    action = get_param_by_request(request.GET, "action", "query", str)
    if "edit" in action:
        _id = get_param_by_request(request.GET, "banner_id", 0, int)
        APIResult = db.api.micro.wechat_course.wechat_banner.get_wechat_banner_by_id(_id)
        if APIResult.is_error():
            log.warn("get wechat banner by id failed.")
            return render(request, "404.html")
        result = APIResult.result()
    else:
        result = dict()
    c = {"action": action, "banner": result}
    return render(request, "mz_micro/wechat_course/wechat_banner_edit.html", c)


@dec_login_required
@handle_http_response_exception(501)
def wechat_banner_del(request):
    _id = get_param_by_request(request.GET, "banner_id", 0, int)
    APIResult = db.api.micro.wechat_course.wechat_banner.del_wechat_banner_by_id(_id)
    if APIResult.is_error():
        log.warn("delete wechat banner by id failed.")
        return render(request, "404.html")
    return HttpResponseRedirect(reverse("mz_wechat:wechat_banner_list"))


@dec_login_required
@handle_http_response_exception(501)
def wechat_banner_save(request):
    title = get_param_by_request(request.POST, "title", "", str)
    image = request.FILES.get('image', None)
    url = get_param_by_request(request.POST, "url", "", str)
    index = get_param_by_request(request.POST, "index", 999, int)
    action = get_param_by_request(request.POST, "action", "add", str)
    old_image = get_param_by_request(request.POST, "old_image", "", str)

    if image:
        image_url = upload(image, settings.UPLOAD_IMG_PATH)
    else:
        image_url = old_image

    banner_dict = dict(title=title, url=url, index=index, image_url=image_url)
    if "add" in action:
        APIResult = db.api.micro.wechat_course.wechat_banner.insert_wechat_banner(banner_dict)
        if APIResult.is_error():
            log.warn("insert wechat banner failed.")
            return render(request, "404.html")

    elif "edit" in action:
        _id = get_param_by_request(request.POST, "banner_id", 0, int)
        banner_dict["id"] = _id
        APIResult = db.api.micro.wechat_course.wechat_banner.update_wechat_banner_by_id(banner_dict)
        if APIResult.is_error():
            log.warn("update wechat banner failed.")
            return render(request, "404.html")
    return HttpResponseRedirect(reverse("mz_wechat:wechat_banner_list"))
