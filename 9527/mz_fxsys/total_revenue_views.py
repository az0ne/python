# -*- coding: utf-8 -*-

import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
from utils.logger import logger as log
from mz_fxsys import total_revenue_api
from myproject import settings


@dec_login_required
@handle_http_response_exception(501)
def add_total_revenue(request):
    """增加"""
    today = datetime.date.today()
    total_revenue = get_param_by_request(request.POST, 'total_revenue', '', str)
    date = get_param_by_request(request.POST, 'date', today, str)

    total_revenues = total_revenue_api.get_total_revenue_by_date(date)
    if not total_revenues.is_error():
        if total_revenues.result():
            result = total_revenue_api.update_total_revenue(total_revenues.result()[0]['id'], total_revenue, date)
        else:
            result = total_revenue_api.add_total_revenue(total_revenue, date)

    if result.is_error():
        log.info("insert user data failed!")
    else:
        log.info('{username},新增麦子学院{date}的总收益.总收益额：{total_revenue}--三级分销系统'.format(
            username=request.session.get('username', ''), date=date, total_revenue=total_revenue))
        return HttpResponseRedirect(reverse('mz_fxsys:get_total_revenue'))


@dec_login_required
@handle_http_response_exception(501)
def get_total_revenue_list(request):
    """查询"""
    date = get_param_by_request(request.GET, 'date', '', str)
    action = get_param_by_request(request.GET, 'action', 'search', str)
    page_index = get_param_by_request(request.GET, 'page_index', 1, int)

    if action == 'add':
        return render(request, 'mz_fxsys/totalRevenue_edit.html', {'action': 'add'})
    if action == "search":
        total_revenues = total_revenue_api.select_total_revenue_by_page(page_index, settings.PAGE_SIZE, date)
        if not total_revenues.is_error():
            log.info('{username},查看了麦子学院总收益额.--三级分销系统'.format(username=request.session.get('username', '')))

        data = {
            "total_revenues": total_revenues.result()['result'],
            "page": {
                "page_index": page_index, "rows_count": total_revenues.result()['rows_count'],
                "page_size": settings.PAGE_SIZE, "page_count": total_revenues.result()['page_count']
            },
        }
        return render(request, 'mz_fxsys/totalRevenue_list.html', data)


@dec_login_required
@handle_http_response_exception(501)
def del_total_revenue(request):
    _id = get_param_by_request(request.GET, 'id', 0, int)
    action = get_param_by_request(request.GET, "action", "del", str)

    if action == "del":
        del_total_revenue = total_revenue_api.del_total_revenue_by_id(_id)
        if not del_total_revenue.is_error():
            log.info("{username}删除了id为{id}的总收益额。--分销系统".format(username=request.session.get("username", ""), id=_id))
            return HttpResponseRedirect(reverse("mz_fxsys:get_total_revenue"))