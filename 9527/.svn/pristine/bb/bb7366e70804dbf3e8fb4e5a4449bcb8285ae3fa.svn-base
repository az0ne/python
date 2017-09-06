# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils import tool


@dec_timeit
@dec_make_conn_cursor
def insert_career_page_enterprise(conn, cursor, img_url, img_title, career_id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                insert into mz_career_page_enterprise (img_url, img_title, career_id)
                values (%s,%s,%s);
            """, (img_url, img_title, career_id))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_career_page_enterprise(conn, cursor, _id, img_url, img_title, career_id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                UPDATE mz_career_page_enterprise set img_url=%s, img_title=%s, career_id=%s WHERE id = %s;
            """, (img_url, img_title, career_id, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_career_page_enterprise(conn, cursor, _id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_career_page_enterprise WHERE id=%s;
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
def delete_career_page_enterprise_by_career_id(conn, cursor, career_id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_career_page_enterprise WHERE career_id=%s;
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
def list_career_page_enterprise_by_page(conn, cursor, page_index, page_size):
    """

    """
    start_index = tool.get_page_info(page_index, page_size)

    try:
        cursor.execute(
            """
                SELECT cpe.id,cpe.img_url, cpe.img_title, cpe.career_id, cp.name AS career_name
                FROM mz_career_page_enterprise AS cpe, mz_career_page AS cp
                WHERE cpe.career_id=cp.id
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size,))
        careerPageEnterprises = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_career_page_enterprise
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    careerPageEnterprise_dict = {
        "result": careerPageEnterprises,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=careerPageEnterprise_dict)


@dec_timeit
@dec_make_conn_cursor
def list_career_page_enterprise_by_career_id(conn, cursor, career_id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT cpe.id,cpe.img_url, cpe.img_title, cpe.career_id,cp.name AS career_name
                FROM mz_career_page_enterprise AS cpe, mz_career_page AS cp
                WHERE cpe.career_id=cp.id AND cpe.career_id=%s
            """, (career_id,))

        careerPageEnterprises = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerPageEnterprises)


@dec_timeit
@dec_make_conn_cursor
def list_career_page_enterprise_by_career_name(conn, cursor, career_name, page_index, page_size):
    """
    filter based on career_name,return type of list
    """

    try:
        cursor.execute(
            """
                SELECT cpe.id,cpe.img_url, cpe.img_title, cpe.career_id, cp.name AS career_name
                FROM mz_career_page_enterprise AS cpe, mz_career_page AS cp
                WHERE cpe.career_id=cp.id AND cp.name LIKE %s
                ORDER BY id
                limit %s,%s
            """, (career_name, page_index, page_size))

        careerPageEnterprises = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) AS count
                FROM mz_career_page_enterprise AS cpt, mz_career_page AS cp
                WHERE cpt.career_id=cp.id AND cp.name LIKE %s
            """, (career_name,))

        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    careerPageEnterprise_dict = {
        "result": careerPageEnterprises,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=careerPageEnterprise_dict)


@dec_timeit
@dec_make_conn_cursor
def get_career_page_enterprise_by_id(conn, cursor, _id):
    """
    filter based on id,return a data
    """

    try:
        cursor.execute(
            """
                SELECT cpe.id,cpe.img_url, cpe.img_title, cpe.career_id, cp.name AS career_name
                FROM mz_career_page_enterprise AS cpe, mz_career_page AS cp
                WHERE cpe.career_id=cp.id AND cpe.id = %s
            """, (_id,))

        careerPageEnterprises = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerPageEnterprises)


