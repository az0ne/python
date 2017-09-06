# -*- coding:utf-8 -*-
from django.conf import settings
from db.api import APIResult
from db.cores.mysqlconn import dec_make_conn_cursor
from utils.tool import dec_timeit, get_page_info, get_page_count
from utils.logger import logger as log


@dec_timeit
@dec_make_conn_cursor
def list_coach_info(conn, cursor, page_index, action='query', keyword=dict()):
    page_size = settings.PAGE_SIZE
    start_index = get_page_info(page_index, page_size)
    sql = """
               SELECT coach.id as coach_id, career.name as career_name,career.id as career_id, coach.source_type,coach.abstract,coach.create_date, coach.nick_name,
               coach.last_comment_date,coach.teacher_replay_count,coach.student_replay_count, student.nick_name as student_nick_name, teacher.nick_name as teacher_nick_name,
               student.real_name as student_real_name, teacher.real_name as teacher_real_name,
               coach.student_comment_count,coach.teacher_comment_count,coach.last_student_comment_date,coach.last_teacher_comment_date
               FROM mz_coach as coach
               LEFT JOIN mz_lps4_career as career
               ON coach.career_id=career.id
               LEFT JOIN mz_user_userprofile as teacher
               ON coach.teacher_id=teacher.id
               LEFT JOIN mz_user_userprofile as student
               ON coach.student_id=student.id
            """
    count_sql = """
                SELECT count(*)as count
                FROM mz_coach
                """

    if 'search' in action and keyword:
        search_sql = "   WHERE "
        where_list = list()
        if keyword.get('career_id'):
            where_list.append(" career.id=%s" % keyword.get('career_id'))
        if keyword.get('start_date') and keyword.get('end_date'):
            where_list.append(
                " DATE(create_date) BETWEEN '%s' AND '%s' " % (keyword.get('start_date'), keyword.get('end_date')))
        search_sql += ' and '.join(where_list)
        sql += search_sql
        count_sql = """
                SELECT count(*)as count
                FROM mz_coach as coach
                LEFT JOIN mz_lps4_career as career
                ON coach.career_id=career.id
            """
        count_sql += search_sql
    sql += """  ORDER BY coach.id DESC
                limit %s, %s"""
    try:
        cursor.execute(sql, (start_index, page_size))
        all_coach = cursor.fetchall()
        cursor.execute(count_sql)
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))

        raise e

    coach_dict = {
        "result": all_coach,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=coach_dict)


@dec_timeit
@dec_make_conn_cursor
def get_coach_status_by_id(conn, cursor, coach_id):
    sql = """
        SELECT id, done_status FROM mz_lps4_teacher_warning_backlog
        WHERE (`type`=11 or `type`=12 or `type`=13 or `type`=14) AND obj_id=%s
    """
    try:
        cursor.execute(sql, (coach_id,))
        status = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=status)


@dec_timeit
@dec_make_conn_cursor
def get_coach_info_by_id(conn, cursor, coach_id):
    sql = """
        SELECT coach.id as coach_id, career.name as career_name,career.id as career_id, coach.source_type,coach.abstract,coach.create_date, coach.nick_name,
               coach.last_comment_date,coach.teacher_replay_count,coach.student_replay_count, coach.last_student_comment_date,coach.last_teacher_comment_date,
               student.nick_name as student_nick_name, teacher.nick_name as teacher_nick_name,student.real_name as student_real_name, teacher.real_name as teacher_real_name,
               coach.student_comment_count,coach.teacher_comment_count, coach.source
               FROM mz_coach as coach
               LEFT JOIN mz_lps4_career as career
               ON coach.career_id=career.id
               LEFT JOIN mz_user_userprofile as teacher
               ON coach.teacher_id=teacher.id
               LEFT JOIN mz_user_userprofile as student
               ON coach.student_id=student.id
               WHERE coach.id = %s
    """
    try:
        cursor.execute(sql, (coach_id,))
        coach = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=coach)


@dec_timeit
@dec_make_conn_cursor
def get_all_coach_info(conn, cursor):
    sql = """
        SELECT coach.id as coach_id, career.name as career_name,career.id as career_id, coach.source_type,coach.abstract,coach.create_date, coach.nick_name,
               coach.last_comment_date,coach.teacher_replay_count,coach.student_replay_count,student.nick_name as student_nick_name, teacher.nick_name as teacher_nick_name,
               student.real_name as student_real_name, teacher.real_name as teacher_real_name,
               coach.student_comment_count,coach.teacher_comment_count,coach.last_student_comment_date,coach.last_teacher_comment_date
               FROM mz_coach as coach
               LEFT JOIN mz_lps4_career as career
               ON coach.career_id=career.id
               LEFT JOIN mz_user_userprofile as teacher
               ON coach.teacher_id=teacher.id
               LEFT JOIN mz_user_userprofile as student
               ON coach.student_id=student.id
    """
    try:
        cursor.execute(sql)
        coach_info = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=coach_info)
