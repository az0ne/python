# -*-coding:utf-8-*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils import tool


@dec_timeit
@dec_make_conn_cursor
def insert_obj_tag_relation(conn, cursor, obj_type, obj_id, tag_id, careercatagory_id):
    '''
    '''

    try:
        cursor.execute("""
        INSERT INTO mz_common_objtagrelation (obj_type, obj_id, tag_id, careercatagory_id)
        VALUE (%s,%s,%s,%s)
        """, (obj_type, obj_id, tag_id, careercatagory_id))
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
def update_obj_tag_relation(conn, cursor, _id, obj_type, obj_id, tag_id, careercatagory_id):
    '''
    '''

    try:
        cursor.execute(
            """
            UPDATE mz_common_objtagrelation SET obj_id=%s, obj_type=%s, tag_id=%s,
             careercatagory_id=%s WHERE id=%s
            """, (obj_type, obj_id, tag_id, careercatagory_id, _id)
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
def delete_obj_tag_relation(conn, cursor, _id):
    '''
    :param conn:
    :param cursor:
    :param _id:
    :return:
    '''

    try:
        cursor.execute(
            """
            DELETE  FROM mz_common_objtagrelation WHERE id=%s
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
def get_obj_tag_relation_by_id(conn, cursor, _id):
    '''

    :param conn:
    :param cursor:
    :param _id:
    :return:
    '''

    try:
        cursor.execute(
            """
            SELECT objtagrelation.id,objtagrelation.obj_type,objtagrelation.obj_id,
                CASE objtagrelation.obj_type
                WHEN 'ARTICLE' THEN (SELECT article.title FROM mz_common_newarticle AS article WHERE objtagrelation.obj_id=article.id)
                WHEN 'COURSE' THEN (SELECT course.name FROM mz_course_careercourse AS course WHERE course.id=objtagrelation.obj_id)
                WHEN 'LESSON' THEN (SELECT lesson.name FROM mz_course_lesson AS lesson WHERE lesson.id=objtagrelation.obj_id)
                END AS obj_name,tag.name AS tag_name,careercata.`name` AS careercatagory_name
                FROM mz_common_objtagrelation AS objtagrelation

                LEFT JOIN mz_course_careercatagory AS careercata ON objtagrelation.careercatagory_id=careercata.id
                LEFT JOIN mz_course_tag AS tag ON objtagrelation.tag_id=tag.id
                WHERE objtagrelation.id=%s
            """, (_id,)
        )
        obj_tag_relationes = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=obj_tag_relationes)


@dec_timeit
@dec_make_conn_cursor
def list_obj_tag_relation_by_page(conn, cursor, page_index, page_size):
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
                SELECT objtagrelation.id,objtagrelation.obj_type,objtagrelation.obj_id,
                CASE objtagrelation.obj_type
                WHEN 'ARTICLE' THEN (SELECT article.title FROM mz_common_newarticle AS article WHERE objtagrelation.obj_id=article.id)
                WHEN 'COURSE' THEN (SELECT course.name FROM mz_course_careercourse AS course WHERE course.id=objtagrelation.obj_id)
                WHEN 'LESSON' THEN (SELECT lesson.name FROM mz_course_lesson AS lesson WHERE lesson.id=objtagrelation.obj_id)
                END AS obj_name,tag.name AS tag_name,careercata.`name` AS careercatagory_name
                FROM mz_common_objtagrelation AS objtagrelation

                LEFT JOIN mz_course_careercatagory AS careercata ON objtagrelation.careercatagory_id=careercata.id
                LEFT JOIN mz_course_tag AS tag ON objtagrelation.tag_id=tag.id

                GROUP BY objtagrelation.id
                ORDER BY objtagrelation.id
                LIMIT %s,%s
            """, (start_index, page_size)
        )
        obj_tag_relationes = cursor.fetchall()

        cursor.execute(
            """
            SELECT count(*) AS count FROM mz_common_objtagrelation
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

    obj_tag_relation_dict = {
        "result": obj_tag_relationes,
        "rows_count": rows_count["count"],
        "page_count": page_count
    }

    return APIResult(result=obj_tag_relation_dict)


@dec_timeit
@dec_make_conn_cursor
def list_obj_tag_relation_by_name(conn, cursor, object_name, page_index, page_size):
    '''

    :param conn:
    :param cursor:
    :param object_name:
    :param page_index:
    :param page_size:
    :return:
    '''

    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
            SELECT objtagrelation.id,objtagrelation.obj_type,objtagrelation.obj_id,
                CASE objtagrelation.obj_type
                WHEN 'ARTICLE' THEN (SELECT article.title FROM mz_common_newarticle AS article WHERE objtagrelation.obj_id=article.id)
                WHEN 'COURSE' THEN (SELECT course.name FROM mz_course_careercourse AS course WHERE course.id=objtagrelation.obj_id)
                WHEN 'LESSON' THEN (SELECT lesson.name FROM mz_course_lesson AS lesson WHERE lesson.id=objtagrelation.obj_id)
                END AS obj_name,tag.name AS tag_name,careercata.`name` AS careercatagory_name
                FROM mz_common_objtagrelation AS objtagrelation

                LEFT JOIN mz_course_careercatagory AS careercata ON objtagrelation.careercatagory_id=careercata.id

                LEFT JOIN mz_course_tag AS tag ON objtagrelation.tag_id=tag.id

                GROUP BY objtagrelation.id
                ORDER BY objtagrelation.id
                LIMIT %s,%s
            """, (object_name, start_index, page_size)
        )
        obj_tag_relationes = cursor.fetchall()

        cursor.execute(
            """
            SELECT count(*) AS count FROM mz_common_objtagrelation WHERE object_name LIKE %s
            """, (object_name,)
        )
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    obj_tag_relation_dict = {
        "result": obj_tag_relationes,
        "rows_count": rows_count,
        "page_total": page_count
    }

    return APIResult(result=obj_tag_relation_dict)


@dec_timeit
@dec_make_conn_cursor
def delete_objTagRelation_by_obj(conn,cursor,_id, obj_type):
    """
    returns: true/false
    """
    try:
        cursor.execute(
            """
                DELETE FROM mz_common_objtagrelation WHERE obj_id=%s AND obj_type=%s;
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
def get_tags_by_obj(conn, cursor, _id , type_id):
     """

     """
     try:
        cursor.execute(
            """
            SELECT tag.name,tag.id
            FROM mz_common_objtagrelation AS objtagrelation LEFT JOIN mz_course_tag AS tag ON objtagrelation.tag_id=tag.id
            WHERE objtagrelation.obj_id=%s AND objtagrelation.obj_type=%s;
            """, (_id,type_id,))
        tags = cursor.fetchall()
     except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

     return APIResult(result=tags)














# @dec_timeit
# @dec_make_conn_cursor
# def get_objTagRelation_by_id(conn, cursor, _id):
#     """
#     """
#
#     try:
#         cursor.execute(
#             """
#                 SELECT  obj_id,obj_type,tag_id,careercatagory_id
#                 FROM mz_common_objtagrelation WHERE id = %s
#             """, (_id,))
#         objTagRelation = cursor.fetchone()
#     except Exception as e:
#         log.warn(
#             "execute exception: %s. "
#             "statement: %s" % (e, cursor.statement))
#         raise e
#
#     return APIResult(result=objTagRelation)