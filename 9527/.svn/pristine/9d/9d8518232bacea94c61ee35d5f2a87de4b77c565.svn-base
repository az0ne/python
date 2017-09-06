# -*- coding: utf-8 -*-

import datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse

import db.api.fxsys.order
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
from utils.logger import logger as log
from mz_fxsys import order_api, user_api
from myproject import settings


@dec_login_required
@handle_http_response_exception(501)
def get_order_list(request):
    """查询"""
    id = get_param_by_request(request.GET, 'id', 0, int)
    order_price = get_param_by_request(request.GET, 'order_price', '', str)
    user_name = get_param_by_request(request.GET, 'user_name', "", str)
    start_date = get_param_by_request(request.GET, 'start_date', '', str)
    end_date = get_param_by_request(request.GET, 'end_date', '', str)
    action = get_param_by_request(request.GET, 'action', 'search', str)
    page_index = get_param_by_request(request.GET, 'page_index', 1, int)

    if id != 0:
        order = order_api.select_order_by_id(id)
        if not order.is_error():
            log.info('{username},查看了订单信息，订单号为：{order_No}.--三级分销系统'.format(
                username=request.session.get('username', ''), order_No=order.result()['order_No']))
            data = {'order': order.result(), 'action': action}
            return render(request, 'mz_fxsys/order_edit.html', data)

    if id == 0:
        if action == "add":
            return render(request, 'mz_fxsys/order_edit.html', {'action': action})

        if action == "search":
            orders = order_api.select_order_by_page(page_index, settings.PAGE_SIZE, order_price, start_date, end_date,
                                                        user_name)
            if not orders.is_error():
                log.info('{username},查看了所有订单.--三级分销系统'.format(username=request.session.get('username', '')))
                data = {
                    "orders": orders.result()['result'],
                    "order_price": order_price,
                    "start_date": start_date,
                    "end_date": end_date,
                    "page": {
                        "page_index": page_index, "rows_count": orders.result()['rows_count'],
                        "page_size": settings.PAGE_SIZE, "page_count": orders.result()['page_count']
                    },
                }
                return render(request, 'mz_fxsys/order_list.html', data)


def get_order_by_id(order_id, username):
    order = order_api.select_order_by_id(order_id)
    if not order.is_error():
        log.info('{username},查看订单，订单号：{orderNo}.--三级分销系统'.format(
            username=username, orderNo=order.result()['order_No']))
        return order.result()


@dec_login_required
@handle_http_response_exception(501)
def update_order(request):
    """修改"""
    id = get_param_by_request(request.GET, 'uid', 0, int)
    # user_id = get_param_by_request(request.POST, 'user_id', 0, int)
    # order_No = get_param_by_request(request.POST, 'order_No', '', str)
    # order_price = get_param_by_request(request.POST, 'order_price', '', str)
    student_name = get_param_by_request(request.POST, 'student_name' '', str)
    date = get_param_by_request(request.POST, 'date', '', str)

    order = order_api.update_order_by_id(id, student_name, date)

    if not order.is_error():
        log.info('{username},修改了订单.订单id：{id}--三级分销系统'.format(
            username=request.session.get('username', ''), id=id))
        return HttpResponseRedirect(reverse('mz_fxsys:get_order'))


@dec_login_required
@handle_http_response_exception(501)
def del_order(request):
    """删除"""
    id = get_param_by_request(request.GET, 'id', 0, int)
    order_No = get_param_by_request(request.GET, 'order_No', '', str)

    order = db.api.fxsys.order.del_order(id)
    if not order.is_error():
        log.info('{username},删除了订单.订单号：{id} 合同号:{order_No}--三级分销系统'.format(
            username=request.session.get('username', ''), id=id, order_No=order_No))
    return HttpResponseRedirect(reverse('mz_fxsys:get_order'))



@dec_login_required
@handle_http_response_exception(501)
def add_order(request):
    """新增新的订单"""
    # uid = get_param_by_request(request.GET, 'uid', 0, int)
    user = get_param_by_request(request.POST, 'user', '0_0', str)
    user_id = user.split('_', 1)[0]
    # username = user.split('_', 1)[1]
    order_No = get_param_by_request(request.POST, 'order_No', '', str)
    order_price = get_param_by_request(request.POST, 'order_price', '', str)
    student_name = get_param_by_request(request.POST, 'student_name' '', str)
    date = get_param_by_request(request.POST, 'date', '', str)
    order = db.api.fxsys.order.add_order(user_id, order_No, order_price, student_name, date)
    if order.is_error():
        log.warn("add_order is error user_id:{0} ")
    log.info('{username},新增了一条订单，订单号为：{order_No}.'.format(
        username=request.session.get('username', ''), order_No=order_No))
    return HttpResponseRedirect(reverse('mz_fxsys:get_order'))


# def add_brokerage(user_id, student_name, order_No, username, money):
#     """添加推广佣金"""
#
#     before_brokerage_money = 0  # 以前推广获得的佣金
#     total_reward = 0
#
#     # 获取以前总收益额
#     before_total_profit = api.get_total_profit_from_payments(user_id)
#     if not before_total_profit.is_error():
#         if before_total_profit.result():
#             before_brokerage_money = before_total_profit.result()['total_profit']
#     # 获取订单号对应的订单id
#     order_id = order_api.get_order_id_by_orderNo(order_No)
#     if not order_id.is_error():
#
#         # 获取该用户的爷奶id,用户添加领导奖、感恩奖
#         # user = user_api.select_user_by_id(user_id)
#         # if not user.is_error():
#             # 领导奖
#             # if int(user.result()['grandparent_id']) != 0:
#             #     add_leading_result = add_leading(user.result()['grandparent_id'], order_id.result()['id'],
#             #                                      student_name, float(money) * constant_pool.AWARD_PROPORTION['leading'])
#             #     if not add_leading_result:
#             #         log.warn("{0} 的领导奖添加失败，来自于{1}推广佣金，订单号为：{2}.--三级分销系统".format(
#             #             user.result()['grandparent_id']), user_id, order_No)
#
#             # 感恩奖
#             # if int(user.result()['parent_id']) != 0:
#             #
#             #     add_thanksGiving_result = add_thanksGiving_award(user.result()['parent_id'],
#             #                                                      order_id.result()['id'], student_name,
#             #                                                      float(money) * constant_pool.AWARD_PROPORTION[
#             #                                                          'thanksGiving'])
#             #     if not add_thanksGiving_result:
#             #         log.warn("{0} 的感恩奖添加失败，来自于{1}推广佣金，订单号为：{2}.--三级分销系统".format(
#             #             user.result()['grandparent_id']), user_id, order_No)
#             #     else:
#             #         money = float(money) * 0.97
#
#         # 插入推广佣金
#         payments = api.add_spread_brokerage(user_id, order_id.result()['id'], student_name, money,
#                                             money + float(before_brokerage_money))
#
#         if not payments.is_error():
#             log.info('{username},新增了{fxsys_user}推广佣金，来自订单“{order_No}”.--三级分销系统'.format(
#                 username=username, fxsys_user=user_id, order_No=order_No))
#
#         # 更新asset表中的总收益、总奖励、今日奖励
#         tool.update_reward_asset(user_id, datetime.date.today())
#
#         return True
#
#     else:
#         log.warn("{0} 的推广佣金添加失败，来自于订单号：{1}.--三级分销系统".format(user_id, order_No))
#     return False


# def add_leading(user_id, order_id, origin, leading_award):
#     """
#     添加一条领导奖
#     :param user_id: 用户ID
#     :param order_id: 来源的订单ID
#     :param origin: 来源于哪个人
#     :param leading_award: 领导奖金额
#     :return: 返回操作结果（True/False）
#     """
#     # 获取该用户的累计金额
#     total_profit = api.get_total_profit_from_payments(user_id)
#     if not total_profit.is_error():
#         add_leading_result = api.add_leading_award(user_id, order_id, origin, leading_award,
#                                                    leading_award + float(total_profit.result()['total_profit']))
#         if not add_leading_result.is_error():
#             # 更新asset表中的总收益、总奖励、今日奖励
#             tool.update_reward_asset(user_id, datetime.date.today())
#             return True
#     return False


# def add_thanksGiving_award(user_id, order_id, origin, thinkGiving_award):
#     """
#     添加一条感恩奖
#     :param user_id: 用户ID
#     :param order_id: 来源的订单ID
#     :param origin: 来源于哪个人
#     :param thinkGiving_award: 领导奖金额
#     :return: 返回操作结果（True/False）
#     """
#
#     # 获取用户的累计金额
#     total_profit = api.get_total_profit_from_payments(user_id)
#
#     if not total_profit.is_error():
#         add_thanksGiving_award_result = api.add_thankGiving_award(user_id, order_id, origin, thinkGiving_award,
#                                                                   thinkGiving_award + float(
#                                                                       total_profit.result()['total_profit']))
#         if not add_thanksGiving_award_result.is_error():
#             # 更新asset表中的总收益、总奖励、今日奖励
#             tool.update_reward_asset(user_id, datetime.date.today())
#             return True
#     return False


@dec_login_required
def validate_order_No_exist(request):
    """验证订单号是否存在"""

    order_list = []
    order = order_api.get_order()
    if not order.is_error():
        if order.result():
            for o in order.result():
                order_list.append(o['order_No'])
    data = {'result': order_list}
    return JsonResponse(data)


@dec_login_required
def get_order_all(request):
    """
    获取所有的订单号
    return: [{id: xx, order_No: xx}]
    """

    order_list = []
    order = order_api.get_order()
    if not order.is_error():
        if order.result():
            for o in order.result():
                order_list.append({'id': o['id'], 'order_No': o['order_No']})
    data = {'result': order_list}
    return JsonResponse(data)
