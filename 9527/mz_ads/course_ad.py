# -*- coding: utf8 -*-

import db.api.ads.course_ad
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.conf import settings
from django.shortcuts import render
from utils import tool
from utils.logger import logger as log
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception


# course广告列表
@dec_login_required
@handle_http_response_exception(501)
@require_GET
def course_ad_list(request):
    action = tool.get_param_by_request(request.GET, 'action', default_val='query')
    page_index = tool.safe_positive_int(request.GET.get('page_index'), 1)
    page_size = tool.safe_positive_int(request.GET.get('page_size'), settings.PAGE_SIZE)
    img_title = tool.get_param_by_request(request.GET, 'keyword', default_val='')
    ad_id = tool.get_param_by_request(request.GET, 'id', _type=int)

    if action == 'search':
        course_ad_data = db.api.ads.course_ad.get_course_ad_list(
            page_index, page_size, img_title=img_title)

    elif action == 'delete':
        result = db.api.ads.course_ad.del_course_ad(ad_id)
        if result.is_error():
            log.warn('delete course_ad failed. course_ad id: {0}'.format(ad_id))
            return HttpResponse('删除失败，请返回重试')
        return HttpResponseRedirect(
            reverse('mz_ads:course_ad_list') +
            '?action=query&page_index={0}'.format(page_index))

    else:
        course_ad_data = db.api.ads.course_ad.get_course_ad_list(
            page_index, page_size)

    if course_ad_data.is_error():
        log.warn('get course_ad list failed.')
        course_ad_data = []
    else:
        course_ad_data = course_ad_data.result()

    return render(request, 'mz_ads/course_ad_list.html', course_ad_data)


# course广告编辑
@dec_login_required
@handle_http_response_exception(501)
@require_http_methods(['GET', 'POST'])
def course_ad_edit(request):
    if request.method == 'GET':
        action = tool.get_param_by_request(request.GET, 'action', default_val='query')
        ad_id = tool.get_param_by_request(request.GET, 'id', _type=int)

        course_ad = None

        if action == 'edit':
            course_ad = db.api.ads.course_ad.get_course_ad(ad_id)
            careers = db.api.ads.course_ad.get_career_courses()

        elif action == 'add':
            careers = db.api.ads.course_ad.get_career_courses(is_all=False)

        else:
            course_ad = db.api.ads.course_ad.get_course_ad(ad_id)
            careers = db.api.ads.course_ad.get_career_courses()

        if course_ad:
            if course_ad.is_error():
                log.warn('get wiki ad failed. course_ad_id: {0}'.format(ad_id))
                course_ad = {}
            else:
                course_ad = course_ad.result()

        if careers.is_error():
            log.warn('get wiki ad failed. course_ad_id: {0}'.format(ad_id))
            careers = []
        else:
            careers = careers.result()

        data = dict(ad=course_ad, action=action, careers=careers)
        return render(request, 'mz_ads/course_ad_edit.html', data)

    else:
        action = tool.get_param_by_request(request.POST, 'action', default_val='add')
        page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)  # 跳转过来的页数
        ad_id = tool.get_param_by_request(request.POST, 'id', _type=int)
        img = request.FILES.get('img_url', '')
        old_image_url = tool.get_param_by_request(request.POST, 'old_image_path')
        img_title = tool.get_param_by_request(request.POST, 'img_title', default_val='')
        career_id = tool.get_param_by_request(request.POST, 'career_id', _type=int)
        is_actived = tool.get_param_by_request(request.POST, 'is_actived', _type=int)
        url = tool.get_param_by_request(request.POST, 'url', default_val='')
        type = tool.get_param_by_request(request.POST, 'type', default_val='')

        img_url = old_image_url
        if img:
            img_url = tool.upload(img, settings.UPLOAD_IMG_PATH)

        if action == 'edit':
            result = db.api.ads.course_ad.update_course_ad(
                ad_id=ad_id, img_url=img_url, url=url, img_title=img_title,
                career_id=career_id, is_actived=is_actived, type=type)

        elif action == 'add':
            page_index = 1
            result = db.api.ads.course_ad.add_course_ad(
                img_url=img_url, url=url, img_title=img_title, career_id=career_id, type=type)

        else:
            return HttpResponse('action错误，无“{0}”此action！'.format(action))

        if result.is_error():
            log.warn('{0} wiki ad failed. parm: action={1},  page_index={2}, '
                     'ad_id={3}, img={4}, old_image_url={5}, img_title={6}, '
                     'career_id={7}'.format(
                        action, action, page_index, ad_id, img,
                        old_image_url, img_title, career_id))
            return HttpResponse('保存失败，请返回检查数据重试！')

        return HttpResponseRedirect(
            reverse('mz_ads:course_ad_list') +
            '?action=query&page_index={0}'.format(page_index))


# 更新course广告状态
@dec_login_required
@handle_http_response_exception(501)
@require_POST
def ajax_update_course_ad_status(request):
    ad_id = tool.get_param_by_request(request.POST, 'ad_id', _type=int)
    is_actived = tool.get_param_by_request(request.POST, 'is_actived', _type=int)

    result = db.api.ads.course_ad.update_course_ad_status(ad_id, is_actived)
    if result.is_error():
        log.warn('update_course_ad_status failed. '
                 'ad_id: {0}, is_actived: {1}'.format(ad_id, is_actived))
        result = False
    else:
        result = result.result()

    return JsonResponse(dict(success=result))
