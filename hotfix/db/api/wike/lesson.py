# -*- coding: utf-8 -*-

from db.cores.mongodbconn import get_mongo_db
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_make_conn_cursor


@dec_timeit("get_lessons_by_course_id")
@dec_make_conn_cursor
def get_lesson_by_id(conn, cursor, course_id, lesson_id):
    """
    @brief 根据微课课程id获取课程章节
    :param conn:
    :param cursor:
    :param course_id: 微课课程id
    :param lesson_id: 微课课程章节id
    :return:
    """

    sql = '''
        SELECT
          l.*,
          teacher.id AS teacher_id,
          teacher.nick_name,
          teacher.username,
          teacher.avatar_url,
          c.name AS course_name,
          c.price
        FROM mz_wechat_lesson AS l
          INNER JOIN mz_wechat_course AS c ON c.id = l.course_id
          INNER JOIN mz_user_userprofile AS teacher ON teacher.id = c.teacher_id
        WHERE c.id = %s AND l.id = %s;
    '''

    try:
        cursor.execute(sql, (course_id, lesson_id))
        data = cursor.fetchone()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data) if data else APIResult(code=False)


@dec_timeit("get_lessons_by_course_id")
@dec_make_conn_cursor
def get_lessons_by_course_id(conn, cursor, course_id):
    """
    @brief 根据微课课程id获取课程章节
    :param conn:
    :param cursor:
    :param course_id: 微课课程id
    :return:
    """

    sql = '''
        SELECT *
        FROM mz_wechat_lesson
        WHERE course_id = %s
        ORDER BY `index`, id;
    '''

    try:
        cursor.execute(sql, (course_id,))
        data = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)


@dec_timeit("get_first_lesson_by_course_id")
@dec_make_conn_cursor
def get_first_lesson_by_course_id(conn, cursor, course_id):
    """
    @brief 根据微课课程id获取该课程下的第一个章节
    :param conn:
    :param cursor:
    :param course_id: 微课课程id
    :return:
    """

    sql = '''
        SELECT *
        FROM mz_wechat_lesson
        WHERE course_id = %s
        ORDER BY `index`, id
        LIMIT 1;
    '''

    try:
        cursor.execute(sql, (course_id,))
        data = cursor.fetchone()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data) if data else APIResult(code=False)


@dec_timeit("update_lesson_play_count")
@dec_make_conn_cursor
def update_lesson_play_count(conn, cursor, lesson_id):
    """
    @brief 更新章节播放次数
    :param conn:
    :param cursor:
    :param lesson_id: 微课课程章节id
    :return:
    """

    sql = '''
        UPDATE mz_wechat_lesson
        SET play_count = play_count + 1
        WHERE id = %s;
    '''

    try:
        cursor.execute(sql, (lesson_id,))
        conn.commit()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=True)


@dec_timeit("get_reply_count")
def get_reply_count(course_id, union_id):
    """
    获取回复次数并归零
    数据格式为：
    {
        "user_id": union_id,
        "course": {
            "reply_count":
                {
                    str(course_id): value
                }
        }
    }
    :param course_id:
    :param union_id:
    :return:
    """

    db = get_mongo_db('main_website')

    try:
        field = "course.reply_count.{0}".format(course_id)
        count = db.wechat_user_info.find_one({"user_id": union_id},  {field: 1})
        if not count:
            count = 0
        else:
            count = count.get('course', {}).get('reply_count', {}).get(str(course_id), 0)
        # 归零
        db.wechat_user_info.update(
            {"user_id": union_id}, {"$set": {field: 0}}, upsert=True)

    except Exception as e:
        count = 0

    return APIResult(result=count)


@dec_timeit("update_reply_count")
def update_reply_count(course_id, union_id):
    """
    更新回复次数
    :param course_id:
    :param union_id:
    :return:
    """

    db = get_mongo_db('main_website')

    try:
        field = "course.reply_count.{0}".format(course_id)
        db.wechat_user_info.update(
            {"user_id": union_id}, {"$inc": {field: 1}}, upsert=True)

    except Exception as e:
        return APIResult(result=False)

    return APIResult(result=True)
