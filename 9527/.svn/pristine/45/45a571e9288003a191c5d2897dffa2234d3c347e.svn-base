# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils import tool


@dec_timeit
@dec_make_conn_cursor
def insert_new_ad(conn, cursor, ad_type, img_title, img_url, url, is_actived):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                insert into mz_common_newad (mz_common_newad.type, img_title, img_url, url, is_actived) values (%s,%s,%s,%s,%s );
            """, (ad_type, img_title, img_url, url, is_actived))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_new_ad(conn, cursor, _id, ad_type, img_title, img_url, url, is_actived):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                UPDATE mz_common_newad SET mz_common_newad.type=%s,img_title=%s,img_url=%s,url=%s,is_actived=%s WHERE id = %s;
            """, (ad_type, img_title, img_url, url, is_actived, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_new_ad_is_actived(conn, cursor):
    """
    update table is_actived=1,Because there are only 1 active states in the mz_common_usercenterad
    :param conn:
    :param cursor:
    :return:
    """

    try:
        cursor.execute(
            """
            UPDATE mz_common_newad SET is_actived=REPLACE(is_actived,1,0)
            """
        )
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_new_ad(conn, cursor, _id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_common_newad  WHERE id=%s;
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
def list_new_ad(conn, cursor):
    """
    """

    try:
        cursor.execute(
            """
                SELECT id
                        ,type
                        ,img_title
                        ,img_url
                        ,url
                        ,is_actived
                FROM mz_common_newad
                ORDER BY id
            """)
        newAds = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=newAds)


@dec_timeit
@dec_make_conn_cursor
def list_new_ad_by_page(conn, cursor, page_index, page_size):
    """

    """
    start_index = tool.get_page_info(page_index, page_size)

    try:
        cursor.execute(
            """
                SELECT id
                        ,type
                        ,img_title
                        ,img_url
                        ,url
                        ,is_actived
                FROM mz_common_newad
                ORDER BY id DESC
                limit %s,%s
            """, (start_index, page_size,))
        newAds = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_newad
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    newAd_dict = {
        "result": newAds,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=newAd_dict)


@dec_timeit
@dec_make_conn_cursor
def get_new_ad_by_id(conn, cursor, _id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT id
                        ,type
                        ,img_title
                        ,img_url
                        ,url
                        ,is_actived
                FROM mz_common_newad WHERE id = %s
            """, (_id,))
        newAds = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=newAds)


@dec_timeit
@dec_make_conn_cursor
def list_new_ad_by_img_title(conn, cursor, img_title, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT id
                        ,type
                        ,img_title
                        ,img_url
                        ,url
                        ,is_actived
                FROM mz_common_newad
                WHERE img_title LIKE %s
                ORDER BY id
                limit %s,%s
            """, (img_title, start_index, page_size))
        newAds = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_newad WHERE img_title LIKE %s
            """, (img_title,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    newAd_dict = {
        "result": newAds,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=newAd_dict)
