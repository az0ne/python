# -*- coding: utf-8 -*-

__author__ = 'changfu'

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_make_conn_cursor

@dec_timeit("get_wike_list")
@dec_make_conn_cursor
def get_wike_list(conn, cursor):
    """
    @brief 获取微课列表
    :param conn:
    :param cursor:
    :return:
    """
    sql = '''
        SELECT
        mc.id, mc.title, mc.status, date_format(mc.start_date, '%c月%e日 %H:%i') as start_date,
        date_format(end_date, '%H:%i') as end_date, mc.back_img, up.nick_name AS teacher_name
        FROM mz_micro_course AS mc
        INNER JOIN mz_user_userprofile AS up
        ON mc.teacher_id = up.id
        WHERE mc.status >= 0
        ORDER BY mc.id DESC
        LIMIT 20
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

@dec_timeit("get_wike")
@dec_make_conn_cursor
def get_wike(conn, cursor, wike_id):
    """

    :param conn:
    :param cursor:
    :param weike_id:
    :return:
    """
    sql = '''
        SELECT mc.id, mc.title, mc.info, mc.playback_img, mc.status, mc.webcast_id, mc.career_id_1, mc.career_id_2, mc.career_id_3, mc.vod_url, mc.student_count, mc.min_student_count, mc.max_student_count,
               up.nick_name, up.description, up.avatar_url, GROUP_CONCAT(cc.short_name, '__', cc.name, '__', cc.image) AS career_course_info
        FROM mz_micro_course AS mc
        INNER JOIN mz_user_userprofile AS up ON mc.teacher_id = up.id
        LEFT JOIN mz_course_careercourse AS cc ON cc.id in (mc.career_id_1, mc.career_id_2, mc.career_id_3)
        WHERE mc.id = %s
        '''
    try:
        cursor.execute(sql, wike_id)
        data = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)

@dec_timeit("update_wike_student_count")
@dec_make_conn_cursor
def update_wike_student_count(conn, cursor, couse_id, student_count):
    """

    :param student_count:
    :return:
    """
    sql = '''
        UPDATE mz_micro_course SET student_count = %s WHERE id = %s
        '''
    try:
        cursor.execute(sql, (student_count, couse_id))
        conn.commit()
        data = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)

@dec_timeit("get_wike_ask_list")
@dec_make_conn_cursor
def get_wike_ask_list(conn, cursor, wike_course_id, openid=None):
    """
    @brief 获取微课问答列表
    :param start_id:　开始的id, 只有这个id之后的才会获取，类似于分页获取
    :return:
    """
    if openid:
        sql = '''
            SELECT a.id, a.nick_name, a.head_image, a.content, a.answer, a.praise_count,
                   (case when isnull(p.id) then 0 else 1 end) AS praised
            FROM mz_micro_course_ask AS a
            INNER JOIN mz_micro_course AS mc
            ON a.micro_course_id = mc.id and mc.id = %s
            LEFT JOIN mz_micro_course_ask_praise AS p
            ON a.id = p.micro_course_ask_id AND p.openid = %s
            ORDER BY a.praise_count DESC
            '''
    else:
        sql = '''
            SELECT a.id, a.nick_name, a.head_image, a.content, a.answer, a.praise_count
            FROM mz_micro_course_ask AS a
            INNER JOIN mz_micro_course AS mc
            ON a.micro_course_id = mc.id and mc.id = %s
            ORDER BY praise_count DESC
            '''
    try:
        if openid:
            cursor.execute(sql, (wike_course_id, openid))
        else:
            cursor.execute(sql, wike_course_id)
        data = cursor.fetchall()
        log.debug('query: %s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    return APIResult(result=data)

@dec_timeit("add_wike_ask")
@dec_make_conn_cursor
def add_wike_ask(conn, cursor, micro_course_id, openid, nick_name, head_image, content, ask_time):
    """
    @brief 新增wike_ask
    :param conn:
    :param cursor:
    :return:
    """
    sql = '''
        INSERT INTO mz_micro_course_ask (micro_course_id, openid, nick_name, head_image, content, ask_time)
        VALUES (%s, %s, %s, %s, %s, %s);
        '''
    sql2 = '''
        SELECT last_insert_id() AS id;
        '''
    try:
        cursor.execute(sql, (micro_course_id, openid, nick_name, head_image, content, ask_time))
        cursor.execute(sql2)
        data = cursor.fetchall()
        conn.commit()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e

    return APIResult(result=data)

    # sql = '''
    #     SELECT last_insert_id() AS id;
    #     '''
    # try:
    #     cursor.execute(sql)
    #     data = cursor.fetchall()
    #     log.debug('query:%s' % cursor._last_executed)
    # except Exception as e:
    #     log.warn(
    #         'execute exception: %s. '
    #         'statement: %s' % (e, cursor._last_executed))
    #     raise e
    #
    # return APIResult(result=data)

@dec_timeit("add_wike_ask_like")
@dec_make_conn_cursor
def add_wike_ask_like(conn, cursor, openid, wike_ask_id):
    """
    @brief 添加微课问答点赞信息
    :param conn:
    :param cursor:
    :param wike_ask_id:　微课问答的id
    :param openid: 微信用户的openid
    :return: 增加之后的微课问答点赞数
    @note 添加点赞信息的步骤为：
    　　　 1. 在表mz_micro_course_ask_praise表中,增加一条记录(openid, wike_ask_id)
          2. 在表mz_micro_course_ask中,更新id为wike_ask_id的记录的字段praise_count,更新方式为+1
    """
    sql = '''
        INSERT INTO mz_micro_course_ask_praise (openid, micro_course_ask_id) values (%s, %s);
        '''
    sql2 = '''
        UPDATE mz_micro_course_ask SET praise_count = praise_count + 1 WHERE id = %s
        '''
    try:
        cursor.execute(sql, (openid, wike_ask_id))
        cursor.execute(sql2, (wike_ask_id, ))
        conn.commit()
        log.debug('query:%s' % cursor._last_executed)
    except cursor.IntegrityError as e:
        log.warn(
            'execute exception: duplicate entry %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e

    return APIResult()

@dec_timeit("get_wike_ask_like_count")
@dec_make_conn_cursor
def get_wike_ask_like_count(conn, cursor, wike_ask_id):
    """
    @brief 获取微课问答的点赞数量
    :param conn:
    :param cursor:
    :param wike_ask_id:
    :return:
    """
    sql = '''
        SELECT praise_count FROM mz_micro_course_ask WHERE id = %s
        '''
    try:
        cursor.execute(sql, wike_ask_id)
        data = cursor.fetchall()
        log.debug('query:%s' % cursor._last_executed)
    except Exception as e:
        log.warn(
            'execute exception: %s. '
            'statement: %s' % (e, cursor._last_executed))
        raise e

    return APIResult(result=data)
