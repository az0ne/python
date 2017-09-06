#! /usr/bin/evn python
# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit, get_page_info, get_page_count
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def get_all_teacher_backlog(conn, cursor, page_index, page_size):
    start_index = get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
               SELECT backlog.id, user_name,warn_one_date, warn_two_date, warn_three_date, is_done,backlog.`type`,
               create_date, done_date, teacher_id, content,warning.title as type_name,user_profile.real_name as teacher_real_name,
               user_profile.nick_name as teacher_nick_name,career.name as career_name,backlog.done_status,
               CASE backlog.is_done
               WHEN '0' THEN '未处理'
               WHEN '1' THEN '已处理'
               WHEN '2' THEN '已取消'
               END as is_done_name
               FROM mz_lps4_teacher_warning_backlog as backlog
               LEFT JOIN mz_lps4_teacher_warning as warning
               ON backlog.type=warning.type
               LEFT JOIN mz_user_userprofile as user_profile
               ON backlog.teacher_id=user_profile.id
               LEFT JOIN mz_lps4_career as career
               ON career.id=backlog.career_id
               ORDER BY is_done ASC, warn_two_date ASC
               limit %s, %s;
            """, (start_index, page_size))
        backlog = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_lps4_teacher_warning_backlog
            """)
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    backlog_dict = {
        "result": backlog,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=backlog_dict)


@dec_timeit
@dec_make_conn_cursor
def get_all_teacher_backlog_by_search(conn, cursor, page_index, page_size, dict_keyword):
    start_index = get_page_info(page_index, page_size)
    keyword = dict_keyword.get('keyword', None)
    is_done = dict_keyword.get('is_done', None)
    done_status = dict_keyword.get('done_status', None)
    career_id = dict_keyword.get('career_id', None)
    start_date = dict_keyword.get('start_date')
    end_date = dict_keyword.get('end_date')
    is_done_sql = "" if is_done is None else " AND backlog.is_done={0}".format(is_done)
    if is_done: #当代办已经还没有处理时不查询状态
        done_status_sql = "" if done_status is None else " AND backlog.done_status={0}".format(done_status)
    else:
        done_status_sql = ""

    if is_done == 0 and done_status is not None: #当悬在未处理不分页，外面数据分页
        limit_str = ""
    else:
        limit_str = "limit %s, %s;"
    career_sql = "" if career_id is None else " AND career_id={0}".format(career_id)
    date_sql = " AND DATE(create_date) BETWEEN '{0}' AND '{1}'".format(start_date, end_date) if (
    start_date and end_date) else ""
    if is_done:
        order = ' done_date DESC'
    else:
        order = ' warn_two_date ASC'
    sql = """
               SELECT backlog.id, user_name,warn_one_date, warn_two_date, warn_three_date, is_done,backlog.`type`,
               create_date, done_date, teacher_id, content,warning.title as type_name,career.id as career_id,
               user_profile.nick_name as teacher_nick_name,user_profile.real_name as teacher_real_name,career.name as career_name,backlog.done_status,
               CASE backlog.is_done
               WHEN '0' THEN '未处理'
               WHEN '1' THEN '已处理'
               WHEN '2' THEN '已取消'
               END as is_done_name
               FROM mz_lps4_teacher_warning_backlog as backlog
               LEFT JOIN mz_lps4_teacher_warning as warning
               ON backlog.type=warning.type
               LEFT JOIN mz_user_userprofile as user_profile
               ON backlog.teacher_id=user_profile.id
               LEFT JOIN mz_lps4_career as career
               ON career.id=backlog.career_id
               WHERE (user_profile.nick_name LIKE %s or user_profile.real_name LIKE %s or backlog.user_name LIKE %s or warning.title LIKE %s or backlog.type=%s) {0}{1}{2}{3}
               ORDER BY is_done ASC, {4}
               {5}
            """.format(is_done_sql, done_status_sql, career_sql, date_sql, order, limit_str)
    try:
        if limit_str == '':
            cursor.execute(sql, (keyword, keyword, keyword, keyword, keyword,))
        else:
            cursor.execute(sql, (keyword, keyword, keyword, keyword, keyword, start_index, page_size,))

        backlog = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_lps4_teacher_warning_backlog as backlog
                LEFT JOIN mz_lps4_teacher_warning as warning
                ON backlog.type=warning.type
                LEFT JOIN mz_user_userprofile as user_profile
                ON backlog.teacher_id=user_profile.id
                WHERE (user_profile.nick_name LIKE %s or user_profile.real_name LIKE %s or backlog.user_name LIKE %s or warning.title LIKE %s or backlog.type=%s) {0}{1}{2}{3}
            """.format(is_done_sql, done_status_sql, career_sql, date_sql),
            (keyword, keyword, keyword, keyword, keyword,))
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    backlog_dict = {
        "result": backlog,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=backlog_dict)


@dec_timeit
@dec_make_conn_cursor
def get_backlog_by_id(conn, cursor, _id):
    try:
        cursor.execute(
            """
               SELECT backlog.id, user_name,warn_one_date, warn_two_date, warn_three_date, is_done, backlog.`type`,
               create_date, done_date, teacher_id, content,warning.title as type_name,
               user_profile.nick_name as teacher_name,career.name as career_name,backlog.done_status,
               CASE backlog.is_done
               WHEN '0' THEN '未完成'
               WHEN '1' THEN '已完成'
               WHEN '2' THEN '已取消'
               END as is_done_name
               FROM mz_lps4_teacher_warning_backlog as backlog
               LEFT JOIN mz_lps4_teacher_warning as warning
               ON backlog.type=warning.type
               LEFT JOIN mz_user_userprofile as user_profile
               ON backlog.teacher_id=user_profile.id
               LEFT JOIN mz_lps4_career as career
               ON career.id=backlog.career_id
               WHERE backlog.id=%s
            """, (_id,))
        backlog = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=backlog)


@dec_timeit
@dec_make_conn_cursor
def get_teacher_backlog_by_coach(conn, cursor, page_index, page_size, coach_id):
    start_index = get_page_info(page_index, page_size)
    try:
        cursor.execute(
            """
               SELECT backlog.id, user_name,warn_one_date, warn_two_date, warn_three_date, is_done,backlog.`type`, backlog.obj_id,
               create_date, done_date, teacher_id, content,warning.title as type_name,user_profile.real_name as teacher_real_name,
               user_profile.nick_name as teacher_nick_name,career.name as career_name,backlog.done_status,
               CASE backlog.is_done
               WHEN '0' THEN '未处理'
               WHEN '1' THEN '已处理'
               WHEN '2' THEN '已取消'
               END as is_done_name
               FROM mz_lps4_teacher_warning_backlog as backlog
               LEFT JOIN mz_lps4_teacher_warning as warning
               ON backlog.type=warning.type
               LEFT JOIN mz_user_userprofile as user_profile
               ON backlog.teacher_id=user_profile.id
               LEFT JOIN mz_lps4_career as career
               ON career.id=backlog.career_id
               WHERE backlog.obj_id=%s AND (backlog.`type`=11 or backlog.`type`=12
               or backlog.`type`=13 or backlog.`type`=14)
               ORDER BY create_date ASC
               limit %s, %s;
            """, (coach_id, start_index, page_size))
        backlog = cursor.fetchall()
        cursor.execute(
            """
                SELECT count(*) as count
                FROM mz_lps4_teacher_warning_backlog
                WHERE obj_id=%s AND (`type`=11 or `type`=12 or `type`=13 or `type`=14)
            """, (coach_id,))
        rows_count = cursor.fetchone()
        page_count = get_page_count(rows_count["count"], page_size)

    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    backlog_dict = {
        "result": backlog,
        "rows_count": rows_count["count"],
        "page_count": page_count,
    }
    return APIResult(result=backlog_dict)


@dec_timeit
@dec_make_conn_cursor
def get_teacher_backlog_by_date(conn, cursor, date):
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    try:
        cursor.execute(
            """
               SELECT backlog.id, user_name,warn_one_date, warn_two_date, warn_three_date, is_done,backlog.`type`,
               create_date, done_date, teacher_id, content,warning.title as type_name,user_profile.real_name as teacher_real_name,
               user_profile.nick_name as teacher_nick_name,career.name as career_name,backlog.done_status,
               CASE backlog.is_done
               WHEN '0' THEN '未处理'
               WHEN '1' THEN '已处理'
               WHEN '2' THEN '已取消'
               END as is_done_name
               FROM mz_lps4_teacher_warning_backlog as backlog
               LEFT JOIN mz_lps4_teacher_warning as warning
               ON backlog.type=warning.type
               LEFT JOIN mz_user_userprofile as user_profile
               ON backlog.teacher_id=user_profile.id
               LEFT JOIN mz_lps4_career as career
               ON career.id=backlog.career_id
               WHERE YEAR(create_date)=%s AND MONTH(create_date)=%s
               ORDER BY create_date DESC
            """, (year, month))
        backlog = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    backlog_dict = {
        "result": backlog,
    }
    return APIResult(result=backlog_dict)


@dec_timeit
@dec_make_conn_cursor
def insert_backlog_opt_log(conn, cursor, user_id, user_name, content, backlog_id):
    """
        returns: true/false
    """
    try:
        cursor.execute(
            """
                insert into mz_back_teacher_backlog_opt (user_id, user_name, content, backlog_id)
                 values (%s,%s,%s,%s)
            """, (user_id, user_name, content, backlog_id))

        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e

    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def get_backlog_opt_log(conn, cursor, backlog_id):
    try:
        cursor.execute(
            """
            SELECT * FROM mz_back_teacher_backlog_opt where backlog_id=%s
            """, (backlog_id,))
        backlog = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=backlog)
