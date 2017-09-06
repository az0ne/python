# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def list_feed_back_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT  id ,content,feed_type,publish_date,contact,user_id,nick_name,image_url,current_url,record
                FROM mz_common_newfeedback
                ORDER BY publish_date DESC
                limit %s,%s
            """, (start_index, page_size,))
        feed_back = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_newfeedback
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    feedBack_dict = {
        "result": feed_back,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=feedBack_dict)


@dec_timeit
@dec_make_conn_cursor
def get_feed_back_by_keyword(conn, cursor, page_index, page_size,keyword):
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT id ,content,feed_type,publish_date,contact,user_id,nick_name,image_url,current_url,record
                FROM mz_common_newfeedback
                WHERE content LIKE %s or feed_type LIKE %s or nick_name LIKE %s
                ORDER BY publish_date DESC
                limit %s,%s
            """, (keyword, keyword, keyword, start_index, page_size,))
        feed_back = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_newfeedback
                WHERE content LIKE %s or feed_type LIKE %s or nick_name LIKE %s
            """,(keyword, keyword, keyword,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    feed_back_dict = {
        "result": feed_back,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=feed_back_dict)


@dec_timeit
@dec_make_conn_cursor
def get_feed_back_by_type(conn, cursor, page_index, page_size,type):
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT id ,content,feed_type,publish_date,contact,user_id,nick_name,image_url,current_url,record
                FROM mz_common_newfeedback
                WHERE  feed_type LIKE %s
                ORDER BY publish_date DESC
                limit %s,%s
            """, (type, start_index, page_size,))
        feed_back = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_newfeedback
                WHERE  feed_type LIKE %s
            """,(type,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    feed_back_dict = {
        "result": feed_back,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=feed_back_dict)

@dec_timeit
@dec_make_conn_cursor
def delete_feed_back_by_id(conn, cursor, _id):
    '''
    :param conn:
    :param cursor:
    :param _id:
    :return:
    '''

    try:
        cursor.execute(
            """
            DELETE FROM mz_common_newfeedback WHERE id=%s
            """, (_id,)
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
def list_feed_back(conn, cursor):
    '''
    :param conn:
    :param cursor:
    :return: all feed back data in a list
    '''

    try:
        cursor.execute(
            """
            SELECT id, feed_type, content, contact, publish_date, nick_name,image_url,current_url,record
            FROM mz_common_newfeedback
            ORDER BY id DESC
            """, ()
        )
        feed_back = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=feed_back)


@dec_timeit
@dec_make_conn_cursor
def get_feed_back_by_id(conn, cursor, id):
    '''
    :param conn:
    :param cursor:
    :return: {}/Nones
    '''

    try:
        cursor.execute(
            """
            SELECT id, feed_type, content, contact, publish_date, nick_name,image_url,current_url,record
            FROM mz_common_newfeedback
            WHERE id=%s
            """, (id,)
        )
        feed_back = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=feed_back)


@dec_timeit
@dec_make_conn_cursor
def update_feed_back_by_id(conn, cursor, _id, record):
    '''
    :param conn:
    :param cursor:
    :param _id:
    :return:
    '''

    try:
        cursor.execute(
            """
            UPDATE mz_common_newfeedback SET record=%s
            WHERE id=%s;
            """, (record, _id,)
        )
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=True)