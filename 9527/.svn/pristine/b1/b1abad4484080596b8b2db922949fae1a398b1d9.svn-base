# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils import tool


@dec_timeit
@dec_make_conn_cursor
def insert_banner(conn, cursor, image_title, image_url, url, index, bgcolor,type):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                insert into
                    mz_common_banner (image_title,image_url,url,mz_common_banner.`index`,bgcolor,type)
                values (%s,%s,%s,%s,%s,%s);
            """, (image_title, image_url, url, index, bgcolor,type))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_banner(conn, cursor, _id, image_title, image_url, url, index, bgcolor,type):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                UPDATE mz_common_banner set image_title=%s,image_url=%s,url=%s,mz_common_banner.`index`=%s,bgcolor=%s,type=%s
                WHERE id = %s;
            """, (image_title, image_url, url, index, bgcolor, type, _id))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_banner(conn, cursor, _id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_common_banner WHERE id=%s;
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
def list_banner(conn, cursor):
    """
    """

    try:
        cursor.execute(
            """
                SELECT id
                        ,image_url
                        ,image_title
                        ,url
                        ,mz_common_banner.`index`
                        ,bgcolor
                        ,type
                FROM mz_common_banner
                ORDER BY id DESC
            """)
        banners = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=banners)


@dec_timeit
@dec_make_conn_cursor
def list_banner_by_page(conn, cursor, page_index, page_size):
    """

    """
    start_index = tool.get_page_info(page_index, page_size)

    try:
        cursor.execute(
            """
                SELECT id
                        ,image_url
                        ,image_title
                        ,url
                        ,mz_common_banner.`index`
                        ,bgcolor
                        ,type
                FROM mz_common_banner
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size,))
        banners = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_banner
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    banner_dict = {
        "result": banners,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=banner_dict)


@dec_timeit
@dec_make_conn_cursor
def get_banner_by_id(conn, cursor, _id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT id
                        ,image_url
                        ,image_title
                        ,url
                        ,mz_common_banner.`index`
                        ,bgcolor
                        ,type
                FROM mz_common_banner WHERE id = %s
            """, (_id,))
        banners = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=banners)


@dec_timeit
@dec_make_conn_cursor
def list_banner_by_image_title(conn, cursor, image_title, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)

    try:
        cursor.execute(
            """
                SELECT id
                        ,image_url
                        ,image_title
                        ,url
                        ,mz_common_banner.`index`
                        ,bgcolor
                        ,type
                FROM mz_common_banner
                WHERE image_title LIKE %s
                ORDER BY id DESC
                limit %s,%s
            """, (image_title, start_index, page_size))
        banners = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_banner WHERE image_title LIKE %s
            """, (image_title,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    banner_dict = {
        "result": banners,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=banner_dict)
