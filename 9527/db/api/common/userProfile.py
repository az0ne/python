# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def get_statistical(conn, cursor, start_date, end_date):
    """
    获取某一时间断内注册人数和登录人数
    :param conn:
    :param cursor:
    :param start_date: 开始时间
    :param end_date: 结束时间
    :return: 返回注册人数和登录人数
    """
    try:
        cursor.execute(
            """
                select count(last_login) as last_login_num
                from mz_user_userprofile
                WHERE DATE(last_login) BETWEEN %s and %s

            """, (start_date, end_date,)
        )
        last_login_num = cursor.fetchone()["last_login_num"]
        cursor.execute(
            """
                select count(date_joined) as date_joined_num
                from mz_user_userprofile
                WHERE DATE(date_joined) BETWEEN %s and %s
            """, (start_date, end_date,)
        )
        date_joined_num = cursor.fetchone()["date_joined_num"]
        cursor.execute(
            """
                select count(*) as total_count
                from mz_user_userprofile
            """, ()
        )
        total_count = cursor.fetchone()["total_count"]
        statistical_num = dict(last_login_num=last_login_num,
                               date_joined_num=date_joined_num,
                               total_count=total_count)
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=statistical_num)
