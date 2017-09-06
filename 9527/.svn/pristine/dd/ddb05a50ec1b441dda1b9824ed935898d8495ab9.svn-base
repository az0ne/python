# -*- coding:utf-8 -*-
from django.conf import settings
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
from utils.logger import logger as log
import db.api.ads.app_career_ad
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from mz_lps4.career.lps4_career import get_lps4_career_course


@dec_login_required
@handle_http_response_exception(501)
def app_career_ad_list(request):
    page_index = get_param_by_request(request.GET, 'page_index', 1, int)
    APIResult = db.api.ads.app_career_ad.list_all_app_career_ad(page_index, settings.PAGE_SIZE)
    if APIResult.is_error():
        log.warn('list app career ad failed.')
        return render(request, '404.html')
    ads = APIResult.result()
    c = {"ads": ads["result"],
         "page": {"page_index": page_index, "rows_count": ads["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": ads["page_count"],
                  }}
    return render(request, 'mz_ads/app_career_ad_list.html', c)


@dec_login_required
@handle_http_response_exception(501)
def app_career_ad_edit(request):
    action = get_param_by_request(request.GET, 'action', 'add', str)

    try:
        career_list = get_lps4_career_course()
    except Http404:
        return render(request, '404.html')

    ad_info = dict()
    if 'edit' in action:
        career_id = get_param_by_request(request.GET, 'career_id', 0, int)
        APIResult = db.api.ads.app_career_ad.get_ad_info_by_career_id(career_id)
        if APIResult.is_error():
            log.warn('get app career ad by career_id failed.')
            return render(request, '404.html')
        ad_info = APIResult.result()

    c = dict(ad_info=ad_info, career_list=career_list, action=action)
    return render(request, 'mz_ads/app_career_ad_edit.html', c)


@dec_login_required
@handle_http_response_exception(501)
def app_career_ad_save(request):
    action = get_param_by_request(request.POST, 'action', '', str)
    career_id = get_param_by_request(request.POST, 'career_id', 0, int)
    title = get_param_by_request(request.POST, 'title', '', str)
    img_url = get_param_by_request(request.POST, 'img_url', '', str)
    callback_url = get_param_by_request(request.POST, 'callback_url', '', str)
    ad_info = dict(career_id=career_id, title=title, img_url=img_url, callback_url=callback_url)
    if 'add' in action:
        APIResult = db.api.ads.app_career_ad.insert_ad_info(ad_info)
    else:
        APIResult = db.api.ads.app_career_ad.update_ad_info(ad_info)
    if APIResult.is_error():
        log.warn('insert or update app_career_ad failed.')
        return render(request, '404.html')
    return HttpResponseRedirect(reverse('mz_ads:app_ad_list'))


@dec_login_required
@handle_http_response_exception(501)
def check_is_have_the_career(request):
    career_id = get_param_by_request(request.GET, 'career_id', 0, int)
    is_have = True
    if career_id:
        APIResult = db.api.ads.app_career_ad.check_app_ad_is_have_career(career_id)
        if APIResult.is_error():
            log.warn('get count from mz_app_career_ad by career_id failed.')
            return render(request, '404.html')
        count = APIResult.result().get('count', 1)
        is_have = bool(count)
    return JsonResponse(dict(is_have=is_have))


@dec_login_required
@handle_http_response_exception(501)
def delete_app_ad_by_career_id(request):
    career_id = get_param_by_request(request.GET, 'career_id', 0, int)
    if career_id:
        APIResult = db.api.ads.app_career_ad.delete_ad_info_by_career_id(career_id)
        if APIResult.is_error():
            log.warn('delete app ad by career id failed.')
            return render(request, '404.html')
    return HttpResponseRedirect(reverse('mz_ads:app_ad_list'))
