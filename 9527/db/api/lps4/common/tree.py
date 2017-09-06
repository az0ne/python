#! /usr/bin/evn python
# -*- coding:utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor

@dec_timeit
@dec_make_conn_cursor
def insert_lps4_tree(conn, cursor, data):
    try:
        cursor.execute(
            """
               INSERT INTO mz_lps4_tree (stage_id,career_id,stage_name,`index`)
               values (%s,%s,%s,%s)
            """, (data["stage_id"],data["career_id"],data["stage_name"],data["index"]))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_lps4_tree(conn, cursor, data):
    try:
        cursor.execute(
            """
               UPDATE mz_lps4_tree
               SET stage_id=%s,career_id=%s,stage_name=%s,`index`=%s
               WHERE id=%s
            """, (data["stage_id"],data["career_id"],data["stage_name"],data["index"],data["id"]))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_lps4_tree_by_id(conn, cursor, _id):
    try:
        cursor.execute(
            """
              DELETE FROM mz_lps4_tree
              WHERE id=%s
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
def get_lps4_tree_by_id(conn, cursor, _id):
    try:
        cursor.execute(
            """
              SELECT id,stage_id,career_id,stage_name,`index`
              FROM mz_lps4_tree
              WHERE id=%s
            """, (_id,))
        tree = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=tree)


@dec_timeit
@dec_make_conn_cursor
def list_lps4_tree(conn, cursor):
    try:
        cursor.execute(
            """
              SELECT tree.id,stage_id,career_id,stage_name,`index`,career.name as career_name
              FROM mz_lps4_tree as tree
              INNER JOIN mz_lps4_career as career
              ON tree.career_id=career.id
            """)
        trees = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=trees)


@dec_timeit
@dec_make_conn_cursor
def list_lps4_tree_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT  tree.id,tree.stage_id,tree.career_id,tree.stage_name,tree.`index`,career.name as career_name,
                        stage.name as stage
                FROM mz_lps4_tree as tree
                LEFT JOIN mz_lps4_career as career
                ON tree.career_id=career.id
                LEFT JOIN mz_course_stage as stage
                ON stage.id=tree.stage_id
                ORDER BY tree.career_id, tree.`index`
                limit %s,%s
            """, (start_index, page_size,))
        trees = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_lps4_tree
            """)
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    lps4_tree_dict = {
        "result": trees,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=lps4_tree_dict)


@dec_timeit
@dec_make_conn_cursor
def list_lps4_tree_by_search(conn, cursor, page_index, page_size, career_id):
    """
    """
    start_index = get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT  tree.id,tree.stage_id,tree.career_id,tree.stage_name,tree.`index`,career.name as career_name,
                stage.name as stage
                FROM mz_lps4_tree as tree
                LEFT JOIN mz_lps4_career as career
                ON tree.career_id=career.id
                LEFT JOIN mz_course_stage as stage
                ON stage.id=tree.stage_id
                WHERE tree.career_id=%s
                ORDER BY tree.career_id,tree.`index`
                limit %s,%s
            """, (career_id, start_index, page_size,))
        trees = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_lps4_tree
                WHERE career_id=%s
            """, (career_id,))
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    lps4_tree_dict = {
        "result": trees,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=lps4_tree_dict)