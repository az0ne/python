# -*- coding:utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils import tool


@dec_timeit
@dec_make_conn_cursor
def insert_task_desc(conn, cursor, task_id, img1, img2, img3, title, created_time, update_time, operator_id):
    try:
        cursor.execute(
            """
                INSERT INTO mz_free_task_desc (task_id, title, img1, img2, img3, created_time, update_time, operator_id)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            """, (task_id, title, img1, img2, img3, created_time, update_time, operator_id)
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
def update_task_desc(conn, cursor, _id, task_id, img1, img2, img3, title, update_time):
    try:
        cursor.execute(
            """
                UPDATE mz_free_task_desc SET task_id=%s, title=%s, img1=%s, img2=%s, img3=%s, update_time=%s
                WHERE id=%s
            """, (task_id, title, img1, img2, img3, update_time, _id)
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
def delete_task_desc(conn, cursor, _id):
    try:
        cursor.execute(
            """
                DELETE FROM mz_free_task_desc WHERE id=%s
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
def delete_task_desc_by_task_id(conn, cursor, task_id):
    try:
        cursor.execute(
            """
                DELETE ta,tew,td FROM mz_free_task_desc AS td
                LEFT JOIN mz_free_task_article AS ta ON ta.task_id=td.task_id
                LEFT JOIN mz_free_task_excellent_works AS tew ON tew.task_id=td.task_id
                WHERE td.task_id=%s
            """, (task_id,)
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
def select_task_desc_by_id(conn, cursor, _id):
    try:
        cursor.execute(
            """
                SELECT id,task_id,title,img1,img2,img3,created_time,update_time,operator_id
                FROM mz_free_task_desc WHERE id=%s
            """, (_id,)
        )
        task_desc = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
    return APIResult(result=task_desc)


@dec_timeit
@dec_make_conn_cursor
def select_task_desc_by_task_id(conn, cursor, task_id):
    try:
        cursor.execute(
            """
                SELECT id,task_id,title,img1,img2,img3,created_time,update_time,operator_id
                FROM mz_free_task_desc WHERE task_id=%s
            """, (task_id,)
        )
        task_desc = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=task_desc)


@dec_timeit
@dec_make_conn_cursor
def select_task_desc_by_page(conn, cursor, page_index, page_size):
    """
    :return:
    """
    start_index = tool.get_page_info(page_index, page_size)

    try:
        cursor.execute(
            """
                SELECT id,title,task_id FROM mz_free_task_desc
                ORDER BY id DESC
                LIMIT %s,%s
            """, (start_index, page_size)
        )
        task_desc = cursor.fetchall()

        cursor.execute(
            """
                SELECT COUNT(*) AS count FROM mz_free_task_desc
            """
        )
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "cursor exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    task_desc_dict = {
        "result": task_desc,
        "page_count": page_count,
        "rows_count": rows_count["count"],
    }

    return APIResult(result=task_desc_dict)


@dec_timeit
@dec_make_conn_cursor
def search_task_desc_by_title(conn, cursor, title, page_index, page_size):
    """
    :return:
    """
    start_index = tool.get_page_info(page_index, page_size)

    try:
        cursor.execute(
            """
                SELECT id,title,task_id FROM mz_free_task_desc
                WHERE title LIKE %s
                ORDER BY id DESC
                LIMIT %s,%s
            """, (title, start_index, page_size)
        )
        task_desc = cursor.fetchall()

        cursor.execute(
            """
                SELECT COUNT(*) AS count FROM mz_free_task_desc WHERE title LIKE %s
            """, (title,)
        )
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "cursor exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    task_desc_dict = {
        "result": task_desc,
        "page_count": page_count,
        "rows_count": rows_count["count"],
    }

    return APIResult(result=task_desc_dict)
