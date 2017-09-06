# -*- coding:utf-8 -*-
__author__ = 'qlp'
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from utils import tool
from db.api.apiutils import APIResult
from utils.logger import logger as log


@dec_timeit
@dec_make_conn_cursor
def get_all_lps4_career(conn, cursor):
    try:
        cursor.execute(
            """
               SELECT id,`name`,`type`,price,old_price,url,ad_url,ad_type,jobless_price,description,short_name,video_url
               FROM mz_lps4_career
           """)
        careers = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=careers)


@dec_timeit
@dec_make_conn_cursor
def career_data(conn, cursor, career_id):
    try:
        cursor.execute(
            """
            SELECT id,`name`,`type`,ad_url,url,ad_type,price,old_price ,jobless_price,description,short_name,video_url
            FROM mz_lps4_career WHERE id = %s;
            """
            , (career_id,))
        cardata = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=cardata)


@dec_timeit
@dec_make_conn_cursor
def up_career_name(conn, cursor, data):
    try:
        cursor.execute(
            """
            UPDATE mz_lps4_career SET `name` = %s,ad_type=%s,ad_url=%s,url=%s,old_price=%s,price=%s,`type`=%s,
            jobless_price=%s,description=%s,short_name=%s,video_url=%s
            WHERE id = %s;
            """,
            (data["name"], data["ad_type"], data["ad_url"], data["url"], data["old_price"], data["price"], data["type"],
             data["jobless_price"], data["description"], data["short_name"], data["video_url"], data["id"]))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def insert_career(conn, cursor, data):
    try:
        cursor.execute(
            """
            INSERT INTO mz_lps4_career(id,`name`,`type`,ad_type,ad_url,url,price,old_price,jobless_price,
            description,short_name,video_url)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            , (data["id"],data["name"],data["type"],data["ad_type"],data["ad_url"],data["url"],data["price"],
               data["old_price"],data["jobless_price"],data["description"],data["short_name"],data["video_url"]))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statament: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_count_by_short_name(conn, cursor, short_name):
    try:
        cursor.execute(
            """
            SELECT count(*) as count, id
            FROM mz_lps4_career
            WHERE short_name = %s;
            """
            , (short_name,))
        info = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=info)

