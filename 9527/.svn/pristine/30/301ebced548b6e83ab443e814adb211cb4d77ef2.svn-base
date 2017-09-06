# -*- coding: utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def insert_wiki_item(conn, cursor, dict_item):
    """
        returns:
        result():id
        iserror():True/False
    """
    try:
        cursor.execute(
            """
                insert into mz_wiki_item (course_id,chapter_id,name,content,`index`,short_name) values (%s,%s,%s,%s,%s,%s);
            """, (dict_item['course_id'],dict_item['chapter_id'],dict_item['name'],dict_item['content'],dict_item['index'],dict_item['short_name'],))
        cursor.execute(
            """
                select last_insert_id() as newItemId;
            """)
        newItemId = cursor.fetchone()["newItemId"]
        conn.commit()
    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=newItemId)


@dec_timeit
@dec_make_conn_cursor
def update_wiki_item(conn, cursor,dict_item):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                update mz_wiki_item set course_id=%s,chapter_id=%s,name=%s,`index`=%s,short_name=%s WHERE id=%s;
            """, (dict_item['course_id'],dict_item['chapter_id'],dict_item['name'],dict_item['index'],dict_item['short_name'],dict_item['id'],))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_wiki_item_by_id(conn, cursor, _id):
    """

    """
    try:
        cursor.execute(
            """
                SELECT item.id, item.course_id,item.chapter_id,item.name,item.short_name,item.content,item.`index`,chapter.name as chapter_name
                FROM mz_wiki_item item LEFT JOIN mz_wiki_chapter chapter
                ON item.chapter_id=chapter.id
                WHERE item.id=%s
            """,(_id,))
        wikiItem = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=wikiItem)

#是否需要删除？#
@dec_timeit
@dec_make_conn_cursor
def delete_wiki_item(conn, cursor,_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
               DELETE FROM mz_wiki_item WHERE id=%s;
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
def items_have_the_wikiItem_name(conn, cursor,name):

     try:
        cursor.execute(
            """
                SELECT id, count(*) as count
                FROM mz_wiki_item
                WHERE name=%s
            """, (name,))
        Items = cursor.fetchall()
     except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

     return APIResult(result=Items)


@dec_timeit
@dec_make_conn_cursor
def get_wiki_item_by_course(conn, cursor, course_id):
    """

    """
    try:
        cursor.execute(
            """
                SELECT id, course_id,chapter_id,name,content,`index`,short_name
                FROM mz_wiki_item
                WHERE course_id=%s
                ORDER BY `index`,id
            """,(course_id,))
        wikiItem = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=wikiItem)


@dec_timeit
@dec_make_conn_cursor
def update_wiki_item_content(conn, cursor,_id,content,retrieval):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                update mz_wiki_item set content=%s,tidy_content=%s WHERE id=%s;
            """, (content,retrieval,_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def count_have_the_wikiItem_short_name(conn, cursor,short_name,course_id):

     try:
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_wiki_item
                WHERE short_name=%s AND course_id=%s
            """, (short_name,course_id))
        count = cursor.fetchone()["count"]
     except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

     return APIResult(result=count)