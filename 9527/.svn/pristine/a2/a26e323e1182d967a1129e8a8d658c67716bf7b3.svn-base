# -*- coding:utf-8 -*-
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def insert_liveness_record(conn, cursor, user_id, today_datetime, start_time, end_time, liveness):
    """
    插入每个周期的活跃度记录表
    :param conn:
    :param cursor:
    :param user_id:
    :param today_datetime:
    :param start_time:
    :param end_time:
    :param liveness:
    :return:
    """
    sql = """
      insert into mz_fxsys_liveness_record (user_id,date,liveness, start_time, end_time)
                VALUES (%s,%s,%s,%s,%s)  ON DUPLICATE KEY UPDATE liveness=%s, start_time=%s, end_time=%s
    """
    sql_user = """
         update mz_fxsys_user set liveness=0 WHERE id = %s
    """
    try:
        cursor.execute(sql, (user_id, today_datetime, liveness, start_time, end_time, liveness, start_time, end_time))
        cursor.execute(sql_user, (user_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def liveness_record_list(conn, cursor):
    """

    :param conn:
    :param cursor:
    :param user_id:
    :param today_datetime:
    :param liveness:
    :return:
    """
    sql = """
      select * from mz_fxsys_liveness_record where status=0
    """
    try:
        cursor.execute(sql,)
        liveness = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=liveness)


@dec_timeit
@dec_make_conn_cursor
def update_liveness_record(conn, cursor, profit, _id):
    """

    :param conn:
    :param cursor:
    :param profit:
    :param _id:
    :return:
    """
    sql_update_liveness = """
        update mz_fxsys_liveness_record set status=1,profit=%s where id=%s
    """
    try:
        cursor.execute(sql_update_liveness, (profit, _id))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def insert_liveness_info(conn, cursor, date, user_id, type, liveness, count, is_ceiling, start_time, end_time):
    """
    插入积分流水信息表
    :param conn:
    :param cursor:
    :param date:
    :param user_id:
    :param type: 1:视频 2:练习 3:任务 4:约课 5:辅导
    :param liveness:
    :param count:
    :param is_ceiling:
    :param start_time:
    :param end_time:
    :return:
    """
    sql = """
        select liveness,date,count from mz_fxsys_liveness_info
        where user_id= %s and type = %s and (DATE(date) BETWEEN %s AND %s)
        order by date Desc
        limit 1
    """

    in_sql = """
      insert into mz_fxsys_liveness_info (date,user_id, type, liveness, is_ceiling,plus,date_range,count,plus_count)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    try:
        cursor.execute(sql, (user_id, type, start_time, end_time))
        liveness_info = cursor.fetchone()
        if liveness_info:
            plus = liveness-liveness_info["liveness"]
            plus_count = count-liveness_info["count"]
            date_range = liveness_info["date"].strftime("%Y年%m月%d日%H:%M")+'-'+ date.strftime("%Y年%m月%d日%H:%M")
            if plus_count != 0:
                cursor.execute(in_sql, (date, user_id, type, liveness, is_ceiling, plus, date_range, count, plus_count))
        else:
            plus = liveness
            plus_count = count
            date_range = '新周期开始-' + date.strftime("%Y年%m月%d日%H:%M")
            cursor.execute(in_sql, (date, user_id, type, liveness, is_ceiling, plus, date_range, count, plus_count))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=True)
