# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult
from utils import tool
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def add_total_revenue(conn, cursor, total_revenue, date):
    """新增某天的总收益额"""
    try:
        cursor.execute(
            "insert into mz_fxsys_total_revenue(total_revenue,`date`,is_exe) VALUES (%s,%s,0)",
            (total_revenue, date))
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
def get_total_revenue_by_date(conn, cursor, date):
    """根据日期获取总收益"""
    try:
        cursor.execute("select * from mz_fxsys_total_revenue where TO_DAYS(date)=TO_DAYS(%s) ORDER BY `date` DESC ",
                       (date,))
        total_revenue = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=total_revenue)


@dec_timeit
@dec_make_conn_cursor
def update_total_revenue(conn, cursor, _id, total_revenue, date):
    """根据id,更新total_revenue信息"""
    try:
        cursor.execute("update mz_fxsys_total_revenue set total_revenue=%s,`date`=%s WHERE id=%s",
                       (total_revenue, date, _id))
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
def select_total_revenue_by_page(conn, cursor, page_index, page_size, date):
    """查询总收益额并分页"""
    start_index = tool.get_page_info(page_index, page_size)
    base_sql = "select {fields} from mz_fxsys_total_revenue WHERE 1=1"
    condition = ""
    order_by = " ORDER BY date DESC"
    if date != '':
        condition += " AND date='{0}'".format(date)

    limit = " limit {0},{1}".format(start_index, page_size)
    pagination_sql = base_sql.format(fields='*')
    count_sql = base_sql.format(fields="count(id) as counts")
    if condition != "":
        pagination_sql += condition
        count_sql += condition
    pagination_sql += order_by
    pagination_sql += limit
    try:
        cursor.execute(pagination_sql)
        total_revenue = cursor.fetchall()

        cursor.execute(count_sql)
        rows_count = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    data = {
        "result": total_revenue,
        "rows_count": rows_count['counts'],
        "page_count": tool.get_page_count(rows_count['counts'], page_size)
    }
    return APIResult(result=data)


@dec_timeit
@dec_make_conn_cursor
def del_total_revenue_by_id(conn, cursor, _id):
    """删除今日总收益额，根据ID"""

    try:
        cursor.execute("delete from mz_fxsys_total_revenue where id=%s", (_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=True)
