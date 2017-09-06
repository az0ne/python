# -*- coding: utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def insert_android_version(conn, cursor, vno, size, desc, is_force, down_url, _type):
    """
    插入一条数据，用于添加页面
    :return: true/false
    """
    try:
        cursor.execute(
            """
                insert into mz_common_androidversion
                (vno,`size`,`desc`,is_force,down_url, `type`)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (vno, size, desc, is_force, down_url, _type)
        )
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_android_version_by_id(conn, cursor, _id):
    """
    删除某一条数据，根据id值
    :param conn:
    :param cursor:
    :param _id:
    :return: true/false
    """
    try:
        cursor.execute(
            """
                delete from mz_common_androidversion
                WHERE id=%s
            """, (_id,)
        )
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_android_version(conn, cursor, _id, vno, size, desc, is_force, down_url, _type):
    """
    更新某一条数据，用户修改后保存
    :return: true/false
    """
    try:
        cursor.execute(
            """
                update mz_common_androidversion AS av
                set av.vno=%s,av.size=%s,av.desc=%s,av.is_force=%s,av.down_url=%s,av.type=%s
                WHERE av.id=%s
            """, (vno, size, desc, is_force, down_url, _type, _id)
        )
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def select_android_version_by_page(conn, cursor, page_index, page_size):
    """
    分页查询，根据id字倒序排列，用于list页面显示数据
    :param conn: @dec_make_conn_cursor装饰器参数
    :param cursor: @dec_make_conn_cursor装饰器参数
    :param page_index: 当前页码
    :param page_size: 每页条数
    :return: 返回androidversion表所有字段
    """
    # 获取当前页起始数字
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                select av.id,av.vno,av.size,av.desc,av.is_force, av.type,
                CASE  av.type
                WHEN '1' THEN '学生端'
                WHEN '2' THEN '教师端'
                END as type_name,
                av.down_url
                from mz_common_androidversion as av
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size)
        )
        android_version = cursor.fetchall()

        cursor.execute(
            """
                select count(*) as count from mz_common_androidversion
            """
        )
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:

        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    android_version_dict = {
        "result": android_version,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=android_version_dict)


@dec_timeit
@dec_make_conn_cursor
def search_android_version_by_vno_and_page(conn, cursor, vno, page_index, page_size):
    """
    根据vno字段检索查询并分页，根据id字倒序排列，用于list页面显示数据
    :param conn: @dec_make_conn_cursor装饰器参数
    :param cursor: @dec_make_conn_cursor装饰器参数
    :param page_index: 当前页码
    :param page_size: 每页条数
    :return: 返回androidversion表所有字段
    """
    # 获取当前页起始数字
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                select av.id,av.vno,av.size,av.desc,av.is_force, av.type,
                CASE  av.type
                WHEN '1' THEN '学生端'
                WHEN '2' THEN '教师端'
                END as type_name,
                av.down_url
                from mz_common_androidversion as av
                WHERE av.vno LIKE %s
                ORDER BY id DESC
                limit %s,%s
            """, (vno, start_index, page_size)
        )
        android_version = cursor.fetchall()

        cursor.execute(
            """
                select count(*) as count from mz_common_androidversion as av
                WHERE av.vno LIKE %s
            """, (vno,)
        )
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:

        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    android_version_dict = {
        "result": android_version,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=android_version_dict)


@dec_timeit
@dec_make_conn_cursor
def get_android_version_by_id(conn, cursor, _id):
    """
    获取android版本信息，根据id.用于修改/查看某一条数据
    :param conn:
    :param cursor:
    :param _id: androidversion表的id字段
    :return: 返回所有字段
    """
    try:
        cursor.execute(
            """
                select av.id,av.vno,av.size,av.desc,av.is_force,av.down_url,av.type
                from mz_common_androidversion as av
                WHERE id = %s
            """, (_id,)
        )
        android_version = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=android_version)
