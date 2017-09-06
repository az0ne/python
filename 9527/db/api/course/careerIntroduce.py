# -*- coding: utf-8 -*-

from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor
from db.api.apiutils import APIResult
from utils import tool


@dec_timeit
@dec_make_conn_cursor
def insert_career_introduce(conn, cursor, _id, name, img_url, short_info, info, student_count, career_outline, reason):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                insert into mz_career_page (id,name,img_url,short_info,info,student_count,career_outline,reason)
                values (%s,%s,%s,%s,%s,%s,%s,%s);
            """, (_id, name, img_url, short_info, info, student_count, career_outline, reason))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_career_introduce_info(conn, cursor, _id, img_url, short_info, info, student_count, career_outline, reason):
    """
        returns: true/false
    """

    try:
        cursor.execute(
            """
                UPDATE mz_career_page set img_url=%s, short_info=%s,info=%s,student_count=%s,career_outline=%s,reason=%s WHERE id = %s;
            """, (img_url, short_info, info, student_count, career_outline, reason, _id))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_career_introduce_story(conn, cursor, _id, story_info, story_name, story_title, story_img_url,
                                  story_video_url):
    """
    :return: true/false
    """
    try:
        cursor.execute(
            """
                UPDATE mz_career_page set story_info=%s, story_name=%s, story_title=%s, story_img_url=%s, story_video_url=%s
                WHERE id = %s;
            """, (story_info, story_name, story_title, story_img_url, story_video_url, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_career_introduce_discuss(conn, cursor, _id, discuss_id1, discuss_id2, discuss_id3):
    """
    :return: true/false
    """
    try:
        cursor.execute(
            """
                UPDATE mz_career_page set discuss_id1=%s, discuss_id2=%s,discuss_id3=%s
                WHERE id = %s;
            """, (discuss_id1, discuss_id2, discuss_id3, _id,))
        conn.commit()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_career_introduce(conn, cursor, _id):
    """
    delete careerId related table field
    returns: true/false
    """

    try:
        cursor.execute(
            """
            DELETE cpt,cps,cpe,cpd,cp FROM mz_career_page AS cp
            LEFT JOIN mz_career_page_teacher AS cpt ON cp.id = cpt.career_id
            LEFT JOIN mz_career_page_student AS cps ON cp.id = cps.career_id
            LEFT JOIN mz_career_page_enterprise AS cpe ON cp.id = cpe.career_id
            LEFT JOIN mz_career_page_duty AS cpd ON cp.id = cpd.career_id
            WHERE cp.id = %s;
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
def list_career_introduce(conn, cursor):
    """
    """
    try:
        cursor.execute(
            """
                SELECT id,mz_career_page.name,img_url,short_info,info,student_count,story_info,story_name,
                story_title,story_img_url,story_video_url,career_outline,discuss_id1,discuss_id2,discuss_id3,reason
                FROM mz_career_page
                ORDER BY id DESC
            """)

        careerIntroduces = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerIntroduces)


@dec_timeit
@dec_make_conn_cursor
def list_career_introduce_name(conn, cursor):
    """
    get career name
    """

    try:
        cursor.execute(
            """
                SELECT id,name FROM mz_career_page
                ORDER BY id
            """)

        careerIntroduceNames = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerIntroduceNames)


@dec_timeit
@dec_make_conn_cursor
def get_career_introduce_by_id(conn, cursor, _id):
    """
    :param conn:
    :param cursor:
    :param _id:
    :return:
    """

    try:
        cursor.execute(
            """
                SELECT id,mz_career_page.name,img_url,short_info,info,student_count,story_info,story_name,
                story_title,story_img_url,story_video_url,career_outline,discuss_id1,discuss_id2,discuss_id3,reason
                FROM mz_career_page WHERE id = %s
            """, (_id,))

        careerIntroduces = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerIntroduces)


@dec_timeit
@dec_make_conn_cursor
def list_career_introduce_by_name(conn, cursor, name):
    """
    :param conn:
    :param cursor:
    :param name:
    :return:
    """
    try:
        cursor.execute(
            """
                SELECT id,mz_career_page.name,img_url,short_info,info,student_count,story_info,story_name,
                story_title,story_img_url,story_video_url,career_outline,discuss_id1,discuss_id2,discuss_id3,reason
                FROM mz_career_page WHERE name LIKE %s
                ORDER BY id DESC
            """, (name,))

        careerIntroduces = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerIntroduces)


@dec_timeit
@dec_make_conn_cursor
def select_career_introduce_by_career_id(conn, cursor, career_id):
    """
    :param conn:
    :param cursor:
    :param career_id:
    :return:
    """

    try:
        cursor.execute(
            """
            SELECT id,mz_career_page.name from mz_career_page WHERE id=%s
            """, (career_id,)
        )
        careerIntroduce = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=careerIntroduce)