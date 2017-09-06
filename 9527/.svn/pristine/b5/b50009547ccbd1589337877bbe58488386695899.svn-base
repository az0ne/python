# -*- coding: utf8 -*-

import db.api
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods, require_GET
from django.conf import settings
from django.shortcuts import render
from utils import tool
from utils.logger import logger as log
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception


# wiki广告列表
@dec_login_required
@handle_http_response_exception(501)
@require_GET
def wiki_ad_list(request):
    action = tool.get_param_by_request(request.GET, 'action', default_val='query')
    page_index = tool.safe_positive_int(request.GET.get('page_index'), 1)
    page_size = tool.safe_positive_int(request.GET.get('page_size'), settings.PAGE_SIZE)
    img_title = tool.get_param_by_request(request.GET, 'keyword', default_val='')
    ad_id = tool.get_param_by_request(request.GET, 'id', _type=int)

    if action == 'search':
        wiki_ad_data = db.api.get_wiki_ad_list(
            page_index, page_size, img_title=img_title)

    elif action == 'delete':
        result = db.api.del_wiki_ad(ad_id)
        if result.is_error():
            log.warn('delete wiki ad failed. wiki ad id: {0}'.format(ad_id))
            return HttpResponse('删除失败，请返回重试')
        return HttpResponseRedirect(
            reverse('mz_ads:wiki_ad_list') +
            '?action=query&page_index={0}'.format(page_index))

    else:
        wiki_ad_data = db.api.get_wiki_ad_list(page_index, page_size)

    if wiki_ad_data.is_error():
        log.warn('get wiki ad list failed.')
        wiki_ad_data = []
    else:
        wiki_ad_data = wiki_ad_data.result()

    wiki_ad_data.update(img_title=img_title)

    return render(request, 'mz_ads/wiki_ad_list.html', wiki_ad_data)


# wiki广告编辑
@dec_login_required
@handle_http_response_exception(501)
@require_http_methods(['GET', 'POST'])
def wiki_ad_edit(request):
    if request.method == 'GET':
        action = tool.get_param_by_request(request.GET, 'action', default_val='query')
        ad_id = tool.get_param_by_request(request.GET, 'id', _type=int)

        wiki_ad = None

        if action == 'edit':
            wiki_ad = db.api.get_wiki_ad(ad_id)
            course_types = db.api.get_wiki_course_types()

        elif action == 'add':
            course_types = db.api.get_wiki_course_types(is_all=False)

        else:
            wiki_ad = db.api.get_wiki_ad(ad_id)
            course_types = db.api.get_wiki_course_types()

        if wiki_ad:
            if wiki_ad.is_error():
                log.warn('get wiki ad failed. wiki_ad_id: {0}'.format(ad_id))
                wiki_ad = {}
            else:
                wiki_ad = wiki_ad.result()

        if course_types.is_error():
            log.warn('get wiki ad failed. wiki_ad_id: {0}'.format(ad_id))
            course_types = []
        else:
            course_types = course_types.result()

        data = dict(ad=wiki_ad, action=action, course_types=course_types)

        return render(request, 'mz_ads/wiki_ad_edit.html', data)

    else:
        action = tool.get_param_by_request(request.POST, 'action', default_val='add')
        page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)  # 跳转过来的页数
        ad_id = tool.get_param_by_request(request.POST, 'id', _type=int)
        img = request.FILES.get('img_url', '')
        old_image_url = tool.get_param_by_request(request.POST, 'old_image_path')
        img_title = tool.get_param_by_request(request.POST, 'img_title', default_val='')
        course_type_id = tool.get_param_by_request(request.POST, 'course_type_id', _type=int)
        url = tool.get_param_by_request(request.POST, 'url', default_val='')

        img_url = old_image_url
        if img:
            img_url = tool.upload(img, settings.UPLOAD_IMG_PATH)

        if action == 'edit':
            result = db.api.update_wiki_ad(
                ad_id=ad_id, img_url=img_url, img_title=img_title,
                url=url, course_type_id=course_type_id)

        elif action == 'add':
            page_index = 1
            result = db.api.add_wiki_ad(
               img_url=img_url, img_title=img_title, url=url,
               course_type_id=course_type_id)

        else:
            return HttpResponse('action错误，无“{0}”此action！'.format(action))

        if result.is_error():
            log.warn('{0} wiki ad failed. parm: action={1},  page_index={2}, '
                     'ad_id={3}, img={4}, old_image_url={5}, img_title={6}, '
                     'course_type_id={7}, url={8}'.format(
                        action, action, page_index, ad_id, img,
                        old_image_url, img_title, course_type_id, url))
            return HttpResponse('保存失败，请返回检查数据重试！')

        return HttpResponseRedirect(
            reverse('mz_ads:wiki_ad_list') +
            '?action=query&page_index={0}'.format(page_index))



