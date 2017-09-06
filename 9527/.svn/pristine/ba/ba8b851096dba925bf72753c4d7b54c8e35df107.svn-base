# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils import tool


@dec_timeit
@dec_make_conn_cursor
def insert_career_page_teacher(conn, cursor, _id, teacher_id, name, title, info, big_img_url, career_id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                insert into mz_career_page_teacher (id, name, teacher_id, title, info, big_img_url, career_id)
                values (%s,%s,%s,%s,%s,%s,%s);
            """, (_id, name, teacher_id, title, info, big_img_url, career_id))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_career_page_teacher(conn, cursor, _id, teacher_id, name, title, info, big_img_url, career_id):
    """
    return: true/false
    """
    try:
        cursor.execute(
            """
                UPDATE mz_career_page_teacher set teacher_id=%s, name=%s, title=%s, info=%s, big_img_url=%s, career_id=%s
                WHERE id = %s;
            """, (teacher_id, name, title, info, big_img_url, career_id, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_career_page_teacher(conn, cursor, _id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_career_page_teacher WHERE id=%s;
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
def delete_career_page_teacher_by_career_id(conn, cursor, career_id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_career_page_teacher WHERE career_id=%s;
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
def list_career_page_teacher_by_page(conn, cursor, page_index, page_size):
    """

    """
    start_index = tool.get_page_info(page_index, page_size)

    try:
        cursor.execute(
            """
                SELECT id, teacher_id, name, title, info, big_img_url, career_id, cp.name AS career_name
                FROM mz_career_page_teacher AS cpt, me_career_page AS cp
                WHERE cpt.career_id=cp.id
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size,))
        careerPageTeachers = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_career_page_teacher
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    careerPageTeacher_dict = {
        "result": careerPageTeachers,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=careerPageTeacher_dict)


@dec_timeit
@dec_make_conn_cursor
def list_career_page_teacher_by_career_id(conn, cursor, career_id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT cpt.id, cpt.teacher_id, cpt.name, cpt.title, cpt.info, cpt.big_img_url, cpt.career_id,cp.name AS career_name
                FROM mz_career_page_teacher AS cpt, mz_career_page AS cp
                WHERE cpt.career_id=cp.id AND cpt.career_id=%s
            """, (career_id,))

        careerPageTeachers = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerPageTeachers)


@dec_timeit
@dec_make_conn_cursor
def list_career_page_teacher_by_career_name(conn, cursor, career_name, page_index, page_size):
    """
    filter based on career_name,return type of list
    """

    try:
        cursor.execute(
            """
                SELECT cpt.id, cpt.teacher_id, cpt.name, cpt.title, cpt.info, cpt.big_img_url, cpt.career_id, cp.name AS career_name
                FROM mz_career_page_teacher AS cpt, mz_career_page AS cp
                WHERE cpt.career_id=cp.id AND cp.name LIKE %s
                ORDER BY id
                limit %s,%s
            """, (career_name, page_index, page_size))

        careerPageTeachers = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) AS count
                FROM mz_career_page_teacher AS cpt, mz_career_page AS cp
                WHERE cpt.career_id=cp.id AND cp.name LIKE %s
            """, (career_name,))

        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    careerPageTeacher_dict = {
        "result": careerPageTeachers,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=careerPageTeacher_dict)


@dec_timeit
@dec_make_conn_cursor
def get_career_page_teacher_by_id(conn, cursor, _id):
    """
    filter based on id,return a data
    """

    try:
        cursor.execute(
            """
                SELECT cpt.id, cpt.teacher_id, cpt.name, cpt.title, cpt.info, cpt.big_img_url, cpt.career_id, cp.name AS career_name
                FROM mz_career_page_teacher AS cpt, mz_career_page AS cp
                WHERE cpt.career_id=cp.id AND cpt.id = %s
            """, (_id,))

        careerPageTeachers = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerPageTeachers)


