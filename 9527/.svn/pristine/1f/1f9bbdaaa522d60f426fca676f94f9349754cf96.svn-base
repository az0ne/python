# -*- coding: utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def select_app_consult_info_stream_by_page(conn, cursor, page_index, page_size):
    """
    分页查询，根据id字倒序排列，用于list页面显示数据
    :param conn: @dec_make_conn_cursor装饰器参数
    :param cursor: @dec_make_conn_cursor装饰器参数
    :param page_index: 当前页码
    :param page_size: 每页条数
    :return: 返回androidversion表所有字段
    """
    # 获取当前页起始数字
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                select `name`, phone, qq, interest, date_publish, source, market_from, `id`
                from mz_common_appconsultinfo_stream
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size)
        )
        consult_info = cursor.fetchall()

        cursor.execute(
            """
                select count(*) as count from mz_common_appconsultinfo_stream
            """
        )
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:

        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    consult_info_dict = {
        "result": consult_info,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=consult_info_dict)


@dec_timeit
@dec_make_conn_cursor
def select_app_consult_info_stream_by_search(conn, cursor, keyword, page_index, page_size):
    """
    分页查询，根据id字倒序排列，用于list页面显示数据
    :param conn: @dec_make_conn_cursor装饰器参数
    :param cursor: @dec_make_conn_cursor装饰器参数
    :param page_index: 当前页码
    :param page_size: 每页条数
    :return: 返回androidversion表所有字段
    """
    # 获取当前页起始数字
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                select `name`, phone, qq, interest, date_publish, source, market_from, `id`
                from mz_common_appconsultinfo_stream
                WHERE source LIKE %s
                ORDER BY id DESC
                limit %s,%s
            """, (keyword, start_index, page_size)
        )
        consult_info = cursor.fetchall()

        cursor.execute(
            """
                select count(*) as count from mz_common_appconsultinfo_stream
                WHERE source LIKE %s
            """, (keyword,)
        )
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:

        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    consult_info_dict = {
        "result": consult_info,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=consult_info_dict)


@dec_timeit
@dec_make_conn_cursor
def del_app_consult_info_stream_by_id(conn, cursor, _id):
    try:
        cursor.execute(
            """
               DELETE FROM mz_common_appconsultinfo_stream
               WHERE id=%s
            """, (_id,)
        )
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)
