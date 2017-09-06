# -*- coding: utf-8 -*-

import xlwt
from datetime import datetime
from mz_pay.models import UserPurchase

title_lst = [u'序号',
             u'姓名',
             u'麦子账号',
             u'班级编号',
             u'支付平台',
             u'支付平台账号',
             u'交易号',
             u'官网价',
             u'优惠金额',
             u'合同价',
             u'试学款时间',
             u'试学支付金额',
             u'尾款时间',
             u'支付金额',
             u'账龄']

title_gap = {u'序号': 0,
             u'姓名': 1,
             u'麦子账号': 1,
             u'班级编号': 1,
             u'支付平台': 2,
             u'支付平台账号': 2,
             u'交易号':4,
             u'官网价': 1,
             u'优惠金额': 1,
             u'合同价': 1,
             u'试学款时间': 1,
             u'试学支付金额': 1,
             u'尾款时间': 1,
             u'支付金额': 1,
             u'账龄': 1}


def _create_title(sheet):
    font_bold = xlwt.Font()
    alignment = xlwt.Alignment()
    alignment.horz = xlwt.Alignment.HORZ_CENTER
    font_bold.bold = True
    style_bold = xlwt.XFStyle()
    style_title = xlwt.XFStyle()
    style_bold.font = font_bold
    style_title.font = font_bold
    style_title.alignment = alignment

    col = 0
    for title in title_lst:
        sheet.write_merge(0, 0, col, col + title_gap[title], title, style=style_title)
        col = col + title_gap[title] + 1


def _create_body(sheet, year, month):
    all_orders = UserPurchase.objects.filter(pay_status=1)  # 所以已经支付订单
    filter_orders = all_orders.filter(date_pay__year=year, date_pay__month=month)  # 当前月已经支付订单
    order_exported = set()

    row = 1
    for order in filter_orders:
        if order.id in order_exported:
            continue

        #当月全款
        full_orders = filter_orders.filter(user_id=order.user_id,
                                           pay_careercourse_id=order.pay_careercourse_id,
                                           pay_type=0)
        #首付款
        first_orders = all_orders.filter(user_id=order.user_id,
                                         pay_careercourse_id=order.pay_careercourse_id,
                                         pay_type=1)
        #当前月尾款
        current_final_orders = filter_orders.filter(user_id=order.user_id,
                                                    pay_careercourse_id=order.pay_careercourse_id,
                                                    pay_type=2)
        #无就业全款
        no_employment_orders = filter_orders.filter(user_id=order.user_id,
                                                   pay_careercourse_id=order.pay_careercourse_id,
                                                   pay_type=6)
        #无就业首付款
        no_employment_first_orders = all_orders.filter(user_id=order.user_id,
                                                 pay_careercourse_id=order.pay_careercourse_id,
                                                 pay_type=7)
        # #当前月首付款
        # current_first_orders = filter_orders.filter(user_id=order.user.id,
        #                          pay_class_id=order.pay_class.id,
        #                          pay_type=1)

        col = 0
        #序号
        sheet.write_merge(row, row, col, col + title_gap[u'序号'], str(row))
        col = col + title_gap[u'序号'] + 1
        #姓名
        sheet.write_merge(row, row, col, col + title_gap[u'姓名'], (order.user.real_name or order.user.nick_name))
        col = col + title_gap[u'姓名'] + 1
        #麦子账号
        sheet.write_merge(row, row, col, col + title_gap[u'麦子账号'], order.user.username)
        col = col + title_gap[u'麦子账号'] + 1
        #班级编号
        sheet.write_merge(row, row, col, col + title_gap[u'班级编号'], order.pay_class.coding)
        col = col + title_gap[u'班级编号'] + 1
        #支付平台
        pay_way = ''
        for full_order in full_orders:
            pay_way = pay_way + UserPurchase.PAY_WAYS[full_order.pay_way] + ','
            order_exported.add(full_order.id)
        # for current_first_order in current_first_orders:
        #     pay_way = pay_way + UserPurchase.PAY_WAYS[current_first_order.pay_way] + ','
        #     order_exported.add(current_first_order.id)
        for current_final_order in current_final_orders:
            pay_way = pay_way + UserPurchase.PAY_WAYS[current_final_order.pay_way] + ','
            order_exported.add(current_final_order.id)
        for final_order in first_orders:
            pay_way = pay_way + UserPurchase.PAY_WAYS[final_order.pay_way] + ','
            order_exported.add(final_order.id)
        for no_employment_first_order in no_employment_first_orders:
            pay_way = pay_way + UserPurchase.PAY_WAYS[no_employment_first_order.pay_way] + ','
        for no_employment_order in no_employment_orders:
            pay_way = pay_way + UserPurchase.PAY_WAYS[no_employment_order.pay_way] + ','
        sheet.write_merge(row, row, col, col + title_gap[u'支付平台'], pay_way)
        col = col + title_gap[u'支付平台'] + 1
        #支付平台账号
        payment_account = ''
        for full_order in full_orders:
            payment_account = payment_account + (full_order.payment_account or '') + ','
        # for current_first_order in current_first_orders:
        #     payment_account = payment_account + (current_first_order.payment_account or '') + ','
        for current_final_order in current_final_orders:
            payment_account = payment_account + (current_final_order.payment_account or '') + ','
        for final_order in first_orders:
            payment_account = payment_account + (final_order.payment_account or '') + ','
        for no_employment_order in no_employment_orders:
            payment_account = payment_account + (no_employment_order.payment_account or '') + ','
        for no_employment_first_order in no_employment_first_orders:
            payment_account = payment_account + (no_employment_first_order.payment_account or '') + ','
        sheet.write_merge(row, row, col, col + title_gap[u'支付平台账号'], payment_account)
        col = col + title_gap[u'支付平台账号'] + 1
        #交易号
        trade_no = ''
        for full_order in full_orders:
            trade_no = trade_no + (full_order.trade_no or '') + ','
        # for current_first_order in current_first_orders:
        #     trade_no = trade_no + (current_first_order.trade_no or '') + ','
        for current_final_order in current_final_orders:
            trade_no = trade_no + (current_final_order.trade_no or '') + ','
        for final_order in first_orders:
            trade_no = trade_no + (final_order.trade_no or '') + ','
        for no_employment_order in no_employment_orders:
            trade_no = trade_no + (no_employment_order.trade_no or '') + ','
        for no_employment_first_order in no_employment_first_orders:
            trade_no + trade_no + (no_employment_first_order.trade_no or '') + '，'
        sheet.write_merge(row, row, col, col + title_gap[u'交易号'], trade_no)
        col = col + title_gap[u'交易号'] + 1

        #官网价
        if 0 == order.pay_type:
            net_price = _handle_none(order.net_price)
        elif 6 == order.pay_type:
            net_price = _handle_none(order.net_price)
        else:
            if first_orders:
                net_price = _handle_none(first_orders[0].net_price)
                order_exported.add(first_orders[0].id)
            elif no_employment_first_orders:
                net_price = _handle_none((first_orders[0].net_price))
                order_exported.add(no_employment_first_orders[0].id)
            else:
                net_price = u'无试学款'
        sheet.write_merge(row, row, col, col + title_gap[u'官网价'], net_price)
        col = col + title_gap[u'官网价'] + 1
        #优惠金额
        if 0 == order.pay_type:
            discounted_price = _handle_none(order.discounted_price)
        elif 6 == order.pay_type:
            discounted_price = _handle_none(order.discounted_price)
        else:
            if first_orders:
                discounted_price = _handle_none(first_orders[0].discounted_price)
            elif no_employment_first_orders:
                discounted_price = _handle_none(no_employment_first_orders[0].discounted_price)
            else:
                discounted_price = u'无试学款'
        sheet.write_merge(row, row, col, col + title_gap[u'优惠金额'], discounted_price)
        col = col + title_gap[u'优惠金额'] + 1
        #合同价
        if 0 == order.pay_type:
            contract_price = _handle_none(order.contract_price)
        elif 6 == order.pay_type:
            contract_price = _handle_none(order.contract_price)
        else:
            if first_orders:
                contract_price = _handle_none(first_orders[0].contract_price)
            elif no_employment_first_orders:
                contract_price = _handle_none(no_employment_first_orders[0].contract_price)
            else:
                contract_price = u'无试学款'
        sheet.write_merge(row, row, col, col + title_gap[u'合同价'], contract_price)
        col = col + title_gap[u'合同价'] + 1
        #试学款时间
        if 0 == order.pay_type:
            date_first_pay = u'全款'
        elif 6 == order.pay_type:
            date_first_pay = u'无就业全款'
        elif 1 == order.pay_type:
            date_first_pay = order.date_pay.strftime('%Y/%m/%d') if order.date_pay else ''
        elif 7 == order.pay_type:
            date_first_pay = order.date_pay.strftime('%Y/%m/%d') if order.date_pay else ''
        elif 2 == order.pay_type:
            if first_orders:
                date_first_pay = first_orders[0].date_pay.strftime('%Y/%m/%d') if first_orders[0].date_pay else ''
                order_exported.add(first_orders[0].id)
            elif no_employment_first_orders:
                date_first_pay = no_employment_first_orders[0].date_pay.strftime('%Y/%m/%d') if no_employment_first_orders[0].date_pay else ''
            else:
                date_first_pay = u'无试学款'
        else:
            date_first_pay = u'无试学款'
        sheet.write_merge(row, row, col, col + title_gap[u'试学款时间'], date_first_pay)
        col = col + title_gap[u'试学款时间'] + 1

        #试学支付金额
        if 0 == order.pay_type:
            first_pay_money = '0'
        elif 6 == order.pay_type:
            first_pay_money = '0'
        elif 7 == order.pay_type:
            first_pay_money = str(order.pay_money)
        elif 1 == order.pay_type:
            first_pay_money = str(order.pay_money)
        elif 2 == order.pay_type:
            if first_orders:
                first_pay_money = str(first_orders[0].pay_money)
            elif no_employment_first_orders:
                first_pay_money = str(no_employment_first_orders[0].pay_money)
            else:
                first_pay_money = ''
        else:
            first_pay_money = u'无试学款'
        sheet.write_merge(row, row, col, col + title_gap[u'试学支付金额'], first_pay_money)
        col = col + title_gap[u'试学支付金额'] + 1

        #尾款时间
        if 0 == order.pay_type or 2 == order.pay_type or 6 == order.pay_type:
            date_final_pay = order.date_pay.strftime('%Y/%m/%d') if order.date_pay else ''
        elif 1 == order.pay_type:
            if current_final_orders:
                date_final_pay = current_final_orders[0].date_pay.strftime('%Y/%m/%d') if current_final_orders[0].date_pay else ''
                order_exported.add(current_final_orders[0].id)
            else:
                date_final_pay = u'有应收'
        elif 7 == order.pay_type:
            if current_final_orders:
                date_final_pay = current_final_orders[0].date_pay.strftime('%Y/%m/%d') if current_final_orders[0].date_pay else ''
        else:
            date_final_pay = u'无试学款'
        sheet.write_merge(row, row, col, col + title_gap[u'尾款时间'], date_final_pay)
        col = col + title_gap[u'尾款时间'] + 1

        #支付金额
        if 1 == order.pay_type and current_final_orders:
            pay_money = current_final_orders[0].pay_money
        elif 7 == order.pay_type and current_final_orders:
            pay_money = current_final_orders[0].pay_money
        else:
            pay_money = order.pay_money
        sheet.write_merge(row, row, col, col + title_gap[u'支付金额'], pay_money)
        col = col + title_gap[u'支付金额'] + 1

        #账龄
        if order.pay_type not in[0,6] and \
                (not current_final_orders) and \
                (order.date_pay):

            accounts_time = ''
            if first_orders:
                for first_order in first_orders:
                    if first_order.date_pay:
                        delta_time = datetime.now() - first_order.date_pay
                        accounts_time = str(delta_time.days)
            elif no_employment_first_orders:
                for no_employment_first_order in no_employment_first_orders:
                    if no_employment_first_order.date_pay:
                        delta_time = datetime.now() - no_employment_first_order.date_pay
                        accounts_time = str(delta_time.days)
            else:
                accounts_time = ''

            sheet.write_merge(row, row, col, col + title_gap[u'账龄'], accounts_time)

        row += 1


def get_xls_export(year, month):
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet(u'订单信息-%s年%s月' % (year, month))

    _create_title(sheet)
    _create_body(sheet, year, month)

    return book


def _handle_none(value):
    return str(value) if value else u'未填写'