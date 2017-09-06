# -*- coding: utf-8 -*-

import datetime

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_make_conn_cursor
from db.cores.mongodbconn import get_mongo_db


@dec_timeit('add_or_create_third_party_user')
@dec_make_conn_cursor
def create_or_update_third_party_user(conn, cursor, partner, openid, token, nickname='unknown',
                                      date_add=None, user_id=None):
    """
    @brief 创建或者更新thirdpartyuser的用户记录.如果无记录,则插入新的记录,否则,就更新记录

    :param partner:
    :param openid:
    :param token:
    :param nickname:
    :param date_add:
    :param user_id:
    :return:

    @note 因数据库设计并未指定非空字段的默认值, 此处将nickname的默认值设为'unknown'
    @todo 更新数据库设计的错误
    """
    sql = '''
        INSERT INTO mz_user_thirdpartyuser (partner, openid, nickname, token, date_add, user_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE token=%s
        '''
    date_add = date_add if date_add else datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ps = [partner, openid, nickname, token, date_add, user_id, token]
    if nickname != 'unknown':
        sql = '%s%s' % (sql, ', nickname=%s')
        ps.append(nickname)
    if user_id:
        sql = '%s%s' % (sql, ', user_id=%s')
        ps.append(user_id)

    try:
        cursor.execute(sql, ps)
        conn.commit()
        log.debug("query:%s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:" % (e, cursor._last_executed))
        raise e


@dec_timeit('add_or_create_third_party_user')
@dec_make_conn_cursor
def get_teacher_info(conn, cursor, course_id):
    """
    根据课程ID获得授课老师的ID，再到userprofile中去查询老师信息
    :param conn:
    :param cursor:
    :param course_id: 课程ID
    :return: 返回老师昵称，老师头像，老师介绍
    """
    try:
        cursor.execute(
            """
                SELECT
                    id,
                    nick_name,
                    avatar_url,
                    description
                FROM
                    mz_user_userprofile
                WHERE
                    id = (
                        SELECT
                            teacher_id
                        FROM
                            mz_course_course
                        WHERE
                            id = %s
                    )
            """, (course_id,)
        )
        teacher_info = cursor.fetchone()
        # log.debug("query:%s" % cursor.statement)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=teacher_info)


@dec_timeit('get_user_by_id')
@dec_make_conn_cursor
def get_user_by_id(conn, cursor, _id):
    """
    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
         cursor.execute(
            """
            SELECT
              nick_name,
              avatar_url,
              description,
              real_name,
              avatar_middle_thumbnall,
              avatar_small_thumbnall,
              mobile,
              token
            FROM mz_user_userprofile
            WHERE id = %s;
            """,(_id,))
         user = cursor.fetchone()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
         raise e
    return APIResult(result=user)


@dec_timeit('insert_user_log')
def insert_user_log(userid, type):
    """
          数据格式为：
    {
        "user_id": user_id,
        "datetime": datetime,
        "type":"register/login"
    }
    :param userid:
    :param type:
    :return:
    """
    db = get_mongo_db('main_website')
    try:
        # 插入
        db.user_log_info.insert({"user_id": userid, "datetime": datetime.datetime.now(), "type": type})
    except Exception as e:
        log.warn(
            "insert user_log_info is failed"
            "exception: %s. "
            "user_id: %s" % (e, userid))
        return APIResult(result=False)

    return APIResult(result=True)
