# coding: utf-8
__author__ = 'Administrator'
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

import utils.tool
import utils.handle_exception
import utils.decorators
import db.api.apiutils
import db.api.common.onevone.userMeetingCount
from utils.logger import logger as log

URL = ''

@utils.decorators.dec_login_required
@utils.handle_exception.handle_http_response_exception(501)
def userMeetingCount_list(request):
    """
    :param
    :return
    """
    global URL
    URL = request.get_full_path()
    page_size = settings.PAGE_SIZE
    page_index = utils.tool.get_param_by_request(request.GET, 'page_index', 1, int)
    action = utils.tool.get_param_by_request(request.GET, 'action', '', str)
    key_word = utils.tool.get_param_by_request(request.GET, 'key_word', '', str)

    if action == 'search':
        if key_word=='%':
            key_word ='\\' + key_word
        userMeetingCounts = db.api.common.onevone.userMeetingCount.userMeetingCount_search(key_word='%'+key_word+'%',
                                                                                           page_index=page_index,
                                                                                           page_size=page_size)

    else:
        userMeetingCounts = db.api.common.onevone.userMeetingCount.userMeetingCount_list(page_index=page_index,
                                                                                     page_size=page_size)

    if userMeetingCounts.is_error():
        log.warn(
            "get userMeetingCount is_error"
            "action:{0}".format(action)
        )
        return render(request, '404.html', {})
    if not userMeetingCounts.result():
        log.info(
            "get userMeetingCount result() error"
            "action:{0}".format(action)
        )
        return render(request, '404.html', {})

    result_dict = {
        'userMeetingCounts':userMeetingCounts.result()['result'],
        'key_word':key_word,
        'page':dict(
            page_index = page_index,
            page_size = page_size,
            rows_count = userMeetingCounts.result()['rows_count'],
            page_count = userMeetingCounts.result()['page_count']
        )
    }
    return render(request,'mz_common/onevone/userMeetingCount_list.html',result_dict)

@utils.decorators.dec_login_required
@utils.handle_exception.handle_http_response_exception(501)
def userMeetingCount_edit(request):
    """
    :return update page
    """
    _id = utils.tool.get_param_by_request(request.GET, 'id', 0, int )
    userMeetingCount_detail = db.api.common.onevone.userMeetingCount.userMeetingCount_detail(_id=_id)
    result_dict = {
        'userMeetingCount_detail':userMeetingCount_detail.result()
    }

    return render(request, 'mz_common/onevone/userMeetingCount_edit.html', result_dict)

@utils.decorators.dec_login_required
@utils.handle_exception.handle_http_response_exception(501)
def userMeetingCount_save(request):
    """
    :param
    :return
    """
    action = utils.tool.get_param_by_request(request.POST, 'action', '', str)
    _id = utils.tool.get_param_by_request(request.POST, 'id', 0, int)
    count = utils.tool.get_param_by_request(request.POST, 'count', 0, int)
    max_count = utils.tool.get_param_by_request(request.POST, 'max_count', 0, int)

    userMeetingCount_save = db.api.apiutils.APIResult()

    if action == 'save':
        userMeetingCount_save = db.api.common.onevone.userMeetingCount.userMeetingCount_update(_id=_id,count=count,
                                                                                               max_count=max_count)

    if userMeetingCount_save.is_error():
        log.warn(
            "update userMeetingCount is_error"
            "id:{0}".format(_id)
        )
        return render(request, '404.html', {})
    if not userMeetingCount_save.result():
        log.info(
            "update userMeetingCount result() error"
            "id:{0}".format(_id)
        )
        return render(request, '404.html', {})

    return HttpResponseRedirect(utils.tool.get_correct_url(URL,reverse('mz_common:userMeetingCount_list')))
