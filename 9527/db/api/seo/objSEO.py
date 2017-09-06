# -*-coding:utf-8-*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils import tool


@dec_timeit
@dec_make_conn_cursor
def insert_obj_seo(conn, cursor, object_type, object_id, seo_title, seo_keywords, seo_description):
    '''
    '''

    try:
        cursor.execute("""
        INSERT INTO mz_common_objseo (obj_id,obj_type,seo_title,seo_keywords,seo_description)
        VALUE (%s,%s,%s,%s,%s)
        """, (object_id, object_type, seo_title, seo_keywords, seo_description))
        conn.commit()

    except Exception as e:
        print e
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_obj_seo(conn, cursor, _id, object_type, object_id, seo_title, seo_keywords, seo_description):
    '''
    '''

    try:
        cursor.execute(
            """
            UPDATE mz_common_objseo SET obj_id=%s, obj_type=%s, seo_title=%s,
             seo_keywords=%s, seo_description=%s WHERE id=%s
            """, (object_id, object_type, seo_title, seo_keywords, seo_description, _id)
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
def delete_obj_seo(conn, cursor, _id):
    '''
    :param conn:
    :param cursor:
    :param _id:
    :return:
    '''

    try:
        cursor.execute(
            """
            DELETE  FROM mz_common_objseo WHERE id=%s
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
def get_obj_seo_by_id(conn, cursor, _id):
    '''

    :param conn:
    :param cursor:
    :param _id:
    :return:
    '''

    try:
        cursor.execute(
            """
            SELECT objseo.id,objseo.obj_id, objseo.obj_type,
                CASE objseo.obj_type
                WHEN 'ARTICLE' THEN (SELECT article.title FROM mz_common_newarticle AS article
                WHERE article.id=objseo.obj_id )
                WHEN 'COURSE' THEN (SELECT course.name FROM mz_course_careercourse AS course
                WHERE course.id=objseo.obj_id)
                WHEN 'LESSON' THEN (SELECT lesson.name FROM mz_course_lesson AS lesson
                WHERE lesson.id=objseo.obj_id)
                END AS obj_name,objseo.seo_title,objseo.seo_keywords, objseo.seo_description
                FROM mz_common_objseo AS objseo WHERE objseo.id=%s
            """, (_id,)
        )
        obj_seo = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=obj_seo)


@dec_timeit
@dec_make_conn_cursor
def list_obj_seo_by_page(conn, cursor, page_index, page_size):
    '''

    :param conn:
    :param cursro:
    :param page_index:
    :param page_size:
    :return:
    '''

    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT objseo.id,objseo.obj_id, objseo.obj_type,
                CASE objseo.obj_type
                WHEN 'ARTICLE' THEN (SELECT article.title FROM mz_common_newarticle AS article
                WHERE article.id=objseo.obj_id )
                WHEN 'COURSE' THEN (SELECT course.name FROM mz_course_careercourse AS course
                WHERE course.id=objseo.obj_id)
                WHEN 'LESSON' THEN (SELECT lesson.name FROM mz_course_lesson AS lesson
                WHERE lesson.id=objseo.obj_id)
                END AS obj_name,objseo.seo_title,objseo.seo_keywords, objseo.seo_description
                FROM mz_common_objseo AS objseo

                GROUP BY objseo.id
                ORDER BY objseo.id DESC
                LIMIT %s,%s
            """, (start_index, page_size)
        )
        obj_seo = cursor.fetchall()

        cursor.execute(
            """
            SELECT count(*) AS count FROM mz_common_objseo
            """
        )
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    obj_seo_dict = {
        "result": obj_seo,
        "rows_count": rows_count["count"],
        "page_count": page_count
    }

    return APIResult(result=obj_seo_dict)


@dec_timeit
@dec_make_conn_cursor
def list_obj_seo_by_seo_title(conn, cursor, seo_title, page_index, page_size):
    """

    :param conn:
    :param cursor:
    :param seo_title:
    :param page_index:
    :param page_size:
    :return:
    """

    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT objseo.id,objseo.obj_id, objseo.obj_type,

            CASE objseo.obj_type
            WHEN 'ARTICLE' THEN (SELECT article.title FROM mz_common_newarticle AS article
            WHERE article.id=objseo.obj_id )
            WHEN 'COURSE' THEN (SELECT course.name FROM mz_course_careercourse AS course
            WHERE course.id=objseo.obj_id)
            WHEN 'LESSON' THEN (SELECT lesson.name FROM mz_course_lesson AS lesson
            WHERE lesson.id=objseo.obj_id)
            END AS obj_name,objseo.seo_title,objseo.seo_keywords, objseo.seo_description
            FROM mz_common_objseo AS objseo WHERE objseo.seo_title LIKE %s
            GROUP BY objseo.id
            ORDER BY objseo.id
            limit %s,%s
            """, (seo_title, start_index, page_size)
        )
        obj_seo = cursor.fetchall()

        cursor.execute(
            """
            SELECT count(*) as count
            FROM mz_common_objseo AS objseo WHERE objseo.seo_title LIKE %s
            """, (seo_title,)
        )
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    obj_seo_dict = {
        "result": obj_seo,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=obj_seo_dict)


@dec_timeit
@dec_make_conn_cursor
def delete_objSEO_by_obj(conn, cursor, _id, obj_type):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                DELETE FROM mz_common_objseo WHERE obj_id=%s AND obj_type=%s;
            """, (_id,obj_type,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_objSEO_by_obj(conn, cursor,obj_type,obj_id):

    '''

    :param conn:
    :param cursor:
    :param _id:
    :return:
    '''

    try:
        cursor.execute(
            """
            SELECT seo_title,seo_keywords,seo_description
            FROM mz_common_objseo
            WHERE obj_type=%s AND obj_id=%s
            """, (obj_type,obj_id,)
        )
        obj_seo = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=obj_seo)


@dec_timeit
@dec_make_conn_cursor
def update_objSEO_by_obj(conn, cursor,dict_obj):

    '''

    :param conn:
    :param cursor:
    :param _id:
    :return:
    '''

    try:
        cursor.execute(
            """
            UPDATE mz_common_objseo SET seo_title=%s,seo_keywords=%s,seo_description=%s
            WHERE obj_id=%s AND obj_type=%s
            """, ( dict_obj['seo_title'], dict_obj['seo_keywords'], dict_obj['seo_description'], dict_obj['obj_id'], dict_obj['obj_type'],)
        )
        conn.commit()
    except Exception as e:
        print e
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def count_have_obj_seo(conn, cursor,obj_id,obj_type):

     try:
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_common_objseo
                WHERE obj_id=%s AND obj_type=%s
            """, (obj_id,obj_type))
        count = cursor.fetchone()["count"]
     except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

     return APIResult(result=count)