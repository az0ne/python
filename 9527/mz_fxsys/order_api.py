# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult
from utils import tool
from db.cores.mysqlconn import dec_make_conn_cursor



@dec_timeit
@dec_make_conn_cursor
def update_order_by_id(conn, cursor, id, student_name, date):
    """更新订单信息--通过ID"""
    try:
        cursor.execute("""update mz_fxsys_orders set student_name=%s, date=%s WHERE id=%s""",
                       (student_name, date, id))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def select_order_by_page(conn, cursor, page_index, page_size, order_price, start_date, end_date,user_name):
    """查询订单并分页"""
    start_index = tool.get_page_info(page_index, page_size)
    base_sql = "select {fields} from mz_fxsys_orders as orders" \
               " left join mz_fxsys_user as user on user.id=orders.user_id" \
               " WHERE 1=1"
    condition = ""
    order_by = " ORDER BY id DESC"
    if str(order_price) != '':
        condition += " AND order_price={0}".format(order_price)
    if start_date != '':
        condition += " AND date>='{0}'".format(start_date)
    if end_date != '':
        condition += " AND date<='{0}'".format(end_date)
    if user_name:
        condition += " AND (user.username='{0}' OR user.full_name='{1}' )".format(user_name, user_name)
    limit = " limit {0},{1}".format(start_index, page_size)
    pagination_sql = base_sql.format(fields='orders.*,user.username,user.full_name')
    count_sql = base_sql.format(fields="count(orders.id) as counts")
    if condition != "":
        pagination_sql += condition
        count_sql += condition
    pagination_sql += order_by
    pagination_sql += limit
    try:
        cursor.execute(pagination_sql)
        orders = cursor.fetchall()

        cursor.execute(count_sql)
        rows_count = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    data = {
        "result": orders,
        "rows_count": rows_count['counts'],
        "page_count": tool.get_page_count(rows_count['counts'], page_size)
    }
    return APIResult(result=data)



@dec_timeit
@dec_make_conn_cursor
def select_order_by_id(conn, cursor, order_id):
    """查询某条订单-根据订单ID"""
    try:
        cursor.execute(
            """select id,user_id, order_No, order_price, student_name, `date` from mz_fxsys_orders WHERE id = %s""",
            (order_id,))
        orders = cursor.fetchone()
    except Exception as e:
        log.wanr(
            "execute exception: %s"
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=orders)


@dec_timeit
@dec_make_conn_cursor
def get_order(conn, cursor, order_No=None):
    """
    获取订单信息，可以根据order_No（订单号）过滤数据
    :param order_No: 订单号
    :return: ({},{})
    """
    condition = ""
    base_sql = "select * from mz_fxsys_orders where 1=1"
    if order_No:
        condition += " AND order_No={0}".format(order_No)
    sql = base_sql + condition
    try:
        cursor.execute(sql)
        order = cursor.fetchall()
    except Exception as e:
        log.warn(
            "cursor exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=order)



