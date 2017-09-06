# -*- coding: utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor

@dec_timeit
@dec_make_conn_cursor
def update_micro_ask_by_id(conn, cursor, answer, answer_time, _id):
    """
    更新微课问答的回复内容及时间
    :param conn:
    :param cursor:
    :param answer:回复内容
    :param answer_time:回复时间
    :param _id:问答id
    :return: result():True/False
    """

    try:
        cursor.execute(
                """
                UPDATE mz_micro_course_ask set answer=%s,answer_time=%s
                WHERE id=%s;
                """, (answer, answer_time, _id,))
        conn.commit()
    except Exception as e:
        log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_micro_ask_by_id(conn, cursor, _id):
    """

    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
        cursor.execute(
                """
                SELECT id, micro_course_id, nick_name, content, ask_time, praise_count,answer,answer_time
                FROM mz_micro_course_ask
                WHERE id=%s;
                """, (_id,))
        ask = cursor.fetchall()
    except Exception as e:
        log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=ask)


@dec_timeit
@dec_make_conn_cursor
def list_micro_course_ask_by_page(conn, cursor, page_index, page_size, course_id):
    """
    显示微课问答列表
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT id, micro_course_id, nick_name, content, ask_time, praise_count,answer,answer_time
                FROM mz_micro_course_ask
                WHERE micro_course_id=%s
                ORDER BY praise_count DESC,id DESC
                limit %s,%s
            """, (course_id, start_index, page_size,))
        micro_course_ask = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_micro_course_ask
                WHERE micro_course_id=%s
            """, (course_id,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    micro_ask_dict = {
        "result": micro_course_ask,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=micro_ask_dict)



@dec_timeit
@dec_make_conn_cursor
def get_micro_ask_by_keyword_and_status(conn, cursor, page_index, page_size, keyword, course_id, status):
    start_index = tool.get_page_info(page_index, page_size)
    try:
        if status == 1: #选择已回复
            cursor.execute(
                """
                    SELECT id, micro_course_id, nick_name, content, ask_time, praise_count,answer,answer_time
                    FROM mz_micro_course_ask
                    WHERE micro_course_id=%s AND (content LIKE %s OR nick_name LIKE %s OR answer LIKE %s) AND(answer is not null OR answer_time is not null)
                    ORDER BY praise_count DESC,ask_time DESC,id DESC
                    limit %s,%s
                """, (course_id, keyword, keyword, keyword, start_index, page_size,))
            micro_ask = cursor.fetchall()

            cursor.execute(
                """
                    SELECT count(*) as count
                    FROM mz_micro_course_ask
                    WHERE micro_course_id=%s AND (content LIKE %s OR nick_name LIKE %s OR answer LIKE %s) AND(answer is not null OR answer_time is not null)
                """,(course_id, keyword, keyword, keyword,))

        elif status == 2: #选择未回复
            cursor.execute(
                """
                    SELECT id, micro_course_id, nick_name, content, ask_time, praise_count,answer,answer_time
                    FROM mz_micro_course_ask
                    WHERE micro_course_id=%s AND (content LIKE %s OR nick_name LIKE %s OR answer LIKE %s) AND(answer is null AND answer_time is null)
                    ORDER BY  praise_count DESC,ask_time DESC,id DESC
                    limit %s,%s
                """, (course_id, keyword, keyword, keyword, start_index, page_size,))
            micro_ask = cursor.fetchall()

            cursor.execute(
                """
                    SELECT count(*) as count
                    FROM mz_micro_course_ask
                    WHERE micro_course_id=%s AND (content LIKE %s OR nick_name LIKE %s OR answer LIKE %s) AND(answer is null AND answer_time is null)
                """,(course_id, keyword, keyword, keyword,))

        else: #选择全部
            cursor.execute(
                """
                    SELECT id, micro_course_id, nick_name, content, ask_time, praise_count,answer,answer_time
                    FROM mz_micro_course_ask
                    WHERE micro_course_id=%s AND (content LIKE %s OR nick_name LIKE %s OR answer LIKE %s)
                    ORDER BY praise_count DESC,ask_time DESC,id DESC
                    limit %s,%s
                """, (course_id, keyword, keyword, keyword, start_index, page_size,))
            micro_ask = cursor.fetchall()

            cursor.execute(
                """
                    SELECT count(*) as count
                    FROM mz_micro_course_ask
                    WHERE micro_course_id=%s AND (content LIKE %s OR nick_name LIKE %s OR answer LIKE %s)
                """,(course_id, keyword, keyword, keyword,))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    micro_ask_dict = {
        "result": micro_ask,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=micro_ask_dict)



@dec_timeit
@dec_make_conn_cursor
def delete_micro_ask_by_id(conn, cursor, _id):
    """
    更新微课问答的回复内容及时间
    :param conn:
    :param cursor:
    :param answer:回复内容
    :param answer_time:回复时间
    :param _id:问答id
    :return: result():True/False
    """

    try:
        cursor.execute(
                """
                DELETE FROM mz_micro_course_ask
                WHERE id=%s;
                """, ( _id,))
        conn.commit()
    except Exception as e:
        log.warn(
                "execute exception: %s. "
                "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)