# -*- coding: utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def insert_micro_crouse(conn, cursor, course_dict):
    """
        returns: true/false
    """
    try:
        cursor.execute(
                """
                    insert into mz_micro_course (title,info,start_date,end_date,status,vod_url,teacher_id,back_img,playback_img,career_id_1,career_id_2,career_id_3,student_count,min_student_count,max_student_count)
                    values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
                """, (course_dict['title'], course_dict['info'], course_dict['start_date'], course_dict['end_date'], course_dict['status'],course_dict['vod_url'], course_dict['teacher_id'],course_dict['back_img'],
                      course_dict['playback_img'],course_dict['career_id_1'],course_dict['career_id_2'],course_dict['career_id_3'],course_dict['student_count'],course_dict['min_student_count'],course_dict['max_student_count']))
        conn.commit()
    except Exception as e:
        print e
        log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def list_micro_course_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT id, title,info,start_date,end_date,status,teacher_id,student_count,webcast_teacher_url,webcast_student_url,webcast_id
                FROM mz_micro_course
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size,))
        micro_courses = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_micro_course
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    micro_courses_dict = {
        "result": micro_courses,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=micro_courses_dict)


@dec_timeit
@dec_make_conn_cursor
def get_micro_by_id(conn, cursor, _id):
    """

    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
         cursor.execute(
            """
            SELECT id,title,info,start_date,end_date,status,vod_url,student_count,back_img,playback_img,teacher_id,webcast_id,min_student_count,max_student_count,career_id_1,
            career_id_2,career_id_3
            FROM mz_micro_course
            WHERE id=%s;
            """,(_id,))
         course = cursor.fetchall()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=course)

@dec_timeit
@dec_make_conn_cursor
def update_status_by_id(conn, cursor,status, _id):
    """

    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
         cursor.execute(
            """
            UPDATE mz_micro_course set status=%s
            WHERE id=%s;
            """,(status,_id,))
         conn.commit()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_micro_by_keyword(conn, cursor, page_index, page_size,keyword):
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT id, title,info,start_date,end_date,status,teacher_id,student_count
                FROM mz_micro_course
                WHERE title LIKE %s or info LIKE %s
                limit %s,%s
            """, (keyword,keyword,start_index, page_size,))
        courses = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_micro_course
                WHERE title LIKE %s or info LIKE %s
            """,(keyword,keyword,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    course_dict = {
        "result": courses,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=course_dict)


@dec_timeit
@dec_make_conn_cursor
def update_student_count_by_id(conn, cursor, student_count, min_student_count, max_student_count, _id):
    """
    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
         cursor.execute(
            """
            UPDATE mz_micro_course set student_count=%s,min_student_count=%s,max_student_count=%s
            WHERE id=%s;
            """,(student_count, min_student_count, max_student_count, _id,))
         conn.commit()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_vod_by_id(conn, cursor, vod_id, vod_url, _id):
    """

    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
         cursor.execute(
            """
            UPDATE mz_micro_course set vod_id=%s,vod_url=%s
            WHERE id=%s;
            """,(vod_id,vod_url,_id,))
         conn.commit()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_vod_url_by_id(conn, cursor,  vod_url, _id):
    """

    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
         cursor.execute(
            """
            UPDATE mz_micro_course set vod_url=%s
            WHERE id=%s;
            """,(vod_url,_id,))
         conn.commit()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=True)

@dec_timeit
@dec_make_conn_cursor
def update_course_date_by_id(conn, cursor,  start_date, end_date, _id):
    """
    更新课程开始时间和结束时间
    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
         cursor.execute(
            """
            UPDATE mz_micro_course set start_date=%s,end_date=%s
            WHERE id=%s;
            """,(start_date, end_date,_id,))
         conn.commit()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def is_selected_course_time(conn, cursor, _id):
    """
    判断是否已经选择课程的开始时间和结束时间
    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
         cursor.execute(
            """
            SELECT id,start_date,end_date
            FROM mz_micro_course
            WHERE id=%s;
            """,(_id,))
         course = cursor.fetchall()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=course)