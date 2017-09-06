# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor

@dec_timeit
@dec_make_conn_cursor
def list_public_meeting(conn, cursor):
    '''
    :param conn:
    :param cursor:
    :return: all  data in a list
    '''

    try:
        cursor.execute(
            """
            SELECT meeting.id, meeting.qq_group_1, meeting.qq_group_2, meeting.enter_qq, meeting.class_time, meeting.teacher_id, careercourse.name, teacher.name as teacher_name
            FROM mz_career_public_meeting as meeting
            LEFT JOIN mz_course_careercourse as careercourse ON meeting.id = careercourse.id
            LEFT JOIN mz_career_page_teacher as teacher ON meeting.teacher_id = teacher.teacher_id

            """, ()
        )
        public_meetings = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e

    return APIResult(result=public_meetings)


@dec_timeit
@dec_make_conn_cursor
def get_public_meeting_by_keyword(conn, cursor, keyword):
    '''
    根据关键字查询职业课程公开课
    :param conn:
    :param cursor:
    :param keyword:
    :return:
    '''
    try:
        cursor.execute(
            """
                SELECT meeting.id, meeting.qq_group_1, meeting.qq_group_2, meeting.enter_qq, meeting.class_time, meeting.teacher_id, careercourse.name, teacher.name as teacher_name
                FROM mz_career_public_meeting as meeting
                LEFT JOIN mz_course_careercourse as careercourse ON meeting.id = careercourse.id
                LEFT JOIN mz_career_page_teacher as teacher ON meeting.teacher_id = teacher.teacher_id
                WHERE careercourse.name LIKE %s or meeting.qq_group_1 LIKE %s or meeting.qq_group_2 LIKE %s or teacher.name LIKE %s

            """, (keyword, keyword, keyword, keyword,))
        public_meetings = cursor.fetchall()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=public_meetings)


@dec_timeit
@dec_make_conn_cursor
def update_public_meeting_by_id(conn, cursor,  class_time, enter_qq, _id):
    """
    更新公开课生效QQ和开课时间
    :param conn:
    :param cursor:
    :param _id:
    :return: result(),is_error()
    """
    try:
         cursor.execute(
            """
            UPDATE mz_career_public_meeting set class_time=%s,enter_qq=%s
            WHERE id=%s;
            """,(class_time, enter_qq, _id,))
         conn.commit()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=True)


@dec_timeit
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
            meeting.class_time,careercourse.name,teacher.teacher_id,teacher.name as teacher_name
            FROM mz_career_public_meeting as meeting
            LEFT JOIN mz_course_careercourse as careercourse
            ON meeting.id = careercourse.id
            LEFT JOIN mz_career_page_teacher as teacher ON meeting.teacher_id = teacher.teacher_id
            WHERE meeting.id=%s;
            """,(_id,))
         course = cursor.fetchall()
    except Exception as e:
         log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
         raise e
    return APIResult(result=course)

