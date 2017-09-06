# -*- coding: utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def insert_wiki_chapter(conn, cursor, dict_chapter):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                insert into mz_wiki_chapter (name,course_id,`index`,video_course_id) values (%s,%s,%s,%s);
            """,
            (dict_chapter['name'], dict_chapter['course_id'], dict_chapter['index'], dict_chapter['video_course_id']))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_wiki_chapter(conn, cursor, dict_chapter):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                update mz_wiki_chapter set name=%s,course_id=%s ,`index`=%s, video_course_id=%s WHERE id=%s;
            """, (dict_chapter['name'], dict_chapter['course_id'], dict_chapter['index'], dict_chapter["video_course_id"],
                      dict_chapter['id'],))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def list_wiki_chapter(conn, cursor):
    """

    """
    try:
        cursor.execute(
            """
                SELECT id, name,course_id
                FROM mz_wiki_chapter
                ORDER BY `index`,id
            """)
        wikiCourse = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=wikiCourse)


# 是否需要删除？#
@dec_timeit
@dec_make_conn_cursor
def delete_wiki_chapter(conn, cursor, _id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
             DELETE chapter.*,item.*
             FROM mz_wiki_chapter as chapter
             LEFT JOIN mz_wiki_item as item ON item.chapter_id=chapter.id
             WHERE chapter.id=%s;
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
def count_have_the_wikiChapter_name(conn, cursor, name):
    try:
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_wiki_chapter
                WHERE name=%s
            """, (name,))
        count = cursor.fetchone()["count"]
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=count)


@dec_timeit
@dec_make_conn_cursor
def get_wiki_chapters_by_course(conn, cursor, course_id):
    """

    """
    try:
        cursor.execute(
            """
                SELECT id, name,course_id,`index`
                FROM mz_wiki_chapter
                WHERE course_id=%s
                ORDER BY `index` ,id
            """, (course_id,))
        wikiChapters = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=wikiChapters)


@dec_timeit
@dec_make_conn_cursor
def get_wiki_chapter_by_id(conn, cursor, _id):
    """

    """
    try:
        cursor.execute(
            """
                SELECT id, name,course_id,`index`,video_course_id
                FROM mz_wiki_chapter
                WHERE id=%s
            """, (_id,))
        wikiChapter = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=wikiChapter)
