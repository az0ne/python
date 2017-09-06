#!/usr/bin/env python
# -*- coding: utf8 -*-
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
import db.api.micro.wechat_course.course_order
from utils.logger import logger as log

ORDER_STATUS = {0: u"未支付",
                1: u"已支付",
                9: u"支付失败"}


@dec_login_required
# @handle_http_response_exception(501)
def wechat_course_order_list(request):
    action = get_param_by_request(request.GET, "action", "query", str)
    page_index = get_param_by_request(request.GET, "page_index", 1, int)
    get_order_no = get_param_by_request(request.GET, "order_no", "", str)
    request.session["wechat_order_url_back"] = request.get_full_path()
    if "search" in action:
        order_no = "%" + get_order_no + "%"
        APIResult = db.api.micro.wechat_course.course_order.search_all_course_order_by_course(page_index=page_index,
                                                                                              page_size=settings.PAGE_SIZE,
                                                                                              order_no=order_no)
    else:
        APIResult = db.api.micro.wechat_course.course_order.list_all_course_order(page_index=page_index,
                                                                              page_size=settings.PAGE_SIZE)
    if APIResult.is_error():
        log.warn("list all course order failed.")
        return render(request, "404.html")
    result = APIResult.result()
    orders = result.get("result", list())
    for order in orders:
        order["pay_status"] = ORDER_STATUS.get(order["pay_status"], u"状态码错误")
    c = {"action": action, "orders": orders, "keyword": get_order_no,
         "page": {"page_index": page_index, "page_size": settings.PAGE_SIZE,
                  "rows_count": result["rows_count"], "page_count": result["page_count"],
                  }
         }
    return render(request, "mz_micro/wechat_course/wechat_course_order_list.html", c)


@dec_login_required
# @handle_http_response_exception(501)
def wechat_course_order_update(request):
    order_id = get_param_by_request(request.POST, "order_id", 0, int)
    pay_status = get_param_by_request(request.POST, "pay_status", -1, int)
    date_pay = get_param_by_request(request.POST, "date_pay", "", str)
    if not pay_status < 0:
        APIResult = db.api.micro.wechat_course.course_order.update_order_pay_status(order_id=order_id,
                                                                                    pay_status=pay_status,
                                                                                    date_pay=date_pay)
        if APIResult.is_error():
            log.warn("update wechat order pay status failed.")
            return render(request, "404.html")
        log.info("%s update wechat order pay status of id is %s to %s success!" % (
        request.session.get('username', ''), order_id, pay_status))
    return HttpResponseRedirect(
        request.session.get('wechat_order_url_back', reverse('mz_wechat:wechat_course_order_list')))


@dec_login_required
@handle_http_response_exception(501)
def wechat_course_order_edit(request):
    order_id = get_param_by_request(request.GET, "order_id", 0, int)
    APIResult = db.api.micro.wechat_course.course_order.get_pay_status_by_id(order_id)
    if APIResult.is_error():
        log.warn("get pay status by id failed")
        return render(request, "404.html")
    result = APIResult.result()
    pay_status = result.get('pay_status')
    date_pay = result.get('date_pay')
    print pay_status
    c = dict(pay_status=pay_status, order_id=order_id, date_pay=date_pay)
    return render(request, "mz_micro/wechat_course/wechat_course_order_edit.html", c)
