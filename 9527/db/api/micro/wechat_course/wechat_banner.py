#!/usr/bin/env python
# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def insert_wechat_banner(conn, cursor, banner_dict):
    sql = """
            INSERT INTO mz_wechat_banner (title, image_url, url, `index`, date_time) VALUES (%s, %s, %s, %s, NOW())
          """
    try:
        cursor.execute(sql, (banner_dict["title"], banner_dict["image_url"], banner_dict["url"],
                             banner_dict["index"],))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_wechat_banner_by_id(conn, cursor, banner_dict):
    sql = """
            UPDATE mz_wechat_banner SET title=%s, image_url=%s, url=%s, `index`=%s
            WHERE id=%s
          """
    try:
        cursor.execute(sql, (banner_dict["title"], banner_dict["image_url"], banner_dict["url"],
                             banner_dict["index"], banner_dict["id"]))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_wechat_banner_by_id(conn, cursor, banner_id):
    sql = """
            SELECT title, image_url, url, `index`, date_time, id
            FROM mz_wechat_banner
            WHERE id=%s
         """
    try:
        cursor.execute(sql, (banner_id,))
        wechat_course = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=wechat_course)


@dec_timeit
@dec_make_conn_cursor
def del_wechat_banner_by_id(conn, cursor, banner_id):
    sql = """
            DELETE FROM mz_wechat_banner
            WHERE id=%s
         """
    try:
        cursor.execute(sql, (banner_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def list_wechat_all_banner(conn, cursor, page_index, page_size):
    start_index = get_page_info(page_index, page_size)
    sql = """
            SELECT title, image_url, url, `index`, date_time, id
            FROM mz_wechat_banner
            ORDER by `index` DESC
            limit %s, %s
         """
    try:
        cursor.execute(sql, (start_index, page_size,))
        wechat_banners = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_wechat_banner
            """, )
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    wechart_banner_dict = {
        "result": wechat_banners,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=wechart_banner_dict)
