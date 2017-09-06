# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render

from utils.decorators import dec_login_required
from django.conf import settings
import db.api.common.iosVersion
from utils import tool
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.handle_exception import handle_http_response_exception
from django.core.urlresolvers import reverse

# 全局变量
CURRENT_URL = ''  # 记录查看或修改某一条数据前的url地址


@dec_login_required
@handle_http_response_exception(501)
def ios_version_list(request):
    """
    iosVersion表中信息的显示
    action = query: 显示所有数据
    action = search: 根据vno字段，检索，并展示
    action = delete: 根据id,删除某条数据
    :param request:
    :return: 重新渲染页面，delete重定向到list页面
    """
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', '1', int)
    keyword = tool.get_param_by_request(request.GET, 'keyword', '', str)

    # 当action不为delete时，保存当前页的url地址到全局变量CURRENT_URL
    if action != 'delete':
        request.session["ios_version_list_url"] = request.get_full_path()

    if action == 'delete':
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        ios_version = db.api.common.iosVersion.delete_ios_version_by_id(_id)
        if ios_version.is_error():
            log.warn(
                'delete ios version information by id failed!'
                'ios_version_id:{0}'.format(_id)
            )
            return render(request, '404.hml', {})
        return HttpResponseRedirect(request.session.get("ios_version_list_url", reverse("mz_common:iosVersion_list")))
    if action == 'query':
        ios_version = db.api.common.iosVersion.select_ios_version_by_page(page_index, settings.PAGE_SIZE)
        if ios_version.is_error():
            log.warn(
                'select ios version by page failed!'
            )
            return render(request, '404.html', {})
    if action == 'search':
        if '%' in keyword:
            keyword1 = '\\' + keyword
        else:
            keyword1 = keyword
        ios_version = db.api.common.iosVersion.search_ios_version_by_vno_and_page("%" + keyword1 + "%", page_index,
                                                                                  settings.PAGE_SIZE)
        if ios_version.is_error():
            log.warn(
                'select ios version by page and vno failed!'
            )
            return render(request, '404.html', {})

    data = {
        'iosVersions': ios_version.result()["result"],
        'page': {"page_index": page_index, "rows_count": ios_version.result()["rows_count"],
                 "page_size": settings.PAGE_SIZE,
                 "page_count": ios_version.result()["page_count"],
                 }, "key_word": keyword}

    return render(request, 'mz_common/iosVersion_list.html', data)


@dec_login_required
@handle_http_response_exception(501)
def ios_version_edit(request):
    """
    查看/编辑某条数据的详细信息,默认为新增功能
    :param request:
    :return: 渲染编辑页面(iosVersion_edit.html)
    """

    action = tool.get_param_by_request(request.GET, "action", 'add', str)
    _id = tool.get_param_by_request(request.GET, 'id', 0, int)

    # action=add时，返回结果iosVersion键值为空
    ios_version = APIResult()
    if action == 'edit' or action == 'show':
        ios_version = db.api.common.iosVersion.get_ios_version_by_id(_id)
    if ios_version.is_error():
        log.warn(
            "get ios version by id failed!"
            "ios_version_id:{0}".format(_id)
        )
        return render(request, '404.html', {})
    c = {"iosVersion": ios_version.result(), "action": action}
    return render(request, 'mz_common/iosVersion_edit.html', c)


@dec_login_required
@handle_http_response_exception(501)
def ios_version_save(request):
    """
    新增/修改后保存数据
    :param request:
    :return:重定向到list页面
    """
    action = tool.get_param_by_request(request.POST, 'action', 'add', str)
    vno = tool.get_param_by_request(request.POST, 'vno', '', str)
    desc = tool.get_param_by_request(request.POST, 'desc', '', str)
    is_force = tool.get_param_by_request(request.POST, 'is_force', 0, int)
    is_check = tool.get_param_by_request(request.POST, 'is_check', 0, int)
    _type = tool.get_param_by_request(request.POST, 'type', 0, int)
    if action == 'add':
        ios_version = db.api.common.iosVersion.insert_ios_version(vno, desc, is_force, is_check, _type)
        if ios_version.is_error():
            log.warn(
                "insert into ios version table failed!"
            )
            return render(request, '404.html', {})

    if action == 'edit':
        _id = tool.get_param_by_request(request.POST, 'id', 0, int)
        ios_version = db.api.common.iosVersion.update_ios_version(_id, vno, desc, is_force, is_check, _type)
        if ios_version.is_error():
            log.warn(
                "update ios version by id failed!"
                "ios_version_id:{0}".format(_id)
            )
            return render(request, '404.html', {})

    return HttpResponseRedirect(
        request.session.get("ios_version_list_url", reverse("mz_common:iosVersion_list")))  # 重定向到进入到编辑或查看页面前的url地址上
