# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult


@dec_timeit
@dec_make_conn_cursor
def insert_career_newad(conn, cursor, image, image_title, title1, title1_url, title2, title2_url, index):
    """
    插入首页大课程广告
    :param conn:
    :param cursor:
    :param image:
    :param image_title:
    :param title1:
    :param title1_url:
    :param title2:
    :param title2_url:
    :param index:
    :return:
    """
    try:
        cursor.execute(
            """
                insert into mz_common_career_newad (image, image_title, title1, title1_url , title2, title2_url, newad_index)
                values (%s,%s,%s,%s,%s,%s,%s)
            """, (image, image_title, title1, title1_url, title2, title2_url, index))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_career_newad(conn, cursor, _id, image, image_title, title1, title1_url, title2, title2_url, index):
    """
    更新首页大课程广告数据
    :param conn:
    :param cursor:
    :param _id:
    :param image:
    :param image_title:
    :param title1:
    :param title1_url:
    :param title2:
    :param title2_url:
    :param index:
    :return:
    """

    try:
        cursor.execute(
            """
                UPDATE mz_common_career_newad
                SET image=%s, image_title=%s, title1=%s, title1_url=%s, title2=%s, title2_url=%s, newad_index=%s
                WHERE id = %s;
            """, (image, image_title, title1, title1_url, title2, title2_url, index, _id))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_career_newad_list(conn, cursor):
    """
    获取首页大课程广告数据
    :param conn:
    :param cursor:
    :return:
    """

    try:
        cursor.execute(
            """
            select * from  mz_common_career_newad
            """
        )
        data = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=data)


@dec_timeit
@dec_make_conn_cursor
def get_career_newad_get_by_id(conn, cursor, _id):
    """
    根据ID获取首页大课程广告数据
    :param conn:
    :param cursor:
    :return:
    """

    try:
        cursor.execute(
            """
            select * from  mz_common_career_newad where id=%s
            """, (_id,)
        )
        data = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=data)


@dec_timeit
@dec_make_conn_cursor
def delete_career_newad(conn, cursor, _id):
    """
    根据ID删除首页大课程广告数据
    :param conn:
    :param cursor:
    :param _id:
    :return:
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_common_career_newad  WHERE id=%s;
            """, (_id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)

