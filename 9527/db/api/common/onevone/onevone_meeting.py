# -*- coding: utf-8 -*-

from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def list_onevone_meeting(conn, cursor, page_index, page_size):
    start_index = get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT meeting.id,meeting.career_id,meeting.teacher_id,meeting.start_time,meeting.end_time,
                        meeting.teacher_url,meeting.student_url,meeting.video_url,
                        meeting.teacher_token,meeting.assistant_token,meeting.student_client_token,meeting.student_web_token,
                        meeting.live_code,meeting.live_id,meeting.user_id,meeting.phone,meeting.question,meeting.create_date_time,
                        meeting.status,career.name as career_name,teacher.nick_name,meeting.video_token
                FROM mz_onevone_meeting as meeting
                LEFT JOIN mz_lps4_career as career
                ON meeting.career_id=career.id
                LEFT JOIN mz_user_userprofile as teacher
                ON meeting.teacher_id = teacher.id
                ORDER BY meeting.id DESC
                limit %s,%s

            """, (start_index, page_size,))
        meetings = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_onevone_meeting
            """)
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    task_dict = {
        "result": meetings,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=task_dict)


@dec_timeit
@dec_make_conn_cursor
def list_onevone_meeting_on_search(conn, cursor, page_index, page_size, data):
    start_index = get_page_info(page_index, page_size)
    sql = """
                SELECT meeting.id,meeting.career_id,meeting.teacher_id,meeting.start_time,meeting.end_time,
                        meeting.teacher_url,meeting.student_url,meeting.video_url,
                        meeting.teacher_token,meeting.assistant_token,meeting.student_client_token,meeting.student_web_token,
                        meeting.live_code,meeting.live_id,meeting.user_id,meeting.phone,meeting.question,meeting.create_date_time,
                        meeting.status,career.name as career_name,teacher.nick_name,meeting.video_token
                FROM mz_onevone_meeting as meeting
                LEFT JOIN mz_lps4_career as career
                ON meeting.career_id=career.id
                LEFT JOIN mz_user_userprofile as teacher
                ON meeting.teacher_id = teacher .id
                WHERE {where}
                ORDER BY meeting.id DESC
                limit %s,%s

            """
    where = "TRUE "
    for key in data:
        if data[key]:
            if ('status' not in key) and isinstance(data[key], basestring):
                value = "%"+data[key]+"%"
                if "nick_name" in key:
                    where += " AND teacher.%s LIKE '%s'" % (key, value)
                else:
                    where += " AND meeting.%s LIKE '%s'" % (key, value)
            else:
                where += " AND meeting.%s='%s'" % (key, data[key])
    sql = sql.format(where=where)

    try:
        cursor.execute(sql, (start_index, page_size,))
        meetings = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_onevone_meeting as meeting
                LEFT JOIN mz_lps4_career as career
                ON meeting.career_id=career.id
                LEFT JOIN mz_user_userprofile as teacher
                ON meeting.teacher_id = teacher .id
                WHERE %s
            """ % where)
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    task_dict = {
        "result": meetings,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=task_dict)


@dec_timeit
@dec_make_conn_cursor
def get_onevone_meeting_by_id(conn, cursor, _id):
    try:
        cursor.execute(
            """
               SELECT  meeting.id,meeting.career_id,meeting.teacher_id,meeting.start_time,meeting.end_time,
                        meeting.teacher_url,meeting.student_url,meeting.video_url,
                        meeting.teacher_token,meeting.assistant_token,meeting.student_client_token,meeting.student_web_token,
                        meeting.live_code,meeting.live_id,meeting.user_id,meeting.phone,meeting.question,meeting.create_date_time,
                        meeting.status,career.name as career_name,teacher.nick_name,meeting.video_token
               FROM mz_onevone_meeting as meeting
               LEFT JOIN mz_lps4_career as career
               ON meeting.career_id=career.id
               LEFT JOIN mz_user_userprofile as teacher
               ON meeting.teacher_id = teacher.id
               WHERE meeting.id=%s
               ORDER BY meeting.id DESC


           """, (_id,)
        )
        meeting = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=meeting)


@dec_timeit
@dec_make_conn_cursor
def delect_onevone_meeting_by_id(conn, cursor, _id):
    try:
        cursor.execute(
            """
              DELETE FROM mz_onevone_meeting WHERE id=%s
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
def update_onevone_meeting_by_id(conn, cursor, data):
    try:
        cursor.execute(
            """
              UPDATE mz_onevone_meeting SET video_url=%s,start_time=%s,end_time=%s,video_token=%s
              WHERE id=%s
            """, (data['video_url'],  data['start_time'], data['end_time'], data['video_token'], data['id'],))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_onevone_status_by_id(conn, cursor, status, _id):
    try:
        cursor.execute(
            """
              UPDATE mz_onevone_meeting SET status=%s
              WHERE id=%s
            """, (status, _id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)



