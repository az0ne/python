# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor

# 学习时间统计API


# @dec_timeit
# @dec_make_conn_cursor
# def query_datedetail(conn, cursor, _id, date):
#     """
#         returns: true/false
#     """
#     try:
#         cursor.execute(
#             """
#                 SELECT c.name AS coursename, l.name AS lessonname, b.total_minutes AS studytime
#
#                 FROM (mz_businessinfo_study_time AS b LEFT JOIN mz_course_course AS c ON b.course_id = c.id) LEFT JOIN mz_course_lesson AS l ON b.lesson_id = l.id
#
#                 WHERE b.`day` = %s AND b.user_id = %s
#             """, (date, _id))
#         studyinfo = cursor.fetchall()
#     except Exception as e:
#         log.warn(
#             "execute exception: %s. "
#             "statement: %s" % (e, cursor.statement))
#         raise e
#     return APIResult(result=studyinfo)
@dec_timeit
@dec_make_conn_cursor
def list_course_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT
                mz_course_course.id,
                name,
                seo_title,
                seo_keywords,
                seo_description
            FROM
                mz_course_course
            LEFT JOIN mz_common_objseo ON mz_course_course.id = mz_common_objseo.obj_id
            AND mz_common_objseo.obj_type='COURSE'
            ORDER BY id DESC
            limit %s,%s
            """, (start_index, page_size,))
        course = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_course_course
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    employ_dict = {
        "result": course,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)



















@dec_timeit
@dec_make_conn_cursor
def get_course_by_title(conn, cursor, index_joint, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT
                    mz_course_course.id,
                    name,
                    seo_title,
                    seo_keywords,
                    seo_description
                FROM
                    mz_course_course
                LEFT JOIN mz_common_objseo ON mz_course_course.id = mz_common_objseo.obj_id
                AND mz_common_objseo.obj_type='COURSE'
                WHERE
                name LIKE %s
                ORDER BY id DESC
                limit %s,%s
            """, (index_joint, start_index, page_size,))
        courseinfo = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(ttt.name) AS count from (
                SELECT
                    mz_course_course.id,
                    name,
                    seo_title,
                    seo_keywords,
                    seo_description
                FROM
                    mz_course_course
                LEFT JOIN mz_common_objseo ON mz_course_course.id = mz_common_objseo.obj_id
                AND mz_common_objseo.obj_type='COURSE'
                WHERE
                name LIKE %s
                ORDER BY id DESC
                ) AS ttt

            """,(index_joint,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    employ_dict = {
        "result": courseinfo,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)



#创建小课程SEO信息
@dec_timeit
@dec_make_conn_cursor
def cteat_course_conf(conn, cursor, _id, seotitle, seokeyword, seodescription,):
    """
    """
    try:
        cursor.execute(
            """
				INSERT INTO
				mz_common_objseo
				(seo_title, seo_keywords, seo_description, obj_type, obj_id)
				VALUES
				(%s, %s, %s, 'COURSE', %s)
            """, (seotitle,seokeyword,seodescription,_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)














#确认修改小课程SEO信息
@dec_timeit
@dec_make_conn_cursor
def edit_course_conf(conn, cursor, _id, seotitle, seokeyword, seodescription,):
    """
    """
    try:
        cursor.execute(
            """
        UPDATE mz_common_objseo
        SET
        seo_title =%s,
         seo_keywords =%s,
         seo_description =%s
        WHERE
            obj_id =%s
            """, (seotitle,seokeyword,seodescription,_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)








# 查看API
@dec_timeit
@dec_make_conn_cursor
def edit_course_by_id(conn, cursor, _id):
    """
    """

    try:
        cursor.execute(
            """
            SELECT
                mz_course_course.id,
                name,
                seo_title,
                seo_keywords,
                seo_description
            FROM
                mz_course_course,
                mz_common_objseo
            WHERE
                mz_course_course.id = mz_common_objseo.obj_id
            AND mz_course_course.id=%s
            AND mz_common_objseo.obj_type='COURSE'
            """, (_id,))
        employteacher = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=employteacher)



