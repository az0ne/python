# -*- coding:utf-8 -*-
from django.conf import settings

from db.api import APIResult
from db.cores.mysqlconn import dec_make_conn_cursor
from utils.tool import dec_timeit, get_page_info, get_page_count
from utils.logger import logger as log


@dec_timeit
@dec_make_conn_cursor
def get_task_by_career_id(conn, cursor, career_id):
    try:
        cursor.execute(
            """
               SELECT task.id as task_id,task.name as task_name,stage.name as stage_name
               FROM mz_lps3_task as task
               LEFT JOIN mz_lps3_stagetaskrelation as relation
               ON task.id=relation.task_id
               LEFT JOIN mz_course_stage as stage
               ON relation.stage_id=stage.id
               LEFT JOIN mz_lps4_career as career
               ON stage.career_course_id=career.id
               WHERE career.id=%s
            """, (career_id,))
        tasks = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=tasks)


@dec_timeit
@dec_make_conn_cursor
def list_coach_task_lib(conn, cursor, page_index):
    page_size = settings.PAGE_SIZE
    start_index = get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
               SELECT coach.id as coach_id, task.name as task_name, career.name as career_name,coach.content,
               teacher.nick_name, teacher.real_name
               FROM mz_coach_task_lib as coach
               LEFT JOIN mz_lps3_task as task
               ON coach.task_id=task.id
               LEFT JOIN mz_lps4_career as career
               ON coach.career_id=career.id
               LEFT JOIN mz_user_userprofile as teacher
               ON coach.teacher_id=teacher.id
               ORDER BY coach.career_id, coach.task_id
               limit %s, %s;
            """, (start_index, page_size))
        tasks = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*)as count
                FROM mz_coach_task_lib
            """)
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    tasks_dict = {
        "result": tasks,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=tasks_dict)


@dec_timeit
@dec_make_conn_cursor
def list_coach_task_lib_by_search(conn, cursor, page_index, keyword):
    page_size = settings.PAGE_SIZE
    start_index = get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
               SELECT coach.id as coach_id, task.name as task_name, career.name as career_name,coach.content,
               teacher.nick_name, teacher.real_name
               FROM mz_coach_task_lib as coach
               LEFT JOIN mz_lps3_task as task
               ON coach.task_id=task.id
               LEFT JOIN mz_lps4_career as career
               ON coach.career_id=career.id
               LEFT JOIN mz_user_userprofile as teacher
               ON coach.teacher_id=teacher.id
               WHERE career.name LIKE %s
               ORDER BY coach.career_id, coach.task_id
               limit %s, %s;
            """, (keyword, start_index, page_size))
        tasks = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*)as count
                FROM mz_coach_task_lib as coach
                LEFT JOIN mz_lps4_career as career
                ON coach.career_id=career.id
                WHERE career.name LIKE %s
            """, (keyword,))
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    tasks_dict = {
        "result": tasks,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=tasks_dict)


@dec_timeit
@dec_make_conn_cursor
def get_coach_task_lib_by_id(conn, cursor, _id):
    sql = """
           SELECT id,career_id,task_id,content,teacher_id
           FROM mz_coach_task_lib
           WHERE id=%s
        """
    try:
        cursor.execute(sql, (_id,))
        task = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=task)


@dec_timeit
@dec_make_conn_cursor
def get_teacher_by_career(conn, cursor, career_id):
    sql = """
               SELECT teacher.id as teacher_id, teacher.nick_name, teacher.real_name
               FROM mz_lps4_career as career
               RIGHT JOIN mz_lps4_teacher_team as team
               ON team.career_id=career.id
               RIGHT JOIN mz_user_userprofile as teacher
               ON team.teacher_id=teacher.id
               WHERE career.id=%s
            """
    try:
        cursor.execute(sql, (career_id,))
        teacher = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=teacher)


@dec_timeit
@dec_make_conn_cursor
def insert_task_lib(conn, cursor, coach_dict):
    sql = """
               INSERT INTO mz_coach_task_lib (career_id,task_id,teacher_id,content)
               VALUES (%s,%s,%s,%s)
            """
    try:
        cursor.execute(sql, (
        coach_dict['career_id'], coach_dict['task_id'], coach_dict['teacher_id'], coach_dict['content']))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_task_lib_content(conn, cursor, _id, content):
    sql = """
               UPDATE mz_coach_task_lib SET content=%s
               WHERE id=%s
            """
    try:
        cursor.execute(sql, (content, _id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def check_content_by_task_id(conn, cursor, task_id, career_id):
    sql = """
                SELECT count(*)as count
                FROM mz_coach_task_lib
                WHERE task_id=%s and career_id=%s
            """
    try:
        cursor.execute(sql, (task_id, career_id,))
        rows_count = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=rows_count)


@dec_timeit
@dec_make_conn_cursor
def delete_coach_task_by_id(conn, cursor, _id):
    sql = """
                DELETE FROM mz_coach_task_lib
                WHERE id=%s
            """
    try:
        cursor.execute(sql, (_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)