# -*- coding:utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult


@dec_timeit
@dec_make_conn_cursor
def insert_task_article(conn, cursor, task_id, article_title, article_url, index, _type):
    try:
        cursor.execute(
            """
                INSERT INTO mz_free_task_article (task_id, article_title, article_url, mz_free_task_article.`index`, type)
                VALUES (%s,%s,%s,%s,%s)
            """, (task_id, article_title, article_url, index, _type)
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
def update_task_article(conn, cursor, _id, task_id, article_title, article_url, index, _type):
    try:
        cursor.execute(
            """
                UPDATE mz_free_task_article AS ta SET task_id=%s, article_title=%s, article_url=%s, ta.index=%s, type=%s
                WHERE id=%s
            """, (task_id, article_title, article_url, index, _type, _id)
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
def delete_task_article(conn, cursor, _id):
    try:
        cursor.execute(
            """
                DELETE FROM mz_free_task_article WHERE id=%s
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
def select_task_article_by_id(conn, cursor, _id):
    try:
        cursor.execute(
            """
                SELECT id,task_id,article_title,article_url,ta.index,ta.type FROM mz_free_task_article AS ta WHERE id=%s
            """, (_id,)
        )
        task_article = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
    return APIResult(result=task_article)


@dec_timeit
@dec_make_conn_cursor
def select_task_article_by_task_id(conn, cursor, task_id):
    try:
        cursor.execute(
            """
                SELECT id,task_id,article_title,article_url,ta.index,ta.type FROM mz_free_task_article as ta
                WHERE task_id=%s
                ORDER BY id
            """, (task_id,)
        )
        task_article = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=task_article)
