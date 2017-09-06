# -*- coding: utf-8 -*-
from datetime import datetime

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_make_conn_cursor


@dec_timeit("get_faq_by_course_id")
@dec_make_conn_cursor
def get_faq_by_course_id(conn, cursor, course_id):
    """
    @brief 根据微课课程id获取课程常见问题
    :param conn:
    :param cursor:
    :param course_id: 微课课程id
    :return:
    """

    sql = '''
        SELECT *
        FROM mz_wechat_course_question
        WHERE course_id = %s;
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


@dec_timeit("get_discuss_by_lesson_id")
@dec_make_conn_cursor
def get_discuss_by_course_id(conn, cursor, course_id):
    """
    @brief 根据微课课程id获取课程问答
    :param conn:
    :param cursor:
    :param course_id: 微课课程id
    :return:
    """

    sql = '''
        SELECT *
        FROM mz_wechat_course_discuss
        WHERE parent_id = 0 AND course_id = %s;
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


@dec_timeit("get_child_discuss")
@dec_make_conn_cursor
def get_child_discuss(conn, cursor, parent_id):
    """
    @brief 根据评论id获取子评论
    :param conn:
    :param cursor:
    :param parent_id: 评论父id
    :return:
    """

    sql = '''
        SELECT *
        FROM mz_wechat_course_discuss
        WHERE parent_id = %s;
    '''

    try:
        cursor.execute(sql, (parent_id,))
        data = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)


@dec_timeit("add_discuss")
@dec_make_conn_cursor
def add_discuss(conn, cursor, course_id, union_id, nick_name,
                avatar_url, content, parent_id):
    """
    @brief 新增评论
    :param conn:
    :param cursor:
    :param course_id: 微课课程id
    :param union_id: 微信用户union_id
    :param nick_name: 微信用户名
    :param avatar_url: 微信用户头像
    :param content: 评论内容
    :param parent_id: 父评论id
    :return:
    """

    sql = '''
        INSERT INTO
          mz_wechat_course_discuss (
            course_id,
            union_id,
            parent_id,
            nick_name,
            avatar_url,
            content,
            date_time
          )
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    '''

    try:
        cursor.execute(sql, (course_id, union_id, parent_id, nick_name,
                             avatar_url, content, datetime.now()))
        conn.commit()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=cursor.lastrowid)


@dec_timeit("get_discuss_by_id")
@dec_make_conn_cursor
def get_discuss_by_id(conn, cursor, discuss_id):
    """
    @brief 根据评论id获取评论
    :param conn:
    :param cursor:
    :param discuss_id: 评论id
    :return:
    """

    sql = '''
        SELECT union_id
        FROM mz_wechat_course_discuss
        WHERE id = %s;
    '''

    try:
        cursor.execute(sql, (discuss_id,))
        data = cursor.fetchone()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)
