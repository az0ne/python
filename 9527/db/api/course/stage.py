#! /usr/bin/evn python
# -*- coding:utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor

@dec_timeit
@dec_make_conn_cursor
def get_stage_by_career_id(conn, cursor, career_id):
    try:
        cursor.execute(
            """
               SELECT id, `name`
               FROM mz_course_stage
               WHERE career_course_id=%s AND lps_version=3.0
               ORDER BY `index`
            """, (career_id,))
        task = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=task)