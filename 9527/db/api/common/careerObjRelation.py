# coding: utf-8
from utils.logger import logger as log
import db.cores.mysqlconn
import db.api.apiutils

import utils.tool


@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def career_obj_relation_course_list(conn, cursor, page_index, pagesize):
    """
    course list by page
    """
    start_index = utils.tool.get_page_info(page_index=page_index, page_size=pagesize)
    try:
        cursor.execute(
            """
            SELECT obj.id AS id,course.name AS obj_name,obj.obj_type AS type,career.name AS career_name,obj.is_actived AS is_actived
            FROM mz_common_careerobjrelation AS obj
            LEFT JOIN mz_course_course AS course
            ON course.id = obj.obj_id
            LEFT JOIN mz_course_careercourse AS career
            ON career.id = obj.career_id
            WHERE obj.obj_type = 'COURSE'
            ORDER BY obj.id DESC
            LIMIT %s,%s""", (start_index, pagesize,)
        )
        select_result = cursor.fetchall()

        cursor.execute(
            """
            SELECT COUNT(*) AS count FROM mz_common_careerobjrelation WHERE obj_type = 'COURSE'
            """
        )

        rows_count = cursor.fetchone()
        page_count = utils.tool.get_page_count(rows_count=rows_count['count'], page_size=pagesize)

    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" % (e, cursor.statement)
        )
        raise e

    result_dict = {
        'result': select_result,
        'rows_count': rows_count['count'],
        'page_count': page_count,
    }

    return db.api.apiutils.APIResult(result=result_dict)


@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def career_obj_relation_article_list(conn, cursor, page_index, pagesize):
    """
    article list by page
    """
    start_index = utils.tool.get_page_info(page_index=page_index, page_size=pagesize)
    try:
        cursor.execute(
            """
            SELECT obj.id AS id,article.title AS obj_name,obj.obj_type AS type,career.name AS career_name,obj.is_actived AS is_actived
            FROM mz_common_careerobjrelation AS obj
            LEFT JOIN mz_common_newarticle AS article
            ON article.id = obj.obj_id
            LEFT JOIN mz_course_careercourse AS career
            ON career.id = obj.career_id
            WHERE obj.obj_type = 'ARTICLE'
            ORDER BY obj.id DESC
            LIMIT %s,%s
            """,(start_index, pagesize)
        )
        select_result = cursor.fetchall()

        cursor.execute(
            """
            SELECT COUNT(*) AS count FROM mz_common_careerobjrelation WHERE obj_type = 'ARTICLE'
            """
        )
        rows_count = cursor.fetchone()
        page_count = utils.tool.get_page_count(rows_count=rows_count['count'], page_size=pagesize)

    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" %(e, cursor.statement)
        )
        raise e
    result_dict = {
        "rows_count":rows_count['count'],
        "page_count":page_count,
        "result":select_result,
    }
    return db.api.apiutils.APIResult(result=result_dict)

@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def careerobjrelation_detail(conn, cursor, id):
    """
    get detail by id
    """
    try:
        cursor.execute(
            """
            SELECT id, obj_id, obj_type, career_id, is_actived FROM  mz_common_careerobjrelation
            WHERE id = %s
            """,(id,)
        )
        result = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute Exception:%s."
            "statement %s" %(e, cursor.statement)
        )
        raise e
    return db.api.apiutils.APIResult(result=result)

@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def search_careerobjrelation_course(conn, cursor, course_name, page_index, page_size):
    """
    search by obj_name(course)
    """
    start_index = utils.tool.get_page_info(page_index=page_index, page_size=page_size)
    try:
        cursor.execute(
            """
            SELECT obj.id AS id,course.name AS obj_name,obj.obj_type AS type,career.name AS career_name,obj.is_actived AS is_actived
            FROM mz_common_careerobjrelation AS obj
            LEFT JOIN mz_course_course AS course
            ON course.id = obj.obj_id
            LEFT JOIN mz_course_careercourse AS career
            ON career.id = obj.career_id
            WHERE obj.obj_type = 'COURSE' AND course.name LIKE %s
            ORDER BY obj.id DESC
            LIMIT %s,%s
            """,(course_name, start_index, page_size,)
        )
        result = cursor.fetchall()

        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM mz_common_careerobjrelation AS obj
            LEFT JOIN mz_course_course AS course
            ON course.id = obj.obj_id
            WHERE obj.obj_type = 'COURSE' AND course.name LIKE %s
            ORDER BY obj.id DESC
            """,(course_name,)
        )
        rows_count = cursor.fetchone()
        page_count = utils.tool.get_page_count(rows_count=rows_count['count'], page_size=page_size)

    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" %(e, cursor.statement)
        )
        raise e
    result_dict = {
        'rows_count':rows_count['count'],
        'page_count':page_count,
        'result':result
    }
    return db.api.apiutils.APIResult(result=result_dict)



@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def search_careerobjrelation_article(conn, cursor, article_title, page_index, page_size):
    """
    search by obj_name(article)
    """
    start_index = utils.tool.get_page_info(page_index=page_index, page_size=page_size)
    try:
        cursor.execute(
            """
            SELECT obj.id AS id,article.title AS obj_name,obj.obj_type AS type,career.name AS career_name,obj.is_actived AS is_actived
            FROM mz_common_careerobjrelation AS obj
            LEFT JOIN mz_common_newarticle AS article
            ON article.id = obj.obj_id
            LEFT JOIN mz_course_careercourse AS career
            ON career.id = obj.career_id
            WHERE obj.obj_type = 'ARTICLE' AND article.title LIKE %s
            ORDER BY obj.id DESC
            LIMIT %s,%s
            """,(article_title, start_index, page_size,)
        )
        result = cursor.fetchall()

        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM mz_common_careerobjrelation AS obj
            LEFT JOIN mz_common_newarticle AS article
            ON article.id = obj.obj_id
            WHERE obj.obj_type = 'ARTICLE' AND article.title LIKE %s
            ORDER BY obj.id DESC
            """,(article_title,)
        )
        rows_count = cursor.fetchone()
        page_count = utils.tool.get_page_count(rows_count=rows_count['count'], page_size=page_size)

    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" %(e, cursor.statement)
        )
        raise e
    result_dict = {
        'rows_count':rows_count['count'],
        'page_count':page_count,
        'result':result,
    }
    return db.api.apiutils.APIResult(result=result_dict)


@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def delete_careerobjrelation(conn, cursor, id):
    """
    delete by id
    """
    try:
        cursor.execute(
            """
            DELETE FROM mz_common_careerobjrelation WHERE id = %s
            """, (id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" % (e, cursor.statement)
        )
        raise e

    return db.api.apiutils.APIResult(result=True)

@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def insert_careerobjrelation(conn, cursor, obj_id, obj_type, career_id, is_actived):
    """
    insert new careerObjRelation
    """
    try:
        cursor.execute(
            """
            INSERT INTO mz_common_careerobjrelation(obj_id, obj_type, career_id, is_actived)
            VALUE(%s,%s,%s,%s)
            """,(obj_id,obj_type,career_id,is_actived,)
        )
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" %(e, cursor.statement)
        )
        raise e

    return db.api.apiutils.APIResult(result=True)

@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def update_careerobjrelation(conn, cursor, id, is_actived):
    """
    update careerObjRelation by id
    """
    try:
        cursor.execute(
            """
            UPDATE mz_common_careerobjrelation SET is_actived = %s WHERE id = %s
            """,(is_actived, id,)
        )
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement %s" %(e, cursor.statement)
        )
        raise e

    return db.api.apiutils.APIResult(result=True)

@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def select_is_actived(conn, cursor, obj_id, obj_type):
    """
    修改某个careerobjrelation的对应关系的状态为激活之前，
    将所有其他的对应关系状态修改为未激活
    """
    try:
        cursor.execute(
            """
            SELECT career_id FROM mz_common_careerobjrelation WHERE obj_id = %s AND obj_type = %s AND is_actived = 1
            LIMIT 2
            """,(obj_id,obj_type,)
        )
        result = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" %(e, cursor.statement)
        )
        raise e

    return db.api.apiutils.APIResult(result=result)

@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def check_obj_id(conn, cursor, obj_id, obj_type):
    """
    check course by id
    """
    try:
        if obj_type == 'COURSE':
            cursor.execute(
                """
                SELECT id FROM mz_course_course WHERE id = %s
                """,(obj_id,))

        if obj_type == 'ARTICLE':
            cursor.execute(
                """
                SELECT id FROM mz_common_newarticle WHERE  id = %s
                """, (obj_id,)
            )
        result = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" %(e, cursor.statement)
        )
        raise e

    return db.api.apiutils.APIResult(result=result)


@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def check_exist(conn, cursor, obj_id, obj_type, career_id):
    """
    check exists by obj_id, obj_type, career_id
    """
    try:
        cursor.execute(
            """
            SELECT obj_id, obj_type, career_id FROM mz_common_careerobjrelation
            WHERE  obj_id = %s AND obj_type = %s AND career_id = %s
            """,(obj_id, obj_type, career_id,)
        )
        result = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" %(e, cursor.statement)
        )
        raise e

    return db.api.apiutils.APIResult(result=result)


@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def get_career_course(conn, cursor):
    """
    get career_course id, name
    """
    try:
        cursor.execute(
            """
            SELECT DISTINCT career.id,career.name FROM mz_course_careercourse career
            INNER JOIN mz_course_stage stage
            ON stage.career_course_id = career.id
            WHERE stage.lps_version = 3.0
            """
        )
        result = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" %(e, cursor.statement)
        )
        raise e

    return db.api.apiutils.APIResult(result=result)


@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def get_obj_id_list(conn, cursor, obj_type='COURSE'):
    """
    get course list
    """
    try:
        if obj_type == 'COURSE':
            cursor.execute(
                """
                SELECT id, name FROM  mz_course_course
                """
            )

        if obj_type == 'ARTICLE':
            cursor.execute(
                """
                SELECT id, title FROM mz_common_newarticle
                """
            )
        result = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" %(e, cursor.statement)
        )
        raise e

    return db.api.apiutils.APIResult(result=result)


