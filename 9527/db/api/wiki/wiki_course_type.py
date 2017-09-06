# -*- coding: utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def insert_wiki_course_type(conn, cursor, dict):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                insert into mz_wiki_course_type (name,short_name,img_title,img_url,`index`) values (%s,%s,%s,%s,%s);
            """, (dict['name'],dict['short_name'],dict['img_title'],dict['img_url'],dict['index'],))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_wiki_course_type(conn, cursor, dict):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                update mz_wiki_course_type set name=%s,short_name=%s,img_title=%s,img_url=%s,`index`=%s  WHERE id=%s;
            """, (dict['name'],dict['short_name'],dict['img_title'],dict['img_url'],dict['index'],dict['id'],))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def list_wikiCourseType_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT id, name,short_name,img_title,img_url,`index`
                FROM mz_wiki_course_type
                limit %s,%s
            """, (start_index, page_size,))
        wikiCourseType = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_wiki_course_type

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
        "result": wikiCourseType,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=article_dict)



@dec_timeit
@dec_make_conn_cursor
def list_wiki_course_type(conn, cursor):
    """

    """
    try:
        cursor.execute(
            """
                SELECT id, name,short_name,img_title,img_url,`index`
                FROM mz_wiki_course_type
            """)
        wikiCourseType = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=wikiCourseType)


@dec_timeit
@dec_make_conn_cursor
def delete_wiki_course_type(conn, cursor,_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
             DELETE type,course,chapter,item
             FROM mz_wiki_course_type as type
             LEFT JOIN mz_wiki_course as course ON type.id=course.type_id
             LEFT JOIN mz_wiki_chapter as chapter ON chapter.course_id=course.id
             LEFT JOIN mz_wiki_item as item ON item.chapter_id=chapter.id
             WHERE type.id=%s;
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
def count_have_wikiCourseType_short_name(conn, cursor,short_name):

     try:
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_wiki_course_type
                WHERE short_name=%s
            """, (short_name,))
        count = cursor.fetchone()["count"]
     except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

     return APIResult(result=count)


@dec_timeit
@dec_make_conn_cursor
def get_wikiCourseType_by_id(conn, cursor, _id):
    """
    """

    try:
        cursor.execute(
            """
                SELECT id,name,short_name,img_title,img_url,`index`
                FROM mz_wiki_course_type WHERE id = %s
            """, (_id,))
        wikiCourseType = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=wikiCourseType)
