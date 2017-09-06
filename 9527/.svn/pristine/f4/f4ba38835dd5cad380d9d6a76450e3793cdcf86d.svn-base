# coding: utf-8
__author__ = 'Administrator'
from utils.logger import logger as log

import db.api.apiutils
import db.cores.mysqlconn
import utils.tool

@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def userMeetingCount_list(conn, cursor, page_index, page_size):
    """
    Meeting Count list by page
    """
    start_index = utils.tool.get_page_info(page_index=page_index, page_size=page_size)
    try:
        cursor.execute(
            """
            SELECT meeting_count.id, lps4_career.`name` AS career_name, mz_user.username AS username,meeting_count.count, meeting_count.max_count
            FROM mz_onevone_meeting_user_count AS meeting_count
            INNER JOIN mz_user_userprofile AS mz_user ON mz_user.id = meeting_count.user_id
            INNER JOIN mz_lps4_career AS lps4_career ON lps4_career.id = meeting_count.career_id
            ORDER BY meeting_count.id DESC
            LIMIT %s,%s
            """,(start_index, page_size,)
        )
        result = cursor.fetchall()

        cursor.execute(
            """
            SELECT COUNT(*) AS count FROM  mz_onevone_meeting_user_count;
            """
        )
        rows_count = cursor.fetchone()
        page_count = utils.tool.get_page_count(rows_count=rows_count['count'], page_size=page_size)
    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" %(e, cursor.statement)
        )
        raise e
    result_dict = {
        'rows_count':rows_count['count'],
        'page_count':page_count,
        'result':result
    }

    return db.api.apiutils.APIResult(result=result_dict)

@utils.tool.dec_timeit
@db.cores.mysqlconn.dec_make_conn_cursor
def userMeetingCount_search(conn, cursor, key_word, page_index, page_size):
    """
    get userMeetingCount by user_name
    """
    start_index = utils.tool.get_page_info(page_index=page_index, page_size=page_size)
    try:
        cursor.execute(
            """
            SELECT meeting_count.id, lps4_career.`name` AS career_name, mz_user.username AS username,meeting_count.count, meeting_count.max_count
            FROM mz_onevone_meeting_user_count AS meeting_count
            INNER JOIN mz_user_userprofile AS mz_user ON mz_user.id = meeting_count.user_id
            INNER JOIN mz_lps4_career AS lps4_career ON lps4_career.id = meeting_count.career_id
            WHERE mz_user.username LIKE %s
            ORDER BY meeting_count.id DESC
            LIMIT %s,%s
            """, ( key_word, start_index, page_size,)
        )
        result = cursor.fetchall()

        cursor.execute(
            """
            SELECT COUNT(*) AS count FROM mz_onevone_meeting_user_count AS meeting_count
            INNER JOIN mz_user_userprofile AS mz_user ON mz_user.id = meeting_count.user_id
            WHERE mz_user.username LIKE %s;
            """,(key_word,)
        )
        rows_count = cursor.fetchone()
        page_count = utils.tool.get_page_count(rows_count=rows_count['count'], page_size=page_size)

    except Exception as e:
        log.warn(

            "execute exception:%s."
            "statement:%s" %(e, cursor.statement)
        )
        raise e
    result_dict = {
        'rows_count':rows_count['count'],
        'page_count':page_count,
        'result':result
    }

    return db.api.apiutils.APIResult(result=result_dict)


@utils.tool.dec_timeit
@db.api.dec_make_conn_cursor
def userMeetingCount_detail(conn, cursor, _id):
    """
    get userMeetingCount detail by id
    """
    try:
        cursor.execute(
            """
            SELECT meeting_count.id, career.name, mz_user.username, meeting_count.count, meeting_count.max_count
            FROM mz_onevone_meeting_user_count AS meeting_count
            INNER JOIN mz_user_userprofile AS mz_user ON mz_user.id = meeting_count.user_id
            INNER JOIN mz_lps4_career AS career on career.id = meeting_count.career_id
            WHERE meeting_count.id = %s
            """,(_id,)
        )
        result = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" %(e, cursor.statement)
        )
        raise e
    return db.api.apiutils.APIResult(result=result)


@utils.tool.dec_timeit
@db.api.dec_make_conn_cursor
def userMeetingCount_update(conn, cursor, _id, count, max_count):
    """
    update userMeetingCount by id
    """
    try:
        cursor.execute(
            """
            UPDATE mz_onevone_meeting_user_count SET count=%s,max_count=%s WHERE id=%s;
            """,(count, max_count, _id)
        )
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception:%s."
            "statement:%s" %(e, cursor.statement)
        )
        raise e
    return db.api.apiutils.APIResult(result=True)