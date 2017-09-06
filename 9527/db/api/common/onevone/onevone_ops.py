# -*- coding: utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def list_onevone_ops(conn, cursor, page_index, page_size):
    start_index = get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT userprofile.real_name,userprofile.nick_name,userprofile.username,
                        userprofile.mobile,userprofile.qq,userprofile.city_id,ops.time_interval,
                        career.name,ops.datetime,ops.id,ops.mobile as ops_mobile,ops.is_done,
                        CASE ops.source
                            WHEN '1' THEN '1V1服务'
                            WHEN '2' THEN '1V1直播'
                        END AS source_name,
                        CASE ops.time_interval
                            WHEN '1' THEN '午休'
                            WHEN '2' THEN '下午'
                            WHEN '3' THEN '下班'
                        END AS time_interval_name,
                        CASE ops.is_work
                            WHEN '0' THEN '在读'
                            WHEN '1' THEN '在职'
                        END AS type_name,
                        CASE ops.is_done
                            WHEN '0' THEN '未处理'
                            WHEN '1' THEN '已处理'
                        END AS is_done_name
                FROM mz_onevone_ops as ops
                LEFT JOIN mz_lps4_career as career
                ON ops.career_id=career.id
                LEFT JOIN mz_user_userprofile as userprofile
                ON ops.user_id = userprofile.id
                ORDER BY ops.id DESC
                limit %s,%s

            """, (start_index, page_size,))
        ops = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_onevone_ops
            """)
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    ops_dict = {
        "result": ops,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=ops_dict)



@dec_timeit
@dec_make_conn_cursor
def get_all_onevone_ops(conn, cursor):
    try:
        cursor.execute(
            """
                SELECT userprofile.real_name,userprofile.nick_name,userprofile.username,
                        userprofile.mobile,userprofile.qq,userprofile.city_id,ops.time_interval,
                        career.name,ops.datetime,ops.id,ops.mobile as ops_mobile,ops.is_done,
                        CASE ops.source
                            WHEN '1' THEN '1V1服务'
                            WHEN '2' THEN '1V1直播'
                        END AS source_name,
                        CASE ops.time_interval
                            WHEN '1' THEN '午休'
                            WHEN '2' THEN '下午'
                            WHEN '3' THEN '下班'
                        END AS time_interval_name,
                        CASE ops.is_work
                            WHEN '0' THEN '在读'
                            WHEN '1' THEN '在职'
                        END AS type_name,
                        CASE ops.is_done
                            WHEN '0' THEN '未处理'
                            WHEN '1' THEN '已处理'
                        END AS is_done_name
                FROM mz_onevone_ops as ops
                LEFT JOIN mz_lps4_career as career
                ON ops.career_id=career.id
                LEFT JOIN mz_user_userprofile as userprofile
                ON ops.user_id = userprofile.id
                ORDER BY ops.id DESC

            """)
        ops = cursor.fetchall()
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=ops)


@dec_timeit
@dec_make_conn_cursor
def change_ops_is_done(conn, cursor, ops_id):
    try:
        cursor.execute(
            """
                UPDATE mz_onevone_ops SET is_done=(NOT is_done)
                WHERE id=%s
            """, (ops_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def change_ops_is_done_to_1(conn, cursor, ops_id):
    try:
        cursor.execute(
            """
                UPDATE mz_onevone_ops SET is_done=1
                WHERE id=%s
            """, (ops_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)
