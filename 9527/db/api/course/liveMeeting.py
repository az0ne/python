#!/usr/bin/env python
# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils import tool
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def list_live_meeting_by_page(conn, cursor, page_index, page_size):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT  live.id as live_id ,meeting.create_datetime,meeting.startline,meeting.finish_date,
                        meeting.content,class.coding,meeting.status,class.id as class_id,live.live_code
                FROM mz_lps3_liveroom  as live
                LEFT JOIN mz_lps3_classmeeting as meeting ON live.class_meeting_id=meeting.id
                LEFT JOIN mz_lps3_classmeetingrelation as relation ON relation.class_meeting_id=meeting.id
                LEFT JOIN mz_lps_class as class ON relation.class_id=class.id
                LEFT JOIN mz_lps3_classmeetingvideo as video ON live.live_id=video.live_id
                ORDER BY meeting.startline DESC
                limit %s,%s
            """, (start_index, page_size,))
        liveMeetings = cursor.fetchall()

        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_lps3_liveroom
            """)
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    liveMeeting_dict = {
        "result": liveMeetings,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=liveMeeting_dict)


@dec_timeit
@dec_make_conn_cursor
def list_live_meeting_by_keyword(conn, cursor, page_index, page_size, keyword):
    """
    """
    start_index = tool.get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
                SELECT  live.id as live_id ,meeting.create_datetime,meeting.startline,meeting.finish_date,
                        meeting.content,class.coding,meeting.status,class.id as class_id,live.live_code
                FROM mz_lps3_liveroom  as live
                LEFT JOIN mz_lps3_classmeeting as meeting ON live.class_meeting_id=meeting.id
                LEFT JOIN mz_lps3_classmeetingrelation as relation ON relation.class_meeting_id=meeting.id
                LEFT JOIN mz_lps_class as class ON relation.class_id=class.id
                WHERE live.live_code LIKE %s OR class.coding LIKE %s
                ORDER BY meeting.startline DESC
                limit %s,%s
            """, (keyword,keyword, start_index, page_size,))
        liveMeetings = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_lps3_liveroom  as live
                LEFT JOIN mz_lps3_classmeeting as meeting ON live.class_meeting_id=meeting.id
                LEFT JOIN mz_lps3_classmeetingrelation as relation ON relation.class_meeting_id=meeting.id
                LEFT JOIN mz_lps_class as class ON relation.class_id=class.id
                WHERE live.live_code LIKE %s OR class.coding LIKE %s
            """,(keyword,keyword))
        rows_count = cursor.fetchone()
        page_count = tool.get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    liveMeeting_dict = {
        "result": liveMeetings,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }

    return APIResult(result=liveMeeting_dict)


@dec_timeit
@dec_make_conn_cursor
def get_live_meeting_by_id(conn, cursor, id, class_id):
    """
    """
    try:
        cursor.execute(
            """
                SELECT  meeting.create_datetime,meeting.startline,meeting.finish_date,class.coding,
                        meeting.content,meeting.status,live.live_code,live.assistant_token,live.student_token,
                        live.teacher_token,live.student_client_token,live.student_join_url,live.teacher_join_url,
                        live.live_id
                FROM mz_lps3_liveroom  as live
                LEFT JOIN mz_lps3_classmeeting as meeting ON live.class_meeting_id=meeting.id
                LEFT JOIN mz_lps3_classmeetingrelation as relation ON relation.class_meeting_id=meeting.id
                LEFT JOIN mz_lps_class as class ON relation.class_id=class.id
                WHERE live.id=%s and class_id=%s
            """, (id, class_id))
        liveMeeting = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=liveMeeting)


@dec_timeit
@dec_make_conn_cursor
def get_video_by_live_id(conn, cursor, live_id):
    """
    """
    try:
        cursor.execute(
            """
                SELECT  token,`url`
                FROM mz_lps3_classmeetingvideo
                WHERE live_id=%s
            """, (live_id,))
        liveMeeting = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement:%s" % (e, cursor.statement))
        raise e

    return APIResult(result=liveMeeting)
