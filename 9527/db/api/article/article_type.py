# -*- coding: utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def insert_articleType(conn, cursor, _id, name, short_name, homepage_img, index):
    """
        插入文章类型表中的id,name,short_name,homepage_img,is_homepage数据
        returns: true/false
    """
    try:
        cursor.execute(
            """
                insert into mz_common_articletype (id,mz_common_articletype.name,short_name,homepage_img,mz_common_articletype.index)
                values (%s,%s,%s,%s,%s);
            """, (_id, name, short_name, homepage_img, index))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_articleType(conn, cursor, _id, name, short_name, homepage_img, index):
    """
    更新文章类型中的name,shortname,is_homepage,homepage_img四个字段
    :return: true/false
    """
    try:
        cursor.execute(
            """
                UPDATE mz_common_articletype AS at
                SET at.name=%s,short_name=%s,homepage_img=%s,at.index=%s
                WHERE id=%s
            """, (name, short_name, homepage_img, index, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_articleType_isCareer(conn, cursor, _id, is_career):
    """
    更新文章类型中的is_career字段,使该类型是否在职业课程页显示
    :param conn:
    :param cursor:
    :param _id:
    :param is_career: bool类型，1为在职业课程页显示，0为不在职业课程页显示
    :return: true/false
    """
    try:
        cursor.execute(
            """
                update mz_common_articletype set is_career=%s WHERE id=%s;
            """, (is_career, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_articleType_isVisible(conn, cursor, _id, is_visible):
    """
    更新文章类型中的is_visible字段,使该类型是否在文章页显示
    :param conn:
    :param cursor:
    :param _id:
    :param is_visible: bool类型，1为在文章页显示，0为不在文章页显示
    :return: true/false
    """
    try:
        cursor.execute(
            """
                update mz_common_articletype set is_visible=%s WHERE id=%s;
            """, (is_visible, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_articleType_isHomepage(conn, cursor, _id, is_homepage):
    """
    更新文章类型中的is_visible字段,使该类型是否在文章页显示
    :param conn:
    :param cursor:
    :param _id:
    :param is_homepage: bool类型，1为在文章页显示，0为不在文章页显示
    :return: true/false
    """
    try:
        cursor.execute(
            """
                update mz_common_articletype set is_homepage=%s WHERE id=%s;
            """, (is_homepage, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def list_articleType(conn, cursor):
    """
        获取所有文章类型数据
    """
    try:
        cursor.execute(
            """
                SELECT id, name,at.index,is_visible,is_career,is_homepage
                FROM mz_common_articletype AS at
            """)
        articleType = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=articleType)


@dec_timeit
@dec_make_conn_cursor
def get_articletype_by_id(conn, cursor, _id):
    """
        根据文章类型ID获取数据
    """

    try:
        cursor.execute(
            """
                SELECT id,name,at.index,is_homepage,short_name,homepage_img
                FROM mz_common_articletype AS at WHERE id = %s
            """, (_id,))
        articleType = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=articleType)


@dec_timeit
@dec_make_conn_cursor
def list_articletype_by_name(conn, cursor, name):
    """
        根据文章类型名称来模糊查询数据
    """
    try:
        cursor.execute(
            """
            SELECT id, name,at.index,is_visible,is_career
            FROM mz_common_articletype AS at
            WHERE name like %s
            """, (name,))
        articleType = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=articleType)


@dec_timeit
@dec_make_conn_cursor
def delete_articleType_by_id(conn, cursor, _id):
    """
        根据文章类型id,删除数据
        returns: true/false
    """
    try:
        cursor.execute(
            """
               DELETE FROM mz_common_articletype WHERE id=%s
            """, (_id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_all_article_type_name(conn, cursor):
    """
    获取所有的文章类型名称和id,用于填充下拉列表框
    :param conn:
    :param cursor:
    :return: 返回文章类型名称和id值
    """
    try:
        cursor.execute(
            """
                select id,name from mz_common_articletype
            """
        )
        article_type = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=article_type)


@dec_timeit
@dec_make_conn_cursor
def get_is_homepage_article_type_name(conn, cursor):
    """
    获取所有的文章类型名称和id,用于填充下拉列表框
    :param conn:
    :param cursor:
    :return: 返回文章类型名称和id值
    """
    try:
        cursor.execute(
            """
                select id,name from mz_common_articletype
                WHERE is_homepage=1
            """
        )
        article_type = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=article_type)


@dec_timeit
@dec_make_conn_cursor
def validate_unique_id(conn, cursor, _id):
    """
    查询该id值是否在数据已存在
    :param conn:
    :param cursor:
    :param _id:
    :return:
    """
    try:
        cursor.execute(
            """
                SELECT id,name
                FROM mz_common_articletype WHERE id=%s
            """, (_id,)
        )
        article_type = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=article_type)
