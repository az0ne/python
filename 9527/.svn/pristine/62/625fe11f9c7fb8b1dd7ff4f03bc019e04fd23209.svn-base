# -*- coding: utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def list_courseTag(conn, cursor):
    """
    """

    try:
        cursor.execute(
            """
                SELECT id,name,is_hot_tag
                FROM mz_course_tag
            """)

        courseTag = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=courseTag)


@dec_timeit
@dec_make_conn_cursor
def insert_tag(conn, cursor, name, is_hot_tag):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                insert into mz_course_tag (name,is_hot_tag) values (%s,%s);
            """, (name,is_hot_tag,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_tag_by_id(conn, cursor,_id, name, is_hot_tag):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                update mz_course_tag set name=%s,is_hot_tag=%s WHERE id=%s;
            """, (name, is_hot_tag,_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_tag_by_id(conn, cursor,_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
               DELETE FROM mz_course_tag WHERE id=%s;
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
def list_tags_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT id, name,is_homepage,short_name
                FROM mz_common_articletype
                limit %s,%s
            """, (start_index, page_size,))
        articleType = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_articletype

            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    article_dict = {
        "result": articleType,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=article_dict)

