# -*- coding: utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def update_wechat_question_by_id(conn, cursor, question_dict):
    """
    更新微课问答的回复内容
    :param conn:
    :param cursor:
    :param answer:回复内容
    :param _id:问答id
    :return: result():True/False
    """

    try:
        cursor.execute(
            """
            UPDATE mz_wechat_course_question set course_id=%s, answer=%s,nick_name=%s,avatar_url=%s,question=%s
            WHERE id=%s;
            """, (question_dict["course_id"], question_dict["answer"], question_dict["nick_name"],
                      question_dict["avatar_url"], question_dict["question"], question_dict["id"]))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def insert_wechat_question(conn, cursor, question_dict):
    """
    更新微课问答的回复内容
    :param conn:
    :param cursor:
    :param answer:回复内容
    :param _id:问答id
    :return: result():True/False
    """

    try:
        cursor.execute(
            """
            INSERT INTO mz_wechat_course_question (course_id, nick_name, avatar_url, question, answer)
            VALUES (%s,%s,%s,%s,%s)
            """, (question_dict["course_id"], question_dict["nick_name"], question_dict["avatar_url"],
                      question_dict["question"], question_dict["answer"],))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_wechat_question_by_id(conn, cursor, _id):
    """

    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
        cursor.execute(
            """
            SELECT question.id, course_id, nick_name, avatar_url, question, answer, course.name as course_name
            FROM mz_wechat_course_question as question
            LEFT JOIN mz_wechat_course as course
            ON question.course_id=course.id
            WHERE question.id=%s;
            """, (_id,))
        ask = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=ask)


@dec_timeit
@dec_make_conn_cursor
def list_wechat_question(conn, cursor, page_index, page_size):
    """
    显示微课问答列表
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT question.id, course_id, nick_name, avatar_url, question, answer,course.name as course_name
                FROM mz_wechat_course_question as question
                LEFT JOIN mz_wechat_course as course
                ON question.course_id=course.id
                ORDER BY course_id DESC,id DESC
                limit %s,%s
            """, (start_index, page_size,))
        micro_course_ask = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_wechat_course_question
            """, )
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
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


#
# @dec_timeit
# @dec_make_conn_cursor
# def get_micro_ask_by_keyword_and_status(conn, cursor, page_index, page_size, keyword, course_id, status):
#     start_index = tool.get_page_info(page_index, page_size)
#     try:
#         if status == 1: #选择已回复
#             cursor.execute(
#                 """
#                     SELECT id, course_id, nick_name, avatar_url, question, answer
#                     FROM mz_wechat_course_question
#                     WHERE course_id=%s AND (content LIKE %s OR nick_name LIKE %s OR answer LIKE %s) AND(answer is not null OR answer_time is not null)
#                     ORDER BY praise_count DESC,ask_time DESC,id DESC
#                     limit %s,%s
#                 """, (course_id, keyword, keyword, keyword, start_index, page_size,))
#             micro_ask = cursor.fetchall()
#
#             cursor.execute(
#                 """
#                     SELECT count(*) as count
#                     FROM mz_wechat_course_question
#                     WHERE course_id=%s AND (content LIKE %s OR nick_name LIKE %s OR answer LIKE %s) AND(answer is not null OR answer_time is not null)
#                 """,(course_id, keyword, keyword, keyword,))
#
#         elif status == 2: #选择未回复
#             cursor.execute(
#                 """
#                     SELECT id, micro_course_id, nick_name, content, ask_time, praise_count,answer,answer_time
#                     FROM mz_micro_course_ask
#                     WHERE micro_course_id=%s AND (content LIKE %s OR nick_name LIKE %s OR answer LIKE %s) AND(answer is null AND answer_time is null)
#                     ORDER BY  praise_count DESC,ask_time DESC,id DESC
#                     limit %s,%s
#                 """, (course_id, keyword, keyword, keyword, start_index, page_size,))
#             micro_ask = cursor.fetchall()
#
#             cursor.execute(
#                 """
#                     SELECT count(*) as count
#                     FROM mz_micro_course_ask
#                     WHERE micro_course_id=%s AND (content LIKE %s OR nick_name LIKE %s OR answer LIKE %s) AND(answer is null AND answer_time is null)
#                 """,(course_id, keyword, keyword, keyword,))
#
#         else: #选择全部
#             cursor.execute(
#                 """
#                     SELECT id, micro_course_id, nick_name, content, ask_time, praise_count,answer,answer_time
#                     FROM mz_micro_course_ask
#                     WHERE micro_course_id=%s AND (content LIKE %s OR nick_name LIKE %s OR answer LIKE %s)
#                     ORDER BY praise_count DESC,ask_time DESC,id DESC
#                     limit %s,%s
#                 """, (course_id, keyword, keyword, keyword, start_index, page_size,))
#             micro_ask = cursor.fetchall()
#
#             cursor.execute(
#                 """
#                     SELECT count(*) as count
#                     FROM mz_micro_course_ask
#                     WHERE micro_course_id=%s AND (content LIKE %s OR nick_name LIKE %s OR answer LIKE %s)
#                 """,(course_id, keyword, keyword, keyword,))
#         rows_count = cursor.fetchone()
#         page_count = tool.get_page_count(rows_count["count"], page_size)
#
#     except Exception as e:
#         log.warn(
#             "execute exception: %s. "
#             "statement:%s" % (e, cursor.statement))
#         raise e
#
#     micro_ask_dict = {
#         "result": micro_ask,
#         "rows_count": rows_count["count"],
#         "page_count": page_count,
#     }
#
#     return APIResult(result=micro_ask_dict)



@dec_timeit
@dec_make_conn_cursor
def delete_wechat_question_by_id(conn, cursor, _id):
    """
    更新微课问答的回复内容
    :param conn:
    :param cursor:
    :param answer:回复内容
    :param _id:问答id
    :return: result():True/False
    """

    try:
        cursor.execute(
            """
            DELETE FROM mz_wechat_course_question
            WHERE id=%s;
            """, (_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)
