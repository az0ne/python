# -*- coding: utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def insert_wiki_course(conn, cursor, dict_course):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                insert into mz_wiki_course
                (`name`, short_name, type_id, course_id, `index`, img_title, img_url, is_homepage, info,
                recommend_course_id1, recommend_course_id2, recommend_course_id3, recommend_course_id4)
                values (%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s);
            """, (dict_course['name'],dict_course['short_name'],dict_course['type_id'],dict_course['course_id'],
                  dict_course['index'],dict_course['img_title'],dict_course['img_url'],dict_course['is_homepage'],
                  dict_course['info'], dict_course['recommend_course_id1'], dict_course['recommend_course_id2'],
                  dict_course['recommend_course_id3'], dict_course['recommend_course_id4']))
        conn.commit()
    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))

        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_wiki_course(conn, cursor,dict_course):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                update mz_wiki_course set
                name=%s,short_name=%s,type_id=%s,course_id=%s ,`index`=%s ,
                img_url=%s,img_title=%s ,is_homepage=%s, info=%s, recommend_course_id1=%s,
                recommend_course_id2=%s, recommend_course_id3=%s, recommend_course_id4=%s
                WHERE id=%s;
            """, (dict_course['name'],dict_course['short_name'],dict_course['type_id'],
                  dict_course['course_id'],dict_course['index'],dict_course['img_url'],
                  dict_course['img_title'],dict_course['is_homepage'],dict_course['info'],
                  dict_course['recommend_course_id1'], dict_course['recommend_course_id2'],
                  dict_course['recommend_course_id3'], dict_course['recommend_course_id4'],
                  dict_course['id']))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def list_wiki_course(conn, cursor):
    """

    """
    try:
        cursor.execute(
            """
                SELECT id,name,short_name,type_id,course_id,`index`,img_url,img_title,is_homepage,info
                FROM mz_wiki_course
                ORDER BY `index`,id
            """)
        wikiCourse = cursor.fetchall()
    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=wikiCourse)

#是否需要删除？#
@dec_timeit
@dec_make_conn_cursor
def delete_wiki_course(conn, cursor,_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
             DELETE course,chapter,item
             FROM mz_wiki_course as course
             LEFT JOIN mz_wiki_chapter as chapter ON chapter.course_id=course.id
             LEFT JOIN mz_wiki_item as item ON item.chapter_id=chapter.id
             WHERE course.id=%s;
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
def count_have_the_wikiCourse_short_name(conn, cursor,short_name):

     try:
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_wiki_course
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
def get_wiki_course_by_id(conn, cursor,_id):
    """

    """
    try:
        cursor.execute(
            """
                SELECT
                    id,
                    `name`,
                    short_name,
                    type_id,
                    course_id,
                    `index`,
                    img_url,
                    img_title,
                    is_homepage,
                    info,
                    recommend_course_id1,
                    recommend_course_id2,
                    recommend_course_id3,
                    recommend_course_id4
                FROM
                    mz_wiki_course
                WHERE
                    id = %s
            """, (_id,))
        wikiCourse = cursor.fetchall()
    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=wikiCourse)


@dec_timeit
@dec_make_conn_cursor
def get_wiki_course_by_typeid(conn, cursor,type_id):
    """

    """
    try:
        cursor.execute(
            """
                SELECT id, name,short_name,course_id,`index`,img_url,img_title,is_homepage,info
                FROM mz_wiki_course
                WHERE type_id=%s
                ORDER BY `index`,id
            """,(type_id,))
        wikiCourses = cursor.fetchall()
    except Exception as e:
        print e
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=wikiCourses)