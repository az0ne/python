# -*- coding: utf8 -*-

from db.api.apiutils import APIResult
from db.cores.mysqlconn import dec_make_conn_cursor
from utils.tool import dec_timeit
from utils.logger import logger as log


@dec_make_conn_cursor
@dec_timeit
def get_active_courses(conn, cursor):
    """
    获取所有激活的课查看的课程
    :param conn:
    :param cursor:
    :return:
    """

    sql = """
        SELECT id, `name`
        FROM
            mz_course_course
        WHERE
            is_active = 1
        AND is_click = 1;
    """

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        log.info("query:%s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=result)

