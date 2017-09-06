# -*- coding: utf8 -*-

from utils.logger import logger as log
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor


@dec_make_conn_cursor
def get_careers_by_teacher(conn, cursor, teacher_id):
    """
    根据教师id获取该教师所带的职业课程
    :param conn:
    :param cursor:
    :param teacher_id: 教师id
    :return:
    """
    sql = """
        SELECT
            cc.id,
            cc.`name`,
            cc.short_name,
            COUNT(s.id) AS s_count
        FROM
            mz_lps4_student AS s
        INNER JOIN mz_course_careercourse AS cc ON cc.id = s.career_id
        WHERE
            teacher_id = %s
        GROUP BY cc.id
        ORDER BY s_count DESC
    """

    try:
        cursor.execute(sql, (teacher_id,))
        result = cursor.fetchall()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor._last_executed))
        raise e
    return APIResult(result=result)
