# -*- coding:utf-8 -*-

from collections import OrderedDict
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_make_conn_cursor


@dec_timeit("get_new_asset_by_user_id")
@dec_make_conn_cursor
def get_new_asset_by_user_id(conn, cursor, user_id):
    """
    根据用户ID获取新的支产信息表
    :param conn:
    :param cursor:
    :param user_id:
    :return:
    """
    asset_sql = "select * from mz_fxsys_new_asset WHERE user_id = %s"
    try:
        cursor.execute(asset_sql, (user_id,))
        asset = cursor.fetchone()

    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statment: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=asset)


@dec_timeit("get_rebate_no_by_user_id")
@dec_make_conn_cursor
def get_rebate_no_by_user_id(conn, cursor, user_id):
    """
    获取用户的返利数值
    :param conn:
    :param cursor:
    :param user_id:
    :return:
    """
    sql = """
        select rt.rebate_no FROM mz_fxsys_user as user
        left join mz_fxsys_rebatetype as rt on rt.id=user.rebate_type_id
        where user.id= %s
    """
    try:
        cursor.execute(sql, (user_id,))
        rebate_no = cursor.fetchone()["rebate_no"]
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statment: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=rebate_no)


@dec_timeit("is_notify_liveness_record_by_user_id")
@dec_make_conn_cursor
def is_notify_liveness_record_by_user_id(conn, cursor, user_id):
    """
    根据用户ID获取已经结算判断活跃度结果是否通知
    :param conn:
    :param cursor:
    :param user_id:
    :return:
    """
    sql = """
      select * from mz_fxsys_liveness_record where status!=0 and user_id=%s AND is_notify=0
      ORDER by date DESC limit 1
    """
    try:
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=result)


@dec_timeit("update_is_notify")
@dec_make_conn_cursor
def update_is_notify(conn, cursor, user_id):
    """
    更新活跃度，通知
    :param conn:
    :param cursor:
    :param user_id:
    :return:
    """
    sql = """
      update mz_fxsys_liveness_record
      set is_notify=1
      where user_id=%s
    """
    try:
        cursor.execute(sql, (user_id,))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=True)


@dec_timeit("get_liveness_info_dict")
@dec_make_conn_cursor
def get_liveness_info_dict(conn, cursor, user_id, last_id=None):
    """
    获取学分获得流水信息
    :param conn:
    :param cursor:
    :param user_id:
    :param last_id:
    :return:
    """
    try:
        if last_id:
            sql = """
                    SELECT * FROM mz_fxsys_liveness_info
                    where user_id=%s and id < %s and plus_count > 0
                    order by date Desc,type DESC
                    limit 10
                """
            cursor.execute(sql, (user_id, last_id))
        else:
            sql = """
                    SELECT * FROM mz_fxsys_liveness_info
                    where user_id=%s and plus_count > 0
                    order by date Desc,type DESC
                    limit 10
                """
            cursor.execute(sql, (user_id,))
        liveness_info_list = cursor.fetchall()
        liveness_info_dict = OrderedDict()
        last_id = 0
        is_page = 0
        for liveness_info in liveness_info_list:
            liveness_info_dict.setdefault(liveness_info["date_range"], [])
            if liveness_info_dict.has_key(liveness_info["date_range"]):
                liveness_info_dict.get(liveness_info["date_range"]).append(liveness_info)
        if liveness_info_list:
            last_id = liveness_info_list[-1]["id"]
            if len(liveness_info_list) == 10:
                is_page = 1
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=dict(liveness_info_dict=liveness_info_dict, last_id=last_id, is_page=is_page))


@dec_timeit("get_liveness_infos")
@dec_make_conn_cursor
def get_liveness_infos(conn, cursor, user_id, start_time, end_time):
    """
    获取当前周期任务完成情况
    :param conn:
    :param cursor:
    :param user_id:
    :param page_index:
    :return:
    """
    sql = """
        select liveness,date,count from mz_fxsys_liveness_info
        where user_id= %s and type = %s and (DATE(date) BETWEEN %s AND %s)
        order by date Desc
        limit 1
    """
    try:
        liveness_infos = {}
        # 视频
        cursor.execute(sql, (user_id, 1, start_time, end_time))
        video_info = cursor.fetchone()
        if video_info:
            liveness_infos[1] = [video_info["count"], video_info["liveness"], 20,
                                 video_info["count"]/20.0*100 if video_info["count"]/20 < 1 else 100]
        else:
            liveness_infos[1] = [0, 0, 20, 0]
        # 练习
        cursor.execute(sql, (user_id, 2, start_time, end_time))
        test_info = cursor.fetchone()
        if test_info:
            liveness_infos[2] = [test_info["count"], test_info["liveness"], 1,
                                 test_info["count"]/1.0*100 if test_info["count"]/1 < 1 else 100]
        else:
            liveness_infos[2] = [0, 0, 1, 0]
        # 任务
        cursor.execute(sql, (user_id, 3, start_time, end_time))
        task_info = cursor.fetchone()
        if task_info:
            liveness_infos[3] = [task_info["count"], task_info["liveness"], 4,
                                 task_info["count"]/4.0*100 if task_info["count"]/4 < 1 else 100]
        else:
            liveness_infos[3] = [0, 0, 4, 0]
        # 约课
        cursor.execute(sql, (user_id, 4, start_time, end_time))
        meeting_info = cursor.fetchone()
        if meeting_info:
            liveness_infos[4] = [meeting_info["count"], meeting_info["liveness"], 1,
                                 meeting_info["count"]/1.0*100 if meeting_info["count"]/1 < 1 else 100]
        else:
            liveness_infos[4] = [0, 0, 1, 0]
        # 辅导
        cursor.execute(sql, (user_id, 5, start_time, end_time))
        coach_info = cursor.fetchone()
        if coach_info:
            liveness_infos[5] = [coach_info["count"], coach_info["liveness"], 8,
                                 coach_info["count"]/8.0*100 if coach_info["count"]/8 < 1 else 100]
        else:
            liveness_infos[5] = [0, 0, 8, 0]
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=liveness_infos)

