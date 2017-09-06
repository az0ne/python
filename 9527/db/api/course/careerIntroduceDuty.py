# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils import tool


@dec_timeit
@dec_make_conn_cursor
def insert_career_page_duty(conn, cursor, name, enterprise, career_id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                insert into mz_career_page_duty (name, enterprise, career_id)
                values (%s,%s,%s);
            """, (name, enterprise, career_id))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_career_page_duty(conn, cursor, _id, name, enterprise, career_id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                UPDATE mz_career_page_duty set name=%s, enterprise=%s, career_id=%s WHERE id = %s;
            """, (name, enterprise, career_id, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_career_page_duty(conn, cursor, _id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_career_page_duty WHERE id=%s;
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
def delete_career_page_duty_by_career_id(conn, cursor, career_id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_career_page_duty WHERE career_id=%s;
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
def list_career_page_duty_by_page(conn, cursor, page_index, page_size):
    """

    """
    start_index = tool.get_page_info(page_index, page_size)

    try:
        cursor.execute(
            """
                SELECT cpd.id, cpd.name, cpd.enterprise, cpd.career_id, cp.name AS career_name
                FROM mz_career_page_duty AS cpd, me_career_page AS cp
                WHERE cpd.career_id=cp.id
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size,))
        careerPageDuties = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_career_page_duty
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    careerPageDuty_dict = {
        "result": careerPageDuties,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=careerPageDuty_dict)


@dec_timeit
@dec_make_conn_cursor
def list_career_page_duty_by_career_name(conn, cursor, career_name, page_index, page_size):
    """
    filter based on career_name,return type of list
    """

    try:
        cursor.execute(
            """
                SELECT cpd.id, cpd.name, cpd.enterprise, cpd.career_id, cp.name AS career_name
                FROM mz_career_page_duty AS cpd, me_career_page AS cp
                WHERE cpd.career_id=cp.id AND cp.name LIKE %s
                ORDER BY id
                limit %s,%s
            """, (career_name, page_index, page_size))

        careerPageDuties = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) AS count
                FROM mz_career_page_duty AS cpd, me_career_page AS cp
                WHERE cpd.career_id=cp.id AND cp.name LIKE %s
            """, (career_name,))

        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    careerPageDuty_dict = {
        "result": careerPageDuties,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=careerPageDuty_dict)


@dec_timeit
@dec_make_conn_cursor
def list_career_page_duty_by_career_id(conn, cursor, career_id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT cpd.id, cpd.name, cpd.enterprise, cpd.career_id,cp.name AS career_name
                FROM mz_career_page_duty AS cpd, mz_career_page AS cp
                WHERE cpd.career_id=cp.id AND cpd.career_id=%s
            """, (career_id,))

        careerPageDuties = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerPageDuties)


@dec_timeit
@dec_make_conn_cursor
def get_career_page_duty_by_id(conn, cursor, _id):
    """
    filter based on id,return a data
    """

    try:
        cursor.execute(
            """
                SELECT cpd.id, cpd.name, cpd.enterprise, cpd.career_id, cp.name AS career_name
                FROM mz_career_page_duty AS cpd, mz_career_page AS cp
                WHERE cpd.career_id=cp.id AND cpd.id = %s
            """, (_id,))

        careerPageDuties = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerPageDuties)


