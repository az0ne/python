# -*- coding: utf-8 -*-
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult



@dec_timeit
@dec_make_conn_cursor
def list_career_course_name(conn, cursor):
    """
    get career_course of name field
    """
    try:
        cursor.execute(
            """
                SELECT id,name
                FROM mz_course_careercourse
            """)
        careerCourses = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerCourses)


@dec_timeit
@dec_make_conn_cursor
def get_career_course_by_id(conn, cursor, _id):
    """
    get career_course by id
    """
    try:
        cursor.execute(
            """
                SELECT id,name
                FROM mz_course_careercourse
                WHERR id=%s;
            """)
        careerCourse = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerCourse)