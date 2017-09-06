# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor

# 学习时间统计API


@dec_timeit
@dec_make_conn_cursor
def query_datedetail(conn, cursor, _id, date):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                SELECT c.name AS coursename, l.name AS lessonname, b.total_minutes AS studytime

                FROM (mz_businessinfo_study_time AS b LEFT JOIN mz_course_course AS c ON b.course_id = c.id) LEFT JOIN mz_course_lesson AS l ON b.lesson_id = l.id

                WHERE b.`day` = %s AND b.user_id = %s
            """, (date, _id))
        studyinfo = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=studyinfo)



@dec_timeit
@dec_make_conn_cursor
def query_emaildetail(conn, cursor, index, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT
                    sum(total_minutes) AS studytime,
                    `day` AS datetime,
                    nick_name AS name,
                    mz_user_userprofile.id AS id
                FROM
                    mz_businessinfo_study_time LEFT JOIN mz_user_userprofile ON mz_businessinfo_study_time.user_id = mz_user_userprofile.id
                WHERE
                    user_id = (
                        SELECT
                            id
                        FROM
                            mz_user_userprofile
                        WHERE
                            mz_user_userprofile.email = %s
                        OR mz_user_userprofile.username = %s
                        OR mz_user_userprofile.mobile = %s
                    )
                GROUP BY
                    `day`
                limit %s,%s
            """, (index, index, index, start_index, page_size,))
        studyinfo = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(ttt.datetime) AS count from (
                SELECT
                    sum(total_minutes) AS studytime,
                    `day` AS datetime,
                    nick_name AS name,
                    mz_user_userprofile.id AS id
                FROM
                    mz_businessinfo_study_time LEFT JOIN mz_user_userprofile ON mz_businessinfo_study_time.user_id = mz_user_userprofile.id
                WHERE
                    user_id = (
                        SELECT
                            id
                        FROM
                            mz_user_userprofile
                        WHERE
                            mz_user_userprofile.email = %s
                        OR mz_user_userprofile.username = %s
                        OR mz_user_userprofile.mobile = %s
                    )
                GROUP BY
                    `day`
                ) AS ttt
            """,(index, index, index))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    employ_dict = {
        "result": studyinfo,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)




























# 删除api
@dec_timeit
@dec_make_conn_cursor
def delete_employteacher_by_id(conn, cursor,_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
               DELETE FROM mz_employ_teacher WHERE id=%s;
            """, (_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)



# 搜索api
@dec_timeit
@dec_make_conn_cursor
def list_employteacher_by_resume(conn, cursor, resume, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT id,teacher_type,teacher_catagory,name,career,work_time,resume,mobile,create_time,qq
            FROM mz_employ_teacher
            WHERE resume like %s
            ORDER BY id DESC
            limit %s,%s
            """, (resume, start_index, page_size,))
        employteacher = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_employ_teacher WHERE resume LIKE %s
            """, (resume,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    employ_dict = {
        "result": employteacher,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)



# 列表API
@dec_timeit
@dec_make_conn_cursor
def list_employteacher_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT id,teacher_type,teacher_catagory,name,career,work_time,resume,mobile,create_time,qq
                FROM mz_employ_teacher
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size,))
        employteacher = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_employ_teacher

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
        "result": employteacher,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=employ_dict)



# 查看API
@dec_timeit
@dec_make_conn_cursor
def get_employteacher_by_id(conn, cursor, _id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT id,teacher_type,teacher_catagory,name,career,work_time,resume,mobile,create_time,qq
                FROM mz_employ_teacher WHERE id = %s
            """, (_id,))
        employteacher = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=employteacher)



