# -*- coding: utf-8 -*-

from db.api.apiutils import APIResult
from db.cores.mysqlconn import dec_make_conn_cursor
from utils.tool import dec_timeit, get_page_info, get_page_count
from utils.logger import logger as log


@dec_make_conn_cursor
@dec_timeit
def get_ad_info_by_career_id(conn, cursor, career_id):
    sql = """
            select career_id, title, img_url, callback_url
            from mz_app_career_ad WHERE career_id=%s
          """
    try:
        cursor.execute(sql, (career_id,))
        ad = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=ad)


@dec_timeit
@dec_make_conn_cursor
def list_all_app_career_ad(conn, cursor, page_index, page_size):
    start_index = get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
               SELECT career_id, title, img_url, callback_url, career.name as career_name
               FROM mz_app_career_ad as ad
               LEFT JOIN mz_lps4_career as career
               ON ad.career_id=career.id
               limit %s, %s;
            """, (start_index, page_size,))
        app_ads = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_app_career_ad
            """, ())
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    backlog_dict = {
        "result": app_ads,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=backlog_dict)


@dec_make_conn_cursor
@dec_timeit
def insert_ad_info(conn, cursor, ad_info):
    sql = """
            INSERT INTO mz_app_career_ad
            (career_id,title,img_url,callback_url)
            VALUES (%s,%s,%s,%s)
          """
    try:
        cursor.execute(sql, (
            ad_info.get('career_id'), ad_info.get('title'), ad_info.get('img_url'), ad_info.get('callback_url')))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_make_conn_cursor
@dec_timeit
def update_ad_info(conn, cursor, ad_info):
    sql = """
            UPDATE mz_app_career_ad
            SET title=%s,img_url=%s,callback_url=%s
            WHERE career_id=%s
          """
    try:
        cursor.execute(sql, (
            ad_info.get('title'), ad_info.get('img_url'), ad_info.get('callback_url'), ad_info.get('career_id')))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_make_conn_cursor
@dec_timeit
def delete_ad_info_by_career_id(conn, cursor, career_id):
    sql = """
            DELETE FROM mz_app_career_ad WHERE career_id=%s
          """
    try:
        cursor.execute(sql, (career_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_make_conn_cursor
@dec_timeit
def check_app_ad_is_have_career(conn, cursor, career_id):
    sql = """
            SELECT count(*) as count
            FROM mz_app_career_ad
            WHERE career_id=%s
        """
    try:
        cursor.execute(sql, (career_id,))
        row_count = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=row_count)
