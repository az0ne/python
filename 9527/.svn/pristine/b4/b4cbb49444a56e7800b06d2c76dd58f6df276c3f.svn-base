#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.handle_exception import handle_http_response_exception
from utils.decorators import dec_login_required
from utils import tool
from django.conf import settings
from db.api.micro import micro_ask
from django.shortcuts import render
from utils.logger import logger as log
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime


@dec_login_required
@handle_http_response_exception(501)
def micro_ask_list(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    micro_course_id = tool.get_param_by_request(request.GET, 'micro_course_id', 0, int)
    micro_course_title = tool.get_param_by_request(request.GET, 'micro_course_title', '', str)
    status = 0  # 回复类型，0-全部 1-已回复 2-未回复
    keyword = ''
    if 'search' in action:
        keyword = tool.get_param_by_request(request.GET, 'keyword', '', str)
        status = tool.get_param_by_request(request.GET, 'status', 0, int)
        get_micro_course_ask = micro_ask.get_micro_ask_by_keyword_and_status(page_index, settings.PAGE_SIZE,
                                                                             '%' + keyword + '%', micro_course_id,
                                                                             status)
    elif 'delete' in action:
        _id = tool.get_param_by_request(request.GET, 'ask_id', 0, int)
        url_back = request.META.get('HTTP_REFERER', '')
        ret_del = micro_ask.delete_micro_ask_by_id(_id)
        if ret_del.is_error():
            return render(request, '404.html', {})
        if url_back and 'delete' not in url_back:
            return HttpResponseRedirect(url_back)
        return HttpResponseRedirect(reverse(
        'mz_micro:micro_ask_list') + "?action=query&micro_course_id=%s&micro_course_title=%s&page_index=%s" % (str(
        micro_course_id), micro_course_title, str(page_index)))
    else:
        get_micro_course_ask = micro_ask.list_micro_course_ask_by_page(page_index, settings.PAGE_SIZE,
                                                                       course_id=micro_course_id)

    if get_micro_course_ask.is_error():
        log.warn('failed to get micro course data.')
        return render(request, "404.html", {})
    micro_course_ask = get_micro_course_ask.result()['result']
    c = {"micro_course_ask": micro_course_ask, 'keyword': keyword, 'status': status,
         'micro_course_title': micro_course_title, 'micro_course_id': micro_course_id,
         "page": {"page_index": page_index, "rows_count": get_micro_course_ask.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": get_micro_course_ask.result()["page_count"]}}
    return render(request, "mz_micro/micro_ask_list.html", c)


@dec_login_required
@handle_http_response_exception(501)
def micro_ask_edit(request):
    '''
    微课问答编辑
    :param request:
    :return:
    '''

    action = tool.get_param_by_request(request.GET, 'action', 'edit', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    micro_course_title = tool.get_param_by_request(request.GET, 'micro_course_title', "", str)
    micro_course_id = tool.get_param_by_request(request.GET, 'micro_course_id', 0, int)
    url_back = request.META.get('HTTP_REFERER', '')
    micro_course_ask = dict()

    if 'edit' in action:
        _id = tool.get_param_by_request(request.GET, 'ask_id', 0, int)
        get_micro_ask_ret = micro_ask.get_micro_ask_by_id(_id)
        if get_micro_ask_ret.is_error():
            log.warn('It was failed to get data of micro ask')
            return render(request, "404.html", {})
        if get_micro_ask_ret.result():
            micro_course_ask = get_micro_ask_ret.result()[0]
        return render(request, "mz_micro/micro_ask_reply.html",
                      {'action': action, 'micro_course_ask': micro_course_ask, 'micro_course_id': micro_course_id,
                       'url_back': url_back, 'micro_course_title': micro_course_title, 'page_index': page_index})

    return HttpResponseRedirect(reverse('mz_micro:micro_ask_list'))


@dec_login_required
@handle_http_response_exception(501)
def micro_ask_save(request):
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    micro_course_id = tool.get_param_by_request(request.POST, 'micro_course_id', 0, int)
    micro_course_title = tool.get_param_by_request(request.POST, 'micro_course_title', '', str)
    answer = tool.get_param_by_request(request.POST, 'answer', '', str)
    answer_time = tool.get_param_by_request(request.POST, 'answer_time', '', str)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)
    action = tool.get_param_by_request(request.POST, 'action', "edit", str)
    url_back = tool.get_param_by_request(request.POST, 'url_back', "", str)
    if 'edit' in action:
        if not answer_time:
            answer_time = datetime.datetime.now()
        update_micro_ask = micro_ask.update_micro_ask_by_id(answer, answer_time, _id)
        if update_micro_ask.is_error():
            log.warn('Failed to get micro ask data.')
            return render(request, "404.html", {})

    if url_back and 'list' in url_back:
        return HttpResponseRedirect(url_back)

    return HttpResponseRedirect(reverse(
        'mz_micro:micro_ask_list') + "?action=query&micro_course_id=%s&micro_course_title=%s&page_index=%s" % (str(
        micro_course_id), micro_course_title, str(page_index)))
