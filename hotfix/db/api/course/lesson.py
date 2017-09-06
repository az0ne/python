# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.cache import cache
from db.api.apiutils import APIResult, dec_make_conn_cursor, dec_get_cache


@dec_timeit("get_lessons_by_course_ids_order_by_amount")
@dec_make_conn_cursor
def get_lessons_by_course_ids_order_by_amount(conn, cursor, course_ids):
    """
        returns: tuple:
           ({
              "course_id": ..,
              "s_amount": ..,
              ...
           } ...)
    """

    if not course_ids:
        log.warn("no course_ids.")
        return APIResult(code=True)

    _qsql = """
        SELECT mz_course_lesson.course_id,
               SUM(mz_course_lesson.play_count) AS s_amount
        FROM mz_course_lesson
        WHERE mz_course_lesson.course_id IN (%s)
        GROUP BY mz_course_lesson.course_id
        ORDER BY s_amount DESC
    """
    in_p = ", ".join(map(lambda x: "%s", course_ids))
    qsql = _qsql % (in_p)

    try:
        cursor.execute(qsql, course_ids)
        lessons = cursor.fetchall()
        log.debug("query:%s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:" % (e, cursor.statement))
        raise e

    lesson_dict = {
        "result": lessons,
    }

    return APIResult(result=lesson_dict)


@dec_timeit("update_lesson_play_count")
@dec_make_conn_cursor
def update_lesson_play_count(conn, cursor, lesson_id):
    """
    @brief 更新lesson的play_count
    :param lesson_id:
    :return:
    """
    sql = '''
        UPDATE mz_course_lesson SET play_count = play_count + 1 WHERE id = %s
        '''
    try:
        cursor.execute(sql, (lesson_id,))
        conn.commit()
        data = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)


@dec_timeit("get_lesson_list_by_course_id")
@dec_make_conn_cursor
def get_lesson_list_by_course_id(conn, cursor, course_id):
    """
    根据课程id查询课程章节
    :param conn:
    :param cursor:
    :param course_id:课程ID
    :return:返回课程章节的id,名字，视频地址，学习人数，并根据index和id排序
    """
    try:
        cursor.execute(
            """
            SELECT
                id,
                `name`,
                video_url,
                play_count,
                video_length
            FROM
                mz_course_lesson
            WHERE
                course_id = %s
            ORDER BY
                mz_course_lesson.`index`,
                id
            """, (course_id,)
        )
        lessons = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=lessons)


@dec_timeit("get_lesson_by_id")
@dec_make_conn_cursor
def get_lesson_by_id(conn, cursor, id):
    """
    根据课程章节id查询课程章节
    :param conn:
    :param cursor:
    :param id:课程ID
    :return:返回课程章节的id,名字，视频地址，学习人数，并根据index和id排序
    """
    try:
        cursor.execute(
            """
            SELECT
                id,
                `name`,
                video_url,
                play_count,
                video_length,
                seo_title
            FROM
                mz_course_lesson
            WHERE
                id = %s
            """, (id,)
        )
        lessons = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=lessons)
