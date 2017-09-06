# -*- coding: utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def get_userprofileinfo_by_id(conn, cursor, user_id):
    """
    获取用户的昵称，头像等信息
    """
    try:
        cursor.execute(
            """
                SELECT nick_name,avatar_small_thumbnall
                FROM mz_user_userprofile
                WHERE id=%s
            """, (user_id,))
        user = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=user)