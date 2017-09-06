# -*- coding:utf-8-*-

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
from utils.logger import logger as log
import db.api.fxsys.rebatetype


@dec_login_required
@handle_http_response_exception(501)
def get_rebate_type_list(request):
    """
    查询列表
    :param request:
    :return:
    """
    result = db.api.fxsys.rebatetype.list_rebate_type()
    if result.is_error():
        log.warn('list_rebate_type is error')
    rebate_type_list = result.result()
    data = {'rebate_type_list': rebate_type_list}
    return render(request, 'mz_fxsys/rebate_type_list.html', data)


@dec_login_required
@handle_http_response_exception(501)
def rebate_type_edit(request, rebate_type_id):
    """
    编辑
    :param request:
    :param rebate_type_id:
    :return:
    """
    if request.method == 'POST':
        name = get_param_by_request(request.POST, 'name', '', str)
        rebate_no = get_param_by_request(request.POST, 'rebate_no', '', str)
        if name and rebate_no:
            result = db.api.fxsys.rebatetype.insert_rebate_type(name, rebate_no)
            if result.is_error():
                log.warn('insert_rebate_type is error name:{0} rebate_no:{1}'.format(name, rebate_no))
            else:
                return HttpResponseRedirect(reverse('mz_fxsys:get_rebate_type_list'))
    result = db.api.fxsys.rebatetype.get_rebate_type_by_id(int(rebate_type_id))
    if result.is_error():
        log.warn('get_rebate_type_by_id is error')
    rebate_type = result.result()
    data = {'rebate_type': rebate_type,
            'action': 'edit'}
    return render(request, 'mz_fxsys/rebate_type_edit.html', data)


@dec_login_required
@handle_http_response_exception(501)
def rebate_type_add(request):
    """
    新增加
    :param request:
    :return:
    """
    name = get_param_by_request(request.POST, 'name', '', str)
    rebate_no = get_param_by_request(request.POST, 'rebate_no', '', str)
    if name and rebate_no:
        result = db.api.fxsys.rebatetype.insert_rebate_type(name, rebate_no)
        if result.is_error():
           log.warn('insert_rebate_type is error')
        else:
            return HttpResponseRedirect(reverse('mz_fxsys:get_rebate_type_list'))
    data = {'action': 'add'}
    return render(request, 'mz_fxsys/rebate_type_edit.html', data)


@dec_login_required
@handle_http_response_exception(501)
def rebate_type_del(request):
    """
    删除
    :param request:
    :return:
    """
    _id = get_param_by_request(request.GET, '_id', 0, int)
    result = db.api.fxsys.rebatetype.is_exist_user_rebate_type(_id)
    if result.is_error():
        log.warn('is_exist_user_rebate_type is error rebate_type_id:%s' % _id)
        return render(request, '404.html')
    if result.result():
        return render(request, '404.html')
    result = db.api.fxsys.rebatetype.delete_rebate_type_by_id(_id)
    if result.is_error():
        log.warn('delete_rebate_type_by_id is error rebate_type_id:%s' % _id)
        return render(request, '404.html')
    return HttpResponseRedirect(reverse('mz_fxsys:get_rebate_type_list'))
