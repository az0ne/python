# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor


@dec_timeit("get_career_courses")
@dec_get_cache("get_career_courses")
@dec_make_conn_cursor
def get_course_stage_by_career_course_id(conn, cursor, career_course_id):
    """
    根据职业课程ID，查询该课程的所有阶段
    :param conn:
    :param cursor:
    :param career_course_id:职业课程ID
    :return:返回各个阶段的id，name
    """
    try:
        cursor.execute(
            """
                select id,name from mz_course_stage as stage
                WHERE career_course_id=%s AND stage.lps_version = 3.0
                ORDER BY stage.`index`
            """, (career_course_id,)
        )
        courseStages = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s"
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=courseStages)

@dec_timeit('get_course_stage_by_career_course_id_non_3')
@dec_make_conn_cursor
def get_course_stage_by_career_course_id_non_3(conn, cursor, career_course_id):
    """
    @brief 根据职业课程id，获取该课程的　非3.0　的所有阶段

    :param conn:
    :param cursor:
    :param career_course_id:
    :return:

    @brief 该接口服务与老的课程大纲页
    """
    sql = '''
        SELECT id, name, description FROM mz_course_stage AS stage
        WHERE career_course_id = %s AND (lps_version IS NULL OR lps_version != 3.0)
        ORDER BY stage.index
        '''
    try:
        cursor.execute(sql, (career_course_id,))
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s"
            "statement: %s" % (e, cursor._last_executed))
        raise e

    return APIResult(result=result)

