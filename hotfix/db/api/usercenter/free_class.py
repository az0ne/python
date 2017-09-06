# -*- coding: utf-8 -*-
"""
@version: 2016/6/12 0012
@author: lewis
@contact: lewis@maiziedu.com
@file: free_class.py
@time: 2016/6/12 0012 19:18
@note:  ??
"""
from db.api.apiutils import dec_get_cache, dec_make_conn_cursor, APIResult
from db.cores.cache import cache
from utils.logger import logger


def get_free_class_list(teacher_id, page_index, page_size):
    """
    获取老师的免费试学班级
    :param teacher_id:
    :param page_index: 当前页码(int)
    :param page_size: 每页条数(int)
    :return:
    """
    # 因为查询结果会按照班级再次统计，因此查询是要X2
    start_index = (page_index - 1) * page_size * 2  # 开始条数
    page_size = page_size * 2
    # cache_key = 'get_free_class_list_%s' % teacher_id
    # @dec_get_cache(cache_key)
    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
            SELECT
                _class.id,
                _class.name AS class_name,
                _class.meeting_duration,
                career.name AS career_course_name,
                c_m.content,
                c_m.startline,
                c_m.`status` AS class_meeting_status,
                liveroom.teacher_join_url AS join_url,
                liveroom.teacher_token AS token

            FROM
                    mz_lps_class AS _class
            LEFT JOIN mz_course_careercourse AS career ON career.id = _class.career_course_id
            LEFT JOIN mz_lps3_classmeetingrelation AS c_m_rel ON c_m_rel.class_id = _class.id
            LEFT JOIN mz_lps3_classmeeting AS c_m ON c_m.id = c_m_rel.class_meeting_id
            LEFT JOIN mz_lps3_liveroom as liveroom ON liveroom.class_meeting_id = c_m.id
            LEFT JOIN mz_lps_classteachers AS ct ON _class.id = ct.teacher_class_id
            WHERE
                    ct.teacher_id=%s
                    AND _class.meeting_enabled=True
                    AND _class.class_type=3
                    AND _class.lps_version=3.0
            GROUP BY _class.id,c_m.id
            ORDER BY _class.id Desc
            LIMIT %s,%s
        """
        try:
            cursor.execute(sql, (teacher_id, start_index, page_size))
            free_class = cursor.fetchall()
            # logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:" % (e, cursor._last_executed))
            raise e

        # set cache
        # cache.set(cache_key, free_class)
        return APIResult(result=free_class)

    return main()


def exist_free_class(career_course_id, teacher_id, first_date, answer_date):
    """
    获取老师的免费试学班级
    :param teacher_id:
    :return:
    """

    @dec_make_conn_cursor
    def main(conn, cursor):
        sql = """
            SELECT
            1
            FROM
                mz_lps3_classmeeting AS c_m
            LEFT JOIN mz_lps3_classmeetingrelation AS c_m_rel ON c_m_rel.class_meeting_id = c_m.id
            LEFT JOIN mz_lps_class AS _class ON _class.id = c_m_rel.class_id
            LEFT JOIN mz_lps_classteachers AS ct ON _class.id = ct.teacher_class_id
            WHERE
                ct.teacher_id=%s
                AND _class.meeting_enabled=True
                AND _class.class_type=3
                AND _class.lps_version=3.0
                AND _class.career_course_id=%s
                    AND c_m.startline BETWEEN %s AND %s
            LIMIT 1
        """
        try:
            cursor.execute(sql, (teacher_id, career_course_id, first_date + ' ' + '00:00', answer_date + ' ' + '23:23'))
            result = cursor.fetchall()
            # logger.info("query:%s" % cursor._last_executed)
        except Exception as e:
            logger.warn(
                "execute exception: %s. "
                "statement:" % (e, cursor._last_executed))
            raise e

        return APIResult(result=result)

    return main()
