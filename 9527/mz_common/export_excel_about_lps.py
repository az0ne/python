#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.logger import logger as log
from django.http import JsonResponse
from mz_common.common_interface import excel_export, get_api_data
from utils.tool import get_param_by_request
from django.conf import settings
import requests


@dec_login_required
@handle_http_response_exception(501)
def show_export_excel_about_lps(request):
    list_url = "%s%s" % (settings.OPERATION_API_HOST, '/action/list/')
    try:
        data = requests.get(list_url, timeout=5).json()
    except Exception as e:
        log.warn('get action list from api failed. info:%s' % e)
        data = list()
    return render(request, "mz_common/excel_export_lps_data.html", dict(actions=data))


@dec_login_required
@handle_http_response_exception(501)
def check_is_have_data(request):
    start_date = get_param_by_request(request.GET, 'start_date', '', str).replace('-', '')
    end_date = get_param_by_request(request.GET, 'end_date', '', str).replace('-', '')
    action_id = get_param_by_request(request.GET, 'action_id', '', str)
    json_result = get_api_data(start_date=start_date, end_date=end_date, action_id=action_id)
    dimensions = json_result.get('dimensions', None)
    if dimensions:  # 如果数据不为空则state='success'
        return JsonResponse(dict(status="success"))
    return JsonResponse(dict(status="failed"))


@dec_login_required
@handle_http_response_exception(501)
def export_excel_about_lps(request):
    '''
    导出lps数据到excel
    :param request:
    :return:
    '''
    # 获取前台传过来的数据
    start_date = get_param_by_request(request.GET, 'start_date', '', str).replace('-', '')
    end_date = get_param_by_request(request.GET, 'end_date', '', str).replace('-', '')
    action_id = get_param_by_request(request.GET, 'action_id', '', str)
    json_result = get_api_data(start_date=start_date, end_date=end_date, action_id=action_id)

    # 将获取的json格式的数据转换成生成EXCEL需要的格式
    # {sheet_name:list()}
    excel_data = dict()
    data_list = list()
    action_name = json_result.get('action_name', u"lps数据导出")
    name = "%s_%s_%s" % (action_name.encode("utf-8"), start_date, end_date)
    dimensions = json_result.get('dimensions', dict())
    for dimension_key in dimensions:
        data_list.append([dimension_key, u'数量'])
        dimension = dimensions.get(dimension_key, dict())
        for key in dimension:
            data_list.append([key, dimension.get(key)])
        data_list.append(list())
    excel_data.update({action_name: data_list})
    return excel_export(excel_name=name, excel_title=list(), excel_data=excel_data)

