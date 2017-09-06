# -*- coding: utf8 -*-
from datetime import datetime

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_make_conn_cursor


@dec_timeit("get_recommend_careers")
@dec_make_conn_cursor
def get_recommend_careers(conn, cursor):
    """
    获取在个人中心下的推荐职业课程
    :param conn:
    :param cursor:
    :return: 职业课程
    """

    sql = """
        SELECT
            career.id,
            career.`name`,
            career.image,
            career.course_color,
            career.short_name
        FROM
            mz_record_recommendcareer r_career
        INNER JOIN mz_course_careercourse career ON career.id = r_career.id
    """

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        log.info("query: %s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise

    return APIResult(result=result)


@dec_timeit("get_count_usercareer")
@dec_make_conn_cursor
def get_count_usercareer(conn, cursor, user_id):
    """
    获取用户是否点击过个人中心推荐职业课程
    :param conn:
    :param cursor:
    :param user_id: 用户id
    :return: 0：未点击，大于0：已点击
    """

    sql = """
        SELECT
            COUNT(id) AS user_count
        FROM
            mz_record_usercareer
        WHERE
            user_id = %s
    """

    try:
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()['user_count']
        log.info("query: %s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise

    return APIResult(result=result)


@dec_timeit("add_record_usercareer")
@dec_make_conn_cursor
def add_record_usercareer(conn, cursor, user_id, career_id):
    """
    用户在用户中心点击推荐职业课程后，记录点击
    :param conn:
    :param cursor:
    :param user_id: 用户id
    :param career_id: 职业课程id
    :return:
    """

    create_date = datetime.now()

    sql = """
        INSERT INTO mz_record_usercareer (
            user_id,
            career_id,
            create_date
        )
        VALUES (%s, %s, %s)
    """

    try:
        cursor.execute(sql, (user_id, career_id, create_date))
        conn.commit()
        log.info("query: %s" % cursor._last_executed)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor._last_executed))
        raise

    return APIResult(result=True)
