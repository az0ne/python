# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def list_lps4_student(conn, cursor, page_index, page_size, keyword):
    """
    显示lps4 学生信息
    :param conn:
    :param cursor:
    :param page_index:
    :param page_size:
    :param keyword:
    :return:
    """
    start_index = get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
              SELECT s.user_id, s.start_time, s.career_id, cc.name AS career_name, s.teacher_id, teacher.real_name AS teacher_real,
              teacher.nick_name AS teacher_nick, student.real_name AS student_real, student.nick_name AS student_nick, s.`type` as student_type,
              CASE s.`type`
              WHEN '0' THEN '非就业'
              WHEN '1' THEN '就业'
              END as student_type_name
              FROM mz_lps4_student AS s
              INNER JOIN mz_course_careercourse as cc on cc.id=s.career_id
              INNER JOIN mz_user_userprofile AS teacher ON teacher.id=s.teacher_id
              INNER JOIN mz_user_userprofile AS student ON student.id=s.user_id
              WHERE type!=2 AND (cc.name LIKE %s OR student.real_name LIKE %s OR student.nick_name LIKE %s OR
              teacher.nick_name LIKE %s OR teacher.real_name LIKE %s) ORDER BY career_id
              limit %s,%s
            """, (keyword, keyword, keyword, keyword, keyword, start_index, page_size,))
        students = cursor.fetchall()

        cursor.execute(
            """
              SELECT count(*) as count
              FROM mz_lps4_student AS s
              INNER JOIN mz_course_careercourse as cc on cc.id=s.career_id
              INNER JOIN mz_user_userprofile AS teacher ON teacher.id=s.teacher_id
              INNER JOIN mz_user_userprofile AS student ON student.id=s.user_id
              WHERE type!=2 AND (cc.name LIKE %s OR student.real_name LIKE %s OR student.nick_name LIKE %s OR
              teacher.nick_name LIKE %s OR teacher.real_name LIKE %s)
            """, (keyword, keyword, keyword, keyword, keyword,))
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    students_dict = {
        "result": students,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=students_dict)


@dec_timeit
@dec_make_conn_cursor
def export_lps4_student_info(conn, cursor, keyword):
    """
    根据关键字筛选学生信息
    :param conn:
    :param cursor:
    :param keyword:
    :return:
    """
    try:
        cursor.execute(
            """
              SELECT s.user_id, s.start_time, s.career_id, cc.name AS career_name, s.teacher_id, teacher.real_name AS teacher_real,
              teacher.nick_name AS teacher_nick, student.real_name AS student_real, student.nick_name AS student_nick, s.`type` as student_type,
              CASE s.`type`
              WHEN '0' THEN '非就业'
              WHEN '1' THEN '就业'
              END as student_type_name
              FROM mz_lps4_student AS s
              INNER JOIN mz_course_careercourse as cc on cc.id=s.career_id
              INNER JOIN mz_user_userprofile AS teacher ON teacher.id=s.teacher_id
              INNER JOIN mz_user_userprofile AS student ON student.id=s.user_id
              WHERE s.`type`!=2 AND (cc.name LIKE %s OR student.real_name LIKE %s OR student.nick_name LIKE %s OR
              teacher.nick_name LIKE %s OR teacher.real_name LIKE %s) ORDER BY career_id
            """, (keyword, keyword, keyword, keyword, keyword,))
        students = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    students_dict = {
        "result": students,
    }
    return APIResult(result=students_dict)


@dec_timeit
@dec_make_conn_cursor
def get_lps_students_meeting_count(conn, cursor, info):
    """
    获取学生约课完成数量
    :param conn:
    :param cursor:
    :param info:
    :return:
    """
    try:
        cursor.execute(
            """
              SELECT COUNT(*) AS num
              FROM mz_lps4_teacher_warning_backlog
              WHERE `type`=5 AND is_done=1 AND user_id=%s AND (DATE(done_date) BETWEEN %s AND %s)
            """, (info.get('user_id'), info.get('start_time'), info.get('end_time'),))

        rows_count = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    students_dict = {
        "result": rows_count,
    }
    return APIResult(result=students_dict)


@dec_timeit
@dec_make_conn_cursor
def get_lps_students_video_count(conn, cursor, info):
    """
    获取学生观看视频数量
    """
    try:
        cursor.execute(
            """
              SELECT COUNT(*) AS num FROM mz_lps3_userknowledgeitemrecord as kr
              INNER JOIN mz_lps3_knowledgeitem AS k ON kr.knowledge_item_id = k.id AND k.obj_type='LESSON'
              WHERE kr.class_id=%s AND kr.student_id=%s AND kr.status='DONE' AND (DATE(kr.done_time) BETWEEN %s AND %s)
            """, (info.get('class_id'), info.get('user_id'), info.get('start_time'), info.get('end_time'),))
        rows_count = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    students_dict = {
        "result": rows_count,
    }
    return APIResult(result=students_dict)


@dec_timeit
@dec_make_conn_cursor
def get_lps_students_task_count(conn, cursor, info):
    """
    获取学生任务完成数量
    """
    try:
        cursor.execute(
            """
              SELECT COUNT(*) AS num FROM mz_lps3_usertaskrecord
              WHERE status='PASS' AND student_id=%s AND (DATE(done_time) BETWEEN %s AND %s)
            """, (info.get('user_id'), info.get('start_time'), info.get('end_time'),))
        rows_count = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    students_dict = {
        "result": rows_count,
    }
    return APIResult(result=students_dict)


@dec_timeit
@dec_make_conn_cursor
def get_teacher_coach_count(conn, cursor, info):
    """
    获取教师主动发起辅导数量
    """
    try:
        cursor.execute(
            """
              SELECT COUNT(*) AS num FROM mz_coach
              WHERE source_type=20 AND student_id=%s AND (DATE(create_date) BETWEEN %s AND %s)
            """, (info.get('user_id'), info.get('start_time'), info.get('end_time'),))
        rows_count = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    students_dict = {
        "result": rows_count,
    }
    return APIResult(result=students_dict)


@dec_timeit
@dec_make_conn_cursor
def get_teacher_coach_reply_count(conn, cursor, info):
    """
    获取教师主动发起辅导教师回复数
    """
    try:
        cursor.execute(
            """
              SELECT COUNT(*) AS num FROM mz_coach_comment as comment
              INNER JOIN mz_coach as coach
              ON comment.coach_id=coach.id
              WHERE coach.source_type=20 AND comment.user_type=20 AND coach.student_id=%s AND (DATE(comment.create_date) BETWEEN %s AND %s)
            """, (info.get('user_id'), info.get('start_time'), info.get('end_time'),))
        rows_count = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    students_dict = {
        "result": rows_count,
    }
    return APIResult(result=students_dict)


@dec_timeit
@dec_make_conn_cursor
def get_student_coach_reply_count(conn, cursor, info):
    """
    学生问答，学生主动发起的辅导
    """
    try:
        cursor.execute(
            """
              SELECT COUNT(*) AS num FROM mz_coach_comment as comment
              INNER JOIN mz_coach as coach
              ON comment.coach_id=coach.id
              WHERE coach.source_type=10 AND comment.user_type=20 AND coach.student_id=%s AND (DATE(comment.create_date) BETWEEN %s AND %s)
            """, (info.get('user_id'), info.get('start_time'), info.get('end_time'),))
        rows_count = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    students_dict = {
        "result": rows_count,
    }
    return APIResult(result=students_dict)


@dec_timeit
@dec_make_conn_cursor
def get_teacher_project_coach_reply_count(conn, cursor, info):
    """
    作业上传，老师回复数量
    """
    try:
        cursor.execute(
            """
              SELECT COUNT(*) AS num FROM mz_coach_comment as comment
              INNER JOIN mz_coach as coach
              ON comment.coach_id=coach.id
              WHERE coach.source_type=30 AND (coach.source_location NOT REGEXP '"item_id": 0,') AND comment.user_type=20
              AND coach.student_id=%s  AND (DATE(comment.create_date) BETWEEN %s AND %s)
            """, (info.get('user_id'), info.get('start_time'), info.get('end_time'),))
        rows_count = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    students_dict = {
        "result": rows_count,
    }
    return APIResult(result=students_dict)
