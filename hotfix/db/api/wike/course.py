# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_make_conn_cursor


@dec_timeit("get_careers")
@dec_make_conn_cursor
def get_careers(conn, cursor):
    """
    @brief 获取微课课程分类
    :param conn:
    :param cursor:
    :return:
    """

    sql = '''
        SELECT *
        FROM mz_wechat_career_course
        ORDER BY `index`, id;
    '''

    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)


@dec_timeit("get_courses")
@dec_make_conn_cursor
def get_courses(conn, cursor):
    """
    @brief 获取所有微课课程
    :param conn:
    :param cursor:
    :return:
    """

    sql = '''
        SELECT
          c.image_url,
          c.id,
          c.name,
          c.career_course_id,
          teacher.id,
          teacher.nick_name,
          teacher.real_name,
          teacher.avatar_url
        FROM mz_wechat_course AS c
          INNER JOIN mz_user_userprofile AS teacher ON teacher.id = c.teacher_id
        WHERE c.is_active = 1;
    '''

    try:
        cursor.execute(sql)
        data = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)


@dec_timeit("get_course_by_id")
@dec_make_conn_cursor
def get_course_by_id(conn, cursor, course_id):
    """
    @brief 根据课程id获取微课课程
    :param conn:
    :param cursor:
    :param course_id: 微课课程id
    :return:
    """

    sql = '''
        SELECT
          c.*,
          teacher.id AS teacher_id,
          teacher.nick_name,
          teacher.real_name,
          teacher.avatar_url,
          teacher.description AS teacher_description,
          cc.image AS career_image,
          cc.name AS career_name,
          cc.short_name AS career_short_name,
          cc.course_color AS career_background_color
        FROM mz_wechat_course AS c
          INNER JOIN mz_course_careercourse AS cc ON cc.id = c.web_career_id
          INNER JOIN mz_user_userprofile AS teacher ON teacher.id = c.teacher_id
        WHERE c.is_active = 1 AND c.id = %s;
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


@dec_timeit("get_my_course")
@dec_make_conn_cursor
def get_my_course(conn, cursor, union_id):
    """
    @brief 根据微信用户union_id，获取我的课程
    :param conn:
    :param cursor:
    :param union_id: 微信用户union_id
    :return:
    """

    sql = '''
        SELECT
          c.id,
          c.name,
          c.image_url,
          teacher.id AS teacher_id,
          teacher.nick_name,
          teacher.username
        FROM mz_wechat_order AS o
          INNER JOIN mz_wechat_course AS c ON c.id = o.course_id
          INNER JOIN mz_user_userprofile AS teacher ON teacher.id = c.teacher_id
        WHERE o.union_id = %s and o.pay_status=1;
    '''

    try:
        cursor.execute(sql, (union_id,))
        data = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)


@dec_timeit("get_my_course")
@dec_make_conn_cursor
def is_pay(conn, cursor, union_id, course_id):
    """
    @brief 用户是否购买过某微课课程
    :param conn:
    :param cursor:
    :param union_id: 微信用户union_id
    :param course_id: 微课课程id
    :return:
    """

    sql = '''
        SELECT id
        FROM mz_wechat_order
        WHERE union_id = %s AND course_id = %s AND pay_status = 1;
    '''

    try:
        cursor.execute(sql, (union_id, course_id))
        data = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=bool(data))


@dec_timeit("update_lesson_play_count")
@dec_make_conn_cursor
def update_course_play_count(conn, cursor, course_id):
    """
    @brief 更新微课课程播放次数
    :param conn:
    :param cursor:
    :param course_id: 微课课程章d
    :return:
    """

    sql = '''
        UPDATE mz_wechat_course
        SET student_count = student_count + 1
        WHERE id = %s;
    '''

    try:
        cursor.execute(sql, (course_id,))
        conn.commit()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=True)
