# -*- coding: utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor

@dec_timeit
@dec_make_conn_cursor
def course_ajax(conn, cursor):
    """
    """

    try:
        cursor.execute(
            """
                SELECT id,name
                FROM mz_course_course WHERE is_active=1
            """)

        course_ajax = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=course_ajax)
