#!/usr/bin/env python
# -*- coding:utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def course_page_wiki_list(conn, cursor):
    """
        获取所有的课程大纲页wiki笔记信息，按课程排序
    """

    try:
        cursor.execute(
            """
            SELECT wiki.id,wiki.title,wiki.title_image,wiki.wiki_url,wiki.career_id, course.name,course.id as course_id
            FROM mz_common_wiki as wiki
            LEFT JOIN mz_course_careercourse as course ON course.id=wiki.career_id
            ORDER BY id
            """
        )
        course_page_wiki = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=course_page_wiki)


@dec_timeit
@dec_make_conn_cursor
def get_course_page_wiki_list_by_career_id(conn, cursor, career_id):
    """
        获取所有的课程大纲页wiki笔记信息，按课程排序
    """

    try:
        cursor.execute(
            """
            SELECT wiki.id,wiki.title,wiki.title_image,wiki.wiki_url,wiki.career_id, course.name,course.id as course_id
            FROM mz_common_wiki as wiki
            LEFT JOIN mz_course_careercourse as course ON course.id=wiki.career_id
            WHERE course.id=%s
            """, (career_id,)
        )
        course_page_wiki = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=course_page_wiki)


@dec_timeit
@dec_make_conn_cursor
def get_course_wiki_by_id(conn, cursor, _id):
    '''
    根据id获取课程大纲页wiki的数据
    :param conn:
    :param cursor:
    :param _id: mz_common_wiki 的 id
    :return: None/dict()
    '''

    try:
        cursor.execute(
            """
                SELECT id,title,career_id,title_image,wiki_url
                FROM mz_common_wiki
                WHERE id=%s;
            """, (_id,)
        )
        course_page_wiki = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=course_page_wiki)


@dec_timeit
@dec_make_conn_cursor
def update_course_wiki(conn, cursor, data):
    """
    根据id更新首页wiki的信息
    :param data: {"title":title,……}
    :param conn:
    :param cursor:
    :param _id:
    :return: true/false
    """
    try:
        cursor.execute(
            """
                update mz_common_wiki set title=%s,wiki_url=%s,title_image=%s WHERE id=%s
            """, (data['title'], data['wiki_url'], data['image_path'], data['id'],)
        )
        conn.commit()
    except Exception as e:
        log.warn(
            "cursor exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=True)
