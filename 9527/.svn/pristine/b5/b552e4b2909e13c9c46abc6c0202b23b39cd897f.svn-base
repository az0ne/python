# -*- coding:utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult


@dec_timeit
@dec_make_conn_cursor
def insert_task_excellent_works(conn, cursor, task_id, title, img_url, code_url, index):
    try:
        cursor.execute(
            """
                INSERT INTO mz_free_task_excellent_works (task_id, title, img_url, code_url, mz_free_task_excellent_works.index)
                VALUES(%s,%s,%s,%s,%s)
            """, (task_id, title, img_url, code_url, index)
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
def update_task_excellent_works(conn, cursor, _id, task_id, title, img_url, code_url, index):
    try:
        cursor.execute(
            """
                UPDATE mz_free_task_excellent_works AS tew SET task_id=%s, title=%s, img_url=%s, code_url=%s, tew.index=%s
                WHERE id=%s
            """, (task_id, title, img_url, code_url, index, _id)
        )

        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_task_excellent_works(conn, cursor, _id):
    try:
        cursor.execute(
            """
                DELETE FROM mz_free_task_excellent_works WHERE id=%s
            """, (_id,)
        )
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def select_task_excellent_works_by_id(conn, cursor, _id):
    try:
        cursor.execute(
            """
                SELECT id,task_id,title,img_url,code_url,tew.index
                FROM  mz_free_task_excellent_works AS tew WHERE id=%s
            """, (_id,)
        )
        task_excellent_works = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement: %s" % (e, cursor.statment)
        )
        raise e

    return APIResult(result=task_excellent_works)


@dec_timeit
@dec_make_conn_cursor
def select_task_excellent_works_by_task_id(conn, cursor, task_id):
    try:
        cursor.execute(
            """
                SELECT id,task_id,title,img_url,code_url,mz_free_task_excellent_works.index
                FROM mz_free_task_excellent_works WHERE task_id=%s
            """, (task_id,)
        )
        task_excellent_works = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=task_excellent_works)
