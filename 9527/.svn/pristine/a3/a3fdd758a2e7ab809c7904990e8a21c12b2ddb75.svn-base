#! /usr/bin/evn python
# -*- coding:utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def insert_lps4_task(conn, cursor, dict):
    try:
        cursor.execute(
            """
                insert into mz_lps4_task (`name`, career_id, stage_id, `index`, pre_task, next_task, version)
                values (%s,%s,%s,%s,%s,%s,%s);
            """, (dict["name"], dict["career_id"], dict["stage_id"], dict["index"], dict["pre_task"], dict["next_task"],
                  dict["version"],))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_lps4_task(conn, cursor, dict):
    try:
        cursor.execute(
            """
                update mz_lps4_task
                SET `name`=%s, career_id=%s, stage_id=%s, `index`=%s, pre_task=%s, next_task=%s, version=%s, is_project=%s
                WHERE id=%s
            """, (dict["name"], dict["career_id"], dict["stage_id"], dict["index"], dict["pre_task"], dict["next_task"],
                  dict["version"], dict["is_project"], dict["id"],))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)

@dec_timeit
@dec_make_conn_cursor
def select_lps4_task(conn, cursor, page_index, page_size, keyword=None):
    start_index = get_page_info(page_index, page_size)
    try:
        if keyword:
            cursor.execute(
                """
                    SELECT task.id, task.`name`, task.career_id, task.stage_id, task.`index`,
                            task.pre_task, task.next_task, task.version,task.is_project,
                            career.name as career_name, stage.name as stage_name
                    FROM mz_lps4_task as task
                    LEFT JOIN mz_lps4_career as career
                    ON task.career_id=career.id
                    LEFT JOIN mz_lps4_stage as stage
                    ON task.stage_id=stage.id
                    WHERE career.name LIKE %s
                    ORDER BY `index`
                    limit %s,%s

                """,(keyword, start_index, page_size,))
        else:
            cursor.execute(
                """
                    SELECT task.id, task.`name`, task.career_id, task.stage_id, task.`index`,
                            task.pre_task, task.next_task, task.version,task.is_project,
                            career.name as career_name, stage.name as stage_name
                    FROM mz_lps4_task as task
                    LEFT JOIN mz_lps4_career as career
                    ON task.career_id=career.id
                    LEFT JOIN mz_lps4_stage as stage
                    ON task.stage_id=stage.id
                    ORDER BY `index`
                    limit %s,%s

                """, (start_index, page_size,))
        tasks = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_lps4_task
            """)
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    task_dict = {
        "result": tasks,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=task_dict)


@dec_timeit
@dec_make_conn_cursor
def get_task_by_id(conn, cursor, _id):
    try:
        cursor.execute(
            """
               SELECT id, `name`, career_id, stage_id,`index`,
                       pre_task, next_task, version,is_project
               FROM mz_lps4_task
               WHERE id=%s
            """, (_id,))
        task = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=task)


@dec_timeit
@dec_make_conn_cursor
def delect_task_by_id(conn, cursor, _id):
    try:
        cursor.execute(
            """
              DELETE FROM mz_lps4_task WHERE id=%s
            """, (_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)