# -*- coding: utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor
import datetime


@dec_timeit
@dec_make_conn_cursor
def list_all_course_order(conn, cursor, page_index, page_size):
    start_index = get_page_info(page_index, page_size)
    sql = """
            SELECT wechat_order.id, pay_price,pay_money,order_no,trade_no,date_pay,date_add,
            pay_status,course_id,wechat_order.union_id,course.name as course_name,wechat_user.nick_name
            FROM mz_wechat_order as wechat_order
            LEFT JOIN mz_wechat_user as wechat_user
            ON wechat_user.union_id=wechat_order.union_id
            LEFT JOIN mz_wechat_course as course
            ON course.id = wechat_order.course_id
            ORDER by course_id DESC ,id DESC
            limit %s, %s
         """
    try:
        cursor.execute(sql, (start_index, page_size,))
        wechat_orders = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_wechat_order
            """, )
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    wechat_orders_dict = {
        "result": wechat_orders,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=wechat_orders_dict)


@dec_timeit
@dec_make_conn_cursor
def search_all_course_order_by_course(conn, cursor, page_index, page_size, order_no):
    start_index = get_page_info(page_index, page_size)
    sql = """
            SELECT wechat_order.id, pay_price,pay_money,order_no,trade_no,date_pay,date_add,
            pay_status,course_id,wechat_order.union_id,course.name as course_name,wechat_user.nick_name
            FROM mz_wechat_order as wechat_order
            LEFT JOIN mz_wechat_user as wechat_user
            ON wechat_user.union_id=wechat_order.union_id
            LEFT JOIN mz_wechat_course as course
            ON course.id = wechat_order.course_id
            WHERE wechat_order.order_no LIKE %s
            ORDER by course_id DESC ,id DESC
            limit %s, %s
         """
    try:
        cursor.execute(sql, (order_no, start_index, page_size,))
        wechat_orders = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_wechat_order
                WHERE order_no like %s
            """, (order_no,))
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    wechat_orders_dict = {
        "result": wechat_orders,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=wechat_orders_dict)


@dec_timeit
@dec_make_conn_cursor
def update_order_pay_status(conn, cursor, order_id, pay_status, date_pay):
    sql = """
            UPDATE mz_wechat_order SET pay_status=%s, date_pay=%s
            WHERE id=%s
         """
    if not date_pay:
        date_pay = datetime.datetime.now()
    try:
        cursor.execute(sql, (pay_status, date_pay, order_id))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_pay_status_by_id(conn, cursor, order_id):
    sql = """
            SELECT pay_status, date_pay FROM mz_wechat_order
            WHERE id=%s
            """
    try:
        cursor.execute(sql, (order_id,))
        pay_status = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=pay_status)
