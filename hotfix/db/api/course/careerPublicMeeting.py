# -*- coding:utf-8 -*-
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_get_cache, dec_make_conn_cursor

@dec_timeit('get_public_meeting_by_id')
@dec_make_conn_cursor
def get_public_meeting_by_id(conn, cursor, _id):
    """

    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
         cursor.execute(
            """
            SELECT meeting.id, meeting.qq_group_1,meeting.qq_image_1,meeting.qq_group_key_1,
            meeting.qq_group_2,meeting.qq_image_2,meeting.qq_group_key_2, meeting.enter_qq,
            meeting.class_time,meeting.teacher_id,meeting.free_task_id,careercourse.name
            FROM mz_career_public_meeting as meeting
            LEFT JOIN mz_course_careercourse as careercourse
            ON meeting.id = careercourse.id
            WHERE meeting.id=%s;
            """,(_id,))
         meeting = cursor.fetchone()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=meeting)


@dec_timeit('get_public_meeting_task_info_by_task_id')
@dec_make_conn_cursor
def get_public_meeting_task_info_by_task_id(conn, cursor, _id):
    """

    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
         cursor.execute(
            """
            SELECT free_task.title,free_task.img1,free_task.img2,free_task.img3,task.desc
            FROM mz_free_task_desc as free_task
            LEFT JOIN mz_lps3_task as task
            ON free_task.task_id = task.id
            WHERE free_task.id=%s;
            """,(_id,))
         meeting = cursor.fetchone()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=meeting)


@dec_timeit('insert_public_meeting_data')
@dec_make_conn_cursor
def insert_public_meeting_data(conn, cursor, data):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                insert into mz_career_public_meeting_date (career_id,mobile,enter_date,class_time,qq_group) values (%s,%s,%s,%s,%s);
            """, (data["career_id"], data["mobile"],data["enter_date"], data["class_time"], data["qq_group"],))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit('get_my_public_meeting_data')
@dec_make_conn_cursor
def get_my_public_meeting_data(conn, cursor, mobile, career_id, class_time):
    """
    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
         cursor.execute(
            """
            SELECT id
            FROM mz_career_public_meeting_date
            WHERE career_id=%s AND mobile=%s AND class_time > date(%s);
            """,(career_id,mobile,class_time))
         data = cursor.fetchone()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=data)


@dec_timeit('get_meeting_mobiles')
@dec_make_conn_cursor
def get_meeting_data_by_course(conn, cursor, career_id):
    """
    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
        cursor.execute(
            """
            SELECT id,mobile,qq_group
            FROM mz_career_public_meeting_date
            WHERE career_id=%s AND class_time > date(now()) AND class_time<date_add(date(now()), interval 1 day)
            """, (career_id))
        data = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=data)


@dec_timeit('get_not_started_meeting')
@dec_make_conn_cursor
def get_not_started_meeting(conn, cursor):
    """
    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
        cursor.execute(
            """
            SELECT id,class_time,free_task_id
            FROM mz_career_public_meeting
            WHERE class_time >now()
            """, ())
        data = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=data)
