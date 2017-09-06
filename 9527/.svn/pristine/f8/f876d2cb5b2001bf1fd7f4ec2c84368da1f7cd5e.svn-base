# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils import tool


@dec_timeit
@dec_make_conn_cursor
def insert_career_page_student(conn, cursor, img_url, career_id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                insert into mz_career_page_student (img_url, career_id)
                values (%s,%s);
            """, (img_url, career_id))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_career_page_student(conn, cursor, _id, img_url, career_id):
    """

    :param conn:
    :param cursor:
    :param _id:
    :param img_url:
    :param career_id:
    :return: true/false
    """
    try:
        cursor.execute(
            """
                UPDATE mz_career_page_student set img_url=%s, career_id=%s
                WHERE id = %s;
            """, (img_url, career_id, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_career_page_student(conn, cursor, _id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_career_page_student WHERE id=%s;
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
def delete_career_page_student_by_career_id(conn, cursor, career_id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_career_page_student WHERE career_id=%s;
            """, (career_id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def list_career_page_student_by_page(conn, cursor, page_index, page_size):
    """

    """
    start_index = tool.get_page_info(page_index, page_size)

    try:
        cursor.execute(
            """
                SELECT cps.id,cps.img_url, cps.career_id, cp.name AS career_name
                FROM mz_career_page_student AS cps ,mz_career_page AS cp
                WHERE cp.id=cps.career_id
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size,))
        career_page_student = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_career_page_student
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    careerPageStudents_dict = {
        "result": career_page_student,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=careerPageStudents_dict)


@dec_timeit
@dec_make_conn_cursor
def get_career_page_student_by_id(conn, cursor, _id):
    """

    :param conn:
    :param cursor:
    :param _id:
    :return:
    """

    try:
        cursor.execute(
            """
                SELECT cps.id,cps.img_url, cps.career_id, cp.name AS career_name
                FROM mz_career_page_student AS cps ,mz_career_page AS cp
                WHERE cp.id=cps.career_id AND cps.id = %s
            """, (_id,))

        career_page_students = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=career_page_students)


@dec_timeit
@dec_make_conn_cursor
def list_career_page_student_by_career_id(conn, cursor, career_id):
    """
    """
    try:
        cursor.execute(
            """
                SELECT cps.id,cps.img_url,cps.career_id,cp.name AS career_name
                FROM mz_career_page_student AS cps ,mz_career_page AS cp
                WHERE cp.id=cps.career_id AND cps.career_id=%s
            """, (career_id,))

        career_page_students = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=career_page_students)


@dec_timeit
@dec_make_conn_cursor
def get_career_page_student_by_career_name(conn, cursor, career_name, page_index, page_size):
    """
    filter based on career_name,return type of list
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT cps.id,cps.img_url, cps.career_id, cp.name AS career_name
                FROM mz_career_page_student AS cps ,mz_career_page AS cp
                WHERE cp.id=cps.career_id AND cp.name LIKE %s
                ORDER BY id
                limit %s,%s
            """, (career_name, start_index, page_size))

        career_page_students = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) AS count
                FROM mz_career_page_student AS cps ,mz_career_page AS cp
                WHERE cp.id=cps.career_id AND cp.name LIKE %s
            """, (career_name,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    careerPageStudents_dict = {
        "result": career_page_students,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=careerPageStudents_dict)
