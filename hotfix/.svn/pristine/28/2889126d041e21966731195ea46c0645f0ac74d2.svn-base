# -*- coding: utf-8 -*-
from datetime import datetime

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_make_conn_cursor


@dec_timeit("add_order")
@dec_make_conn_cursor
def add_order(conn, cursor, course_id, union_id,
              pay_price, order_no, pay_status=0):
    """
    @brief 新增订单

    :param conn:
    :param cursor:
    :param course_id: 课程id
    :param union_id: 微信用户union_id
    :param pay_price: 订单金额
    :param order_no: 订单号
    :param pay_status: 支付状态: 未支付=0; 支付成功=1; 支付失败=9
    :return:
    """

    sql = '''
        INSERT INTO
          mz_wechat_order (
            course_id,
            union_id,
            pay_price,
            order_no,
            date_add,
            pay_status
          )
        VALUES (%s, %s, %s, %s, %s, %s);
    '''

    try:
        cursor.execute(sql, (course_id, union_id, pay_price,
                             order_no, datetime.now(), pay_status))
        conn.commit()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=True)


@dec_timeit("update_order")
@dec_make_conn_cursor
def update_order(conn, cursor, order_no, pay_money,
                 trade_no, pay_status=0):
    """
    @brief 修改订单 （用于支付成功后）

    :param conn:
    :param cursor:
    :param order_no: 订单号
    :param pay_money: 支付金额
    :param trade_no: 支付号
    :param pay_status: 支付状态: 未支付=0; 支付成功=1; 支付失败=9
    :return:
    """
    sql_select = """
        SELECT 1 FROM mz_wechat_order WHERE order_no = %s AND pay_status=1 FOR UPDATE
    """
    sql = '''
        UPDATE mz_wechat_order
        SET pay_money = %s, trade_no = %s, date_pay = %s, pay_status = %s
        WHERE order_no = %s;
    '''

    try:
        cursor.execute(sql_select, (order_no,))
        is_exists = cursor.fetchone()
        result = False
        if not is_exists:
            cursor.execute(sql, (pay_money, trade_no, datetime.now(),
                                 pay_status, order_no))
            log.debug('query:%s' % cursor._last_executed)
            result = True
        conn.commit()
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)
