# coding: utf-8
__author__ = 'Administrator'
from utils.logger import logger as log

import db.api.apiutils
import db.cores.mysqlconn
import utils.tool


@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def career_teacher_list(conn, cursor):
    """
    get lps4_career_teacher list
    """
    try:
        cursor.execute(
            """
            SELECT teacher.id,lps4_career.`name`,mz_user.nick_name,teacher.qq,teacher.qq_key,teacher.qq_image_url
            FROM  mz_lps4_career_teacher AS teacher
            INNER JOIN mz_user_userprofile AS mz_user ON mz_user.id = teacher.teacher_id
            INNER JOIN mz_lps4_career AS lps4_career ON lps4_career.id = teacher.career_id
            """
        )
        result = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s." %(e, cursor.statement)
        )
        raise e
    return db.api.apiutils.APIResult(result=result)


@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def career_teacher_add(conn, cursor, career_id, teacher_id, qq, qq_key, qq_image_url):
    """
    insert career_teacher data
    """
    try:
        cursor.execute(
            """
            INSERT INTO mz_lps4_career_teacher(career_id,teacher_id,qq,qq_key,qq_image_url)
            VALUES(%s,%s,%s,%s,%s)
            """,(career_id,teacher_id,qq,qq_key,qq_image_url)
        )
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s." %(e, cursor.execute)
        )
        raise e
    return db.api.apiutils.APIResult(result=True)


@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def career_teacher_update(conn, cursor, _id, career_id, teacher_id, qq, qq_key, qq_image_url):
    """
    update carrer_teacher by id
    """
    try:
        cursor.execute(
            """
            UPDATE mz_lps4_career_teacher
            SET career_id=%s,teacher_id=%s,qq=%s,qq_key=%s,qq_image_url=%s
            WHERE id = %s
            """,(career_id,teacher_id,qq,qq_key,qq_image_url,_id,)
        )
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s." %(e, cursor.statement)
        )
        raise e
    return db.api.apiutils.APIResult(result=True)


@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def career_teacher_delete(conn, cursor, _id):
    """
    delete career_teacher by id
    """
    try:
        cursor.execute(
            """
            DELETE FROM mz_lps4_career_teacher WHERE id = %s
            """,(_id,)
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
def career_list(conn, cursor):
    """
    get lps4_career list
    """
    try:
        cursor.execute(
            """
            SELECT id, name FROM  mz_lps4_career;
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
def careerTeacherDetail(conn, cursor, _id):
    """
    get careerTeacherDetail by _id
    """
    try:
        cursor.execute(
            """
            SELECT id,career_id, teacher_id, qq, qq_key, qq_image_url
            FROM mz_lps4_career_teacher WHERE id = %s
            """,(_id,)
        )
        result = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s".format(e, cursor.statement)
        )
        raise e
    return db.api.apiutils.APIResult(result=result)
