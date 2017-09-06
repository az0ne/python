# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def get_homepagecourse_by_type(conn, cursor, keyword, type, page_index, page_size):
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT
                mz_course_course. NAME,
                mz_homepage_course.`INDEX`,
                mz_homepage_course.id,
                careercatagory_id.id AS careerid
            FROM
                mz_homepage_course
            LEFT JOIN mz_course_course ON mz_homepage_course.course_id = mz_course_course.id
            WHERE
                mz_course_course. NAME LIKE %s
            AND careercatagory_id = %s
            GROUP BY
                mz_homepage_course.id
            ORDER BY
                mz_homepage_course.id DESC
            limit %s,%s
            """, (keyword, type, start_index, page_size))
        homepagecourse = cursor.fetchall()

        cursor.execute(
            """
            SELECT count(*) as count
            FROM mz_homepage_course
            LEFT JOIN mz_course_course ON mz_homepage_course.course_id = mz_course_course.id
            WHERE mz_course_course. NAME LIKE %s AND  careercatagory_id = %s
            """, (keyword, type))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    employ_dict = {
        "result": homepagecourse,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=employ_dict)


@dec_timeit
@dec_make_conn_cursor
def get_homepagecourse_by_onlytype(conn, cursor, type, page_index, page_size):
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT
                mz_course_course. NAME,
                mz_homepage_course.`INDEX`,
                mz_homepage_course.id,
                careercatagory_id AS careerid
            FROM
                mz_homepage_course
            LEFT JOIN mz_course_course ON mz_homepage_course.course_id = mz_course_course.id
            WHERE
                 careercatagory_id = %s
            GROUP BY
                mz_homepage_course.id
            ORDER BY
                mz_homepage_course.id DESC
            limit %s,%s
            """, (type, start_index, page_size))
        homepagecourse = cursor.fetchall()

        cursor.execute(
            """
            SELECT count(*) as count
            FROM mz_homepage_course
            LEFT JOIN mz_course_course ON mz_homepage_course.course_id = mz_course_course.id
            WHERE careercatagory_id = %s
            """, (type,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    employ_dict = {
        "result": homepagecourse,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=employ_dict)































@dec_timeit
@dec_make_conn_cursor
def get_homepagecourse_by_keyword(conn, cursor, keyword, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT
                mz_course_course. NAME,
                mz_homepage_course.`INDEX`,
                mz_homepage_course.id,
                careercatagory_id AS careerid
            FROM
                mz_homepage_course
            LEFT JOIN mz_course_course ON mz_homepage_course.course_id = mz_course_course.id
            WHERE
                mz_course_course. NAME LIKE %s
            GROUP BY
                mz_homepage_course.id
            ORDER BY
                mz_homepage_course.id DESC
            limit %s,%s
            """, (keyword, start_index, page_size))
        homepagecourse = cursor.fetchall()

        cursor.execute(
            """
            SELECT count(*) as count
            FROM mz_homepage_course
            LEFT JOIN mz_course_course ON mz_homepage_course.course_id = mz_course_course.id
            WHERE mz_course_course. NAME LIKE %s
            """, (keyword,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    employ_dict = {
        "result": homepagecourse,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=employ_dict)





















@dec_timeit
@dec_make_conn_cursor
def get_homepagecourse_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT
                mz_course_course. NAME,
                mz_homepage_course.`INDEX`,
                mz_homepage_course.id,
                careercatagory_id AS careerid
            FROM
                mz_homepage_course
            LEFT JOIN mz_course_course ON mz_homepage_course.course_id = mz_course_course.id
            GROUP BY
                mz_homepage_course.id
            ORDER BY
                mz_homepage_course.id DESC
            limit %s,%s
            """, (start_index, page_size,))
        homepagecourse = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_homepage_course
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    employ_dict = {
        "result": homepagecourse,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)































@dec_timeit
@dec_make_conn_cursor
def get_homepagecourse_by_id(conn, cursor, _id):
    """
    """
    try:
        cursor.execute(
            """
            SELECT
                mz_course_course. NAME,
                mz_homepage_course.`INDEX`,
                mz_homepage_course.id,
                careercatagory_id AS careerid,
                mz_homepage_course.course_id
            FROM
                mz_homepage_course
            LEFT JOIN mz_course_course ON mz_homepage_course.course_id = mz_course_course.id
            WHERE mz_homepage_course.id = %s
            """, (_id,))
        homepagecourse = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=homepagecourse)
















@dec_timeit
@dec_make_conn_cursor
def infocon(conn, cursor, career_id, course_id):
    try:
        cursor.execute(
            """
                SELECT *
                FROM mz_common_objtagrelation
                WHERE obj_type='COURSE' AND careercatagory_id=%s AND obj_id=%s
            """,(career_id, course_id))

        course_ajax = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=course_ajax)







@dec_timeit
@dec_make_conn_cursor
def updatehomepagecourse(conn, cursor, _id, course_id):
    try:
        cursor.execute(
            """
                update mz_homepage_course set course_id=%s WHERE id=%s;
            """, (course_id, _id))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)






