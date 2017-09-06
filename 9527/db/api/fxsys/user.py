# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor


# 检测用户账号是否存在
@dec_timeit
@dec_make_conn_cursor
def is_exits_maizi_user(conn, cursor, name):
    try:
        cursor.execute(
            """
            SELECT id FROM mz_user_userprofile WHERE  email = %s OR mobile = %s;
            """, (name, name))
        datacount = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=datacount)


# 获取所有绑定了奖学金系统的用户
@dec_timeit
@dec_make_conn_cursor
def get_fxsys_users(conn, cursor):
    try:
        cursor.execute(
            """
            SELECT ls.user_id,ls.career_id,us.activate_date, us.id,us.register_date,us.is_suspend,us.is_graduate
            FROM mz_fxsys_user  as us
            INNER JOIN  mz_lps4_student as ls ON us.maiziedu_id=ls.user_id and ls.type in (0,1) 
            """)
        user_info = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=user_info)


@dec_timeit
@dec_make_conn_cursor
def get_fxsys_user_by_id(conn, cursor, user_id):
    """
    根据获取绑定了奖学金系统的用户
    :param conn:
    :param cursor:
    :param user_id:
    :return:
    """
    try:
        cursor.execute(
            """
            SELECT ls.user_id,ls.career_id,us.activate_date, us.id,us.register_date FROM mz_fxsys_user  as us
            INNER JOIN  mz_lps4_student as ls ON us.maiziedu_id=ls.user_id  and ls.type in (0,1)
            WHERE us.id=%s
            """, (user_id,))
        user_info = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=user_info)


@dec_timeit
@dec_make_conn_cursor
def get_students_video_count(conn, cursor, class_id, user_id, start_time, end_time):
    """
    获取学生观看视频数量
    :param conn:
    :param cursor:
    :param class_id:
    :param user_id:
    :param start_time:
    :param end_time:
    :return:
    """
    try:
        cursor.execute(
            """
              SELECT COUNT(*) AS num FROM mz_lps3_userknowledgeitemrecord as kr
              INNER JOIN mz_lps3_knowledgeitem AS k ON kr.knowledge_item_id = k.id AND k.obj_type='LESSON'
              WHERE kr.class_id=%s AND kr.student_id=%s AND kr.status='DONE' AND (DATE(kr.done_time) BETWEEN %s AND %s)
            """, (class_id, user_id, start_time, end_time,))
        rows_count = cursor.fetchone()["num"]
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=rows_count)


@dec_timeit
@dec_make_conn_cursor
def get_students_test_count(conn, cursor, class_id, user_id, start_time, end_time):
    """
    获取学生练习次数(测试，小项目制作)
    :param conn:
    :param cursor:
    :param class_id:
    :param user_id:
    :param start_time:
    :param end_time:
    :return:
    """
    try:
        cursor.execute(
            """
              SELECT COUNT(*) AS num FROM mz_lps3_userknowledgeitemrecord as kr
              INNER JOIN mz_lps3_knowledgeitem AS k ON kr.knowledge_item_id = k.id AND k.obj_type='TEST'
              WHERE kr.class_id=%s AND kr.student_id=%s AND kr.status='DONE' AND (DATE(kr.done_time) BETWEEN %s AND %s)
            """, (class_id, user_id, start_time, end_time,))

        test_count = cursor.fetchone()["num"]
        cursor.execute(
            """
            SELECT count(*) AS num FROM mz_coach as coach
            WHERE coach.source_type=30 AND coach.source_location REGEXP '"item_id": 0,'
            AND coach.student_id=%s AND (DATE(coach.create_date) BETWEEN %s AND %s)
            """, (user_id, start_time, end_time,))

        project_count = cursor.fetchone()["num"]
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=test_count+project_count)


@dec_timeit
@dec_make_conn_cursor
def get_students_task_count(conn, cursor, user_id, start_time, end_time):
    """
    获取学生任务完成数量
    :param conn:
    :param cursor:
    :param user_id:
    :param start_time:
    :param end_time:
    :return:
    """
    try:
        cursor.execute(
            """
              SELECT COUNT(*) AS num FROM mz_lps3_usertaskrecord
              WHERE status='PASS' AND student_id=%s AND (DATE(correct_time) BETWEEN %s AND %s)
            """, (user_id, start_time, end_time,))
        rows_count = cursor.fetchone()["num"]

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=rows_count)


@dec_timeit
@dec_make_conn_cursor
def get_students_meeting_count(conn, cursor, user_id, start_time, end_time):
    """
    获取学生约课完成数量
    :param conn:
    :param cursor:
    :param user_id:
    :param start_time:
    :param end_time:
    :return:
    """
    try:
        cursor.execute(
            """
              SELECT COUNT(*) AS num
              FROM mz_lps4_teacher_warning_backlog
              WHERE `type`=5 AND is_done=1 AND user_id=%s AND (DATE(done_date) BETWEEN %s AND %s)
            """, (user_id, start_time, end_time,))

        rows_count = cursor.fetchone()["num"]
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=rows_count)


@dec_timeit
@dec_make_conn_cursor
def get_student_coach_count(conn, cursor, user_id, start_time, end_time):
    """
    学生主动发起的辅导
    :param conn:
    :param cursor:
    :param user_id:
    :param start_time:
    :param end_time:
    :return:
    """
    try:
        cursor.execute(
            """
            SELECT coalesce(sum(student_comment_count),0) AS num FROM mz_coach as coach
            WHERE coach.source_type in (10,11) AND coach.student_id=%s AND (DATE(coach.create_date) BETWEEN %s AND %s)
            """, (user_id, start_time, end_time,))

        project_count = cursor.fetchone()["num"]
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e
    return APIResult(result=project_count)


@dec_timeit
@dec_make_conn_cursor
def update_user_liveness(conn, cursor, _id, liveness, liveness_update_date):
    """
    更新活跃度
    :param conn:
    :param cursor:
    :param _id:
    :param liveness:
    :param liveness_update_date:
    :return:
    """
    try:
        cursor.execute(
            """
              update mz_fxsys_user set liveness=%s,liveness_update_date=%s WHERE id = %s
            """,
            (liveness, liveness_update_date, _id)
        )
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=True)
