# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

import db.api.fxsys.payments
from mz_fxsys.payments_api import select_userID_by_mobile
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
from utils.logger import logger as log
from mz_fxsys import payments_api, user_api
from myproject import settings
import time


@dec_login_required
@handle_http_response_exception(501)
def get_payments_list(request):
    """查询"""

    payments_type = get_param_by_request(request.GET, 'payments_type', 0, int)
    start_date = get_param_by_request(request.GET, 'start_date', '', str)
    end_date = get_param_by_request(request.GET, 'end_date', '', str)
    user_id = get_param_by_request(request.GET, 'user_id', 0, int)
    page_index = get_param_by_request(request.GET, 'page_index', 1, int)
    action = get_param_by_request(request.GET, 'action', 'search', str)

    # user_input = get_param_by_request(request.GET, 'user_input', '', str)
    #
    # if user_input !='':
    #     user_id_by_mobile = select_userID_by_mobile(user_input,user_input).result()
    #     if user_id_by_mobile != None:
    #         user_id_by_mobile = user_id_by_mobile['id']
    #         user_id = user_id_by_mobile
    #     else:
    #         user_id = 9999
    if action == 'add':
        return render(request, 'mz_fxsys/payments_edit.html', {'action': action})

    payments = payments_api.select_payments_by_page(page_index, settings.PAGE_SIZE, payments_type, start_date, end_date,
                                                    user_id)

    if not payments.is_error():
        log.info('{username},查看了收支明细.--三级分销系统'.format(username=request.session.get('username', '')))
        users = user_api.get_all_user()
        if not users.is_error():
            for u in users.result():
                for p in payments.result()['result']:
                    if str(u['id']) == str(p['user_id']):
                        p['username'] = u['username']
                        p['full_name'] = u['full_name']
        data = {
            "payments": payments.result()['result'],
            "payments_type": payments_type,
            "start_date": start_date,
            "end_date": end_date,
            "user_id": user_id,
            # 'user_input': user_input,
            "page": {
                "page_index": page_index, "rows_count": payments.result()['rows_count'],
                "page_size": settings.PAGE_SIZE, "page_count": payments.result()['page_count']
            },
        }
        return render(request, 'mz_fxsys/payments_list.html', data)


# －－－－ 新增定量返现金额 开始　－－－－－－－－－－－　
# @dec_login_required
# @handle_http_response_exception(501)
# def add_quantitation_payments(request):
#     """增加"""
#     user = get_param_by_request(request.POST, 'user', '', str)
#     user_id = user.split('_', 1)[0]
#     order_id = get_param_by_request(request.POST, 'order_id', 0, int)
#     payments_type = get_param_by_request(request.POST, 'payments_type', 0, int)
#     origin = get_param_by_request(request.POST, 'origin', '', str)
#     money = db.api.fxsys.payments.get_quantitation_cash_back_day(user_id)["cash_back_day"]
#     date = get_param_by_request(request.POST, 'date', '', str)
#
#     result = db.api.fxsys.payments.add_payments(user_id, order_id, money, payments_type, origin, date)
#     username = request.session.get("username", "")
#     if result.is_error():
#         log.warn("add_payments is error user_id:{0} opt:{1}".format(user_id,username))
#     else:
#         log.info("add_payments is error user_id:{0} payments_type:{1} money:{2} opt:{3}".format(user_id, payments_type,
#                                                                                         money, username))
#     return HttpResponseRedirect(reverse('mz_fxsys:get_payments'))


# －－－－ 新增定量返现金额 结束　－－－－－－－－－－－　

@dec_login_required
@handle_http_response_exception(501)
def add_payments(request):
    """增加"""
    user = get_param_by_request(request.POST, 'user', '', str)
    user_id = user.split('_', 1)[0]
    order_id = get_param_by_request(request.POST, 'order_id', 0, int)
    payments_type = get_param_by_request(request.POST, 'payments_type', 0, int)
    origin = get_param_by_request(request.POST, 'origin', '', str)
    money = get_param_by_request(request.POST, 'money', '', str)
    date = get_param_by_request(request.POST, 'date', '', str)

    user_input = get_param_by_request(request.POST, 'user_input', '', str)
    if user_input != '':
        user_id_by_mobile = select_userID_by_mobile(user_input,user_input).result()
        if user_id_by_mobile != None:
            user_id_by_mobile = user_id_by_mobile['id']
            user_id = user_id_by_mobile
        else:
            user_id = 9999

    result = db.api.fxsys.payments.add_payments(user_id, order_id, money, payments_type, origin, date)
    username = request.session.get("username", "")
    if result.is_error():
        log.warn("add_payments is error user_id:{0} opt:{1}".format(user_id, username))
    else:
        log.info("add_payments is error user_id:{0} payments_type:{1} money:{2} opt:{3}".format(user_id, payments_type,
                                                                                                money, username))
    return HttpResponseRedirect(reverse('mz_fxsys:get_payments'))


def del_payments(request):
    """删除收支明细"""

    _id = get_param_by_request(request.GET, "id", 0, int)
    # user_id = get_param_by_request(request.GET, 'user_id', 0, int)
    # action = get_param_by_request(request.GET, 'action', '', str)

    result = db.api.fxsys.payments.delete_payments_by_id(_id)
    username = request.session.get("username", "")
    if result.is_error():
        log.warn("delete_payments_by_id is error id:{0} opt:{1}".format(id, username))
    else:
        log.info("{username}删除id为{id}的收支明细。--分销系统".format(username=request.session.get("username", ""), id=_id))
        return HttpResponseRedirect(reverse("mz_fxsys:get_payments"))

# def update_rebate_in_asset(user_id):
#     total_rebate = payments_api.get_total_rebate(user_id)
#     if not total_rebate.is_error():
#         update = payments_api.update_total_rebate_in_asset(user_id, total_rebate.result()['total_rebate'])
#         if update.is_error():
#             return True
#     return False
