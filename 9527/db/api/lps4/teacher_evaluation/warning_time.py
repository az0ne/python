# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def get_all_warning_time(conn, cursor, ):
    try:
        cursor.execute(
            """
               SELECT id, `type`,warn_one_hour, warn_two_hour, warn_three_hour, title
               FROM mz_lps4_teacher_warning
            """, )
        warn_time = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=warn_time)


@dec_timeit
@dec_make_conn_cursor
def get_warning_time_by_id(conn, cursor, _id):
    try:
        cursor.execute(
            """
               SELECT id, `type`,warn_one_hour, warn_two_hour, warn_three_hour, title
               FROM mz_lps4_teacher_warning
               WHERE id=%s
            """, (_id,))
        warn_time = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=warn_time)


@dec_timeit
@dec_make_conn_cursor
def insert_warning_time(conn, cursor, warning_dict):
    try:
        cursor.execute(
            """
               INSERT INTO mz_lps4_teacher_warning (title, `type`, warn_one_hour,warn_two_hour,warn_three_hour)
               VALUES (%s,%s,%s,%s,%s)
            """, (warning_dict['title'], warning_dict['type'], warning_dict['warn_one_hour'],
                  warning_dict['warn_two_hour'], warning_dict['warn_three_hour'],))

        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def update_warn_time(conn, cursor, warn_dict):
    """
    update the table both mz_lps4_teacher_warning and mz_lps4_teacher_backkog
    :param conn:
    :param cursor:
    :param warningTime_id: the id of mz_lps4_teacher_warning
    :param warningTimeDict: info of changed warning time.
    :return:
    """
    try:
        sql_warning = " update mz_lps4_teacher_warning  SET `title`=%s, warn_one_hour=%s, warn_two_hour=%s, " \
                      "warn_three_hour=%s WHERE id=%s"
        cursor.execute(sql_warning, (warn_dict["title"], warn_dict['warn_one_hour'], warn_dict['warn_two_hour'],
                                     warn_dict['warn_three_hour'], warn_dict['id']))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def delete_warning_time_by_id(conn, cursor, warning_id):
    try:
        cursor.execute(
            """
               DELETE FROM mz_lps4_teacher_warning WHERE id=%s
            """, (warning_id,))

        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)
