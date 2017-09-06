# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils import tool


@dec_timeit
@dec_make_conn_cursor
def insert_career_catagory(conn, cursor, name):
    """
        新增数据
        returns: true/false
    """

    try:
        cursor.execute(
            """
                insert into mz_course_careercatagory (name) values (%s);
            """, (name,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_career_catagory(conn, cursor, _id, name):
    """
        修改数据，根据id值
        returns: true/false
    """

    try:
        cursor.execute(
            """
                UPDATE mz_course_careercatagory set name=%s WHERE id = %s;
            """, (name, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_career_catagory(conn, cursor, _id):
    """
        删除数据，根据id
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_course_careercatagory WHERE id=%s;
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
def list_career_catagory(conn, cursor):
    """
    获取所有的职业方向的名称和id值，用于填充下拉列表框
    :param conn:
    :param cursor:
    :return: 返回职业方向name和id
    """

    try:
        cursor.execute(
            """
                SELECT id
                        ,name
                FROM mz_course_careercatagory
                ORDER BY id
            """)
        careerCatagories = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerCatagories)


@dec_timeit
@dec_make_conn_cursor
def list_career_catagory_by_page(conn, cursor, page_index, page_size):
    """
    分页查询
    """
    start_index = tool.get_page_info(page_index, page_size)

    try:
        cursor.execute(
            """
                SELECT id
                        ,name
                FROM mz_course_careercatagory
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size,))
        careerCatagories = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_course_careercatagory
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    careerCatagory_dict = {
        "result": careerCatagories,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=careerCatagory_dict)


@dec_timeit
@dec_make_conn_cursor
def get_career_catagory_by_id(conn, cursor, _id):
    """
    根据专业方向id查询一条数据
    :param conn:
    :param cursor:
    :param _id: 专业方向id
    :return: 返回专业方向id,name
    """

    try:
        cursor.execute(
            """
                SELECT id
                        ,name
                FROM mz_course_careercatagory WHERE id = %s
            """, (_id,))
        careerCatagories = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerCatagories)


@dec_timeit
@dec_make_conn_cursor
def get_career_catagory_by_name(conn, cursor, name, page_index, page_size):
    """
    根据专业方向名称过滤
    :param conn:
    :param cursor:
    :param name: 专业方向名称
    :param page_index: 当前页码
    :param page_size: 每页多少条数据
    :return: 返回careerCatagory_dict
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT id
                        ,name
                FROM mz_course_careercatagory WHERE name LIKE %s limit %s,%s
            """, (name, start_index, page_size))
        careerCatagories = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_course_careercatagory WHERE name LIKE %s
            """, (name,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    careerCatagory_dict = {
        "result": careerCatagories,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=careerCatagory_dict)
