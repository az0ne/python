# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils import tool


@dec_timeit
@dec_make_conn_cursor
def insert_career_ad(conn, cursor, career_id, img_url, img_title, is_actived, ad_type, url, bgcolor):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                insert into mz_common_careerad (career_id, img_url, img_title, is_actived, type, url, bgcolor) values (%s,%s,%s,%s,%s,%s,%s )
            """, (career_id, img_url, img_title, is_actived, ad_type, url, bgcolor))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_career_ad(conn, cursor, _id, career_id, img_url, img_title, is_actived, ad_type, url, bgcolor):
    """
    returns: true/false
    """

    try:
        cursor.execute(
            """
                UPDATE mz_common_careerad SET career_id=%s, img_url=%s, img_title=%s, is_actived=%s, type=%s, url=%s, bgcolor=%s WHERE id = %s
            """, (career_id, img_url, img_title, is_actived, ad_type, url, bgcolor, _id))

        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_career_ad_is_actived(conn, cursor):
    """
    update table is_actived=1,Because there are only 1 active states in the mz_common_usercenterad
    :param conn:
    :param cursor:
    :return:
    """

    try:
        cursor.execute(
            """
                UPDATE mz_common_careerad SET is_actived=REPLACE(is_actived,1,0)
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
def delete_career_ad(conn, cursor, _id):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_common_careerad WHERE id=%s;
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
def list_career_ad(conn, cursor):
    """
    """

    try:
        cursor.execute(
            """
                SELECT
                    careerad.id,
                    careerad.img_url,
                    careerad.img_title,
                    careerad.is_actived,
                    careerad.type,
                    careerad.career_id
                    careerad.url,
                    careerad.bgcolor,
                    career.name AS career_name
                FROM
                mz_common_careerad AS careerad
                LEFT JOIN mz_course_careercourse AS career ON career.id = careerad.career_id
                GROUP BY
                    careerad.id
            """)
        careerAds = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerAds)


@dec_timeit
@dec_make_conn_cursor
def list_career_ad_by_page(conn, cursor, page_index, page_size):
    """

    """
    start_index = tool.get_page_info(page_index, page_size)

    try:
        cursor.execute(
            """
                SELECT
                    careerad.id,
                    careerad.img_url,
                    careerad.img_title,
                    careerad.is_actived,
                    careerad.type,
                    careerad.career_id,
                    careerad.url,
                    careerad.bgcolor,
                    career.name AS career_name
                FROM
                mz_common_careerad AS careerad
                LEFT JOIN mz_course_careercourse AS career ON career.id = careerad.career_id
                GROUP BY careerad.id
                ORDER BY careerad.id DESC
                limit %s,%s
            """, (start_index, page_size,))

        careerAds = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_careerad
            """)

        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    careerAd_dict = {
        "result": careerAds,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=careerAd_dict)


@dec_timeit
@dec_make_conn_cursor
def get_career_ad_by_id(conn, cursor, _id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT
                    careerad.id,
                    careerad.img_url,
                    careerad.img_title,
                    careerad.is_actived,
                    careerad.type,
                    careerad.career_id,
                    careerad.url,
                    careerad.bgcolor,
                    career.name AS career_name
                FROM
                mz_common_careerad AS careerad
                LEFT JOIN mz_course_careercourse AS career ON career.id = careerad.career_id
                WHERE careerad.id=%s
                GROUP BY careerad.id
            """, (_id,))

        careerAds = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerAds)


@dec_timeit
@dec_make_conn_cursor
def list_career_ad_by_img_title(conn, cursor, img_title, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT
                    careerad.id,
                    careerad.img_url,
                    careerad.img_title,
                    careerad.is_actived,
                    careerad.type,
                    careerad.career_id,
                    careerad.url,
                    careerad.bgcolor,
                    career.name AS career_name
                FROM
                mz_common_careerad AS careerad
                LEFT JOIN mz_course_careercourse AS career ON career.id = careerad.career_id
                WHERE careerad.img_title LIKE %s
                GROUP BY careerad.id
                ORDER BY careerad.id
                limit %s,%s
            """, (img_title, start_index, page_size))

        careerAds = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_careerad WHERE img_title LIKE %s
            """, (img_title,))

        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    careerAd_dict = {
        "result": careerAds,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=careerAd_dict)
