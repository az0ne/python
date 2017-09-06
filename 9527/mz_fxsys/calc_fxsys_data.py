#! /usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import db.api.fxsys.user
import db.api.fxsys.payments
import db.api.fxsys.liveness_record
import db.api.fxsys.static_rebate
import db.api.fxsys.new_asset
from mz_lps4.interface import NORMAL_CLASS_DICT
from mz_fxsys.tool import get_cycle_liveness, effective_time
from utils.logger import logger as log
from mz_fxsys.constant_pool import FROZEN_LIVENESS
import os


def update_all_liveness(today_datetime=None, is_settlement=False):
    """
    更新所有活跃度
    :param today_datetime: 活跃度的计算日期
    :param is_settlement: 是否结算
    :return:
    """
    if not today_datetime:
        today_datetime = datetime.datetime.now()
    user = db.api.fxsys.user.get_fxsys_users()
    if user.is_error():
        log.warn("get_fxsys_users is error today_datetime:{0}".format(today_datetime))
    for user_info in user.result():
        if user_info["activate_date"] and user_info["is_suspend"] == 0 and user_info["is_graduate"] == 0:
            update_liveness_by_userinfo(user_info, is_settlement, today_datetime)
    log.info("update_all_liveness is success today_datetime:{0}".format(today_datetime))


def update_liveness_by_userinfo(user_info, is_settlement=False, today_datetime=None, prompt_settlement=False):
    """
    更新指定用户的周期
    :param user_info: 用户对象
    :param today_datetime: 活跃度的计算日期
    :param is_settlement: 是否结算
    :param prompt_settlement: 是否立即结算(不管周期是否到达)
    :return:
    """
    if not today_datetime:
        today_datetime = datetime.datetime.now()
    try:
        activate_date = user_info["activate_date"]
        register_date = user_info["register_date"]
        # 当前活跃度时间周期
        start_time, end_time = get_cycle_liveness(activate_date, today_datetime)
        start_time = start_time + datetime.timedelta(days=1)
        start_time = start_time.strftime("%Y-%m-%d")
        end_time = end_time.strftime("%Y-%m-%d")
        career_id = user_info['career_id']
        # 班级 Id
        class_id = NORMAL_CLASS_DICT[career_id]
        user_id = user_info['user_id']
        # 学生学习的视频数量
        video_count_result = db.api.fxsys.user.get_students_video_count(class_id, user_id, start_time, end_time)
        if video_count_result.is_error():
            log.warn("get_students_video_count is error user_id:{0}".format(user_id))
        video_count = video_count_result.result()

        test_count_result = db.api.fxsys.user.get_students_test_count(class_id, user_id, start_time, end_time)
        if test_count_result.is_error():
            log.warn("get_students_test_count is error user_id:{0}".format(user_id))
        test_count = test_count_result.result()

        task_count_result = db.api.fxsys.user.get_students_task_count(user_id, start_time, end_time)
        if task_count_result.is_error():
            log.warn("get_students_task_count is error user_id:{0}".format(user_id))
        task_count = task_count_result.result()

        meeting_count_result = db.api.fxsys.user.get_students_meeting_count(user_id, start_time, end_time)
        if meeting_count_result.is_error():
            log.warn("get_students_meeting_count is error user_id:{0}".format(user_id))
        meeting_count = meeting_count_result.result()

        coach_count_result = db.api.fxsys.user.get_student_coach_count(user_id, start_time, end_time)
        if coach_count_result.is_error():
            log.warn("get_student_coach_count is error user_id:{0}".format(user_id))
        coach_count = coach_count_result.result()

        video_mark = video_count * 0.5 if video_count * 0.5 < 10 else 10
        test_mark = test_count * 3 if test_count * 3 < 3 else 3
        task_mark = task_count * 5 if task_count * 5 < 20 else 20
        meeting_mark = meeting_count * 8 if meeting_count * 8 < 8 else 8
        coach_mark = int(coach_count * 3) if coach_count * 3 < 24 else 24
        # 插入视频数据
        db.api.fxsys.liveness_record.insert_liveness_info(today_datetime, user_info["id"], 1, video_mark,
                                                          video_count, 1 if video_mark == 10 else 0, start_time,
                                                          end_time)
        # 插入作业数据
        db.api.fxsys.liveness_record.insert_liveness_info(today_datetime, user_info["id"], 2, test_mark,
                                                          test_count, 1 if test_mark == 3 else 0, start_time, end_time)
        # 插入任务数据
        db.api.fxsys.liveness_record.insert_liveness_info(today_datetime, user_info["id"], 3, task_mark,
                                                          task_count, 1 if task_mark == 20 else 0, start_time, end_time)
        # 插入约课数据
        db.api.fxsys.liveness_record.insert_liveness_info(today_datetime, user_info["id"], 4, meeting_mark,
                                                          meeting_count, 1 if meeting_mark == 8 else 0, start_time,
                                                          end_time)
        # 插入辅导数据
        db.api.fxsys.liveness_record.insert_liveness_info(today_datetime, user_info["id"], 5, coach_mark,
                                                          coach_count, 1 if coach_mark == 24 else 0, start_time,
                                                          end_time)

        liveness = video_mark + test_mark + task_mark + meeting_mark + coach_mark
        result = db.api.fxsys.user.update_user_liveness(user_info["id"], liveness, today_datetime)
        if not result.is_error():
            log.info("update_liveness is success user_id:{0} today_datetime:{1}".format(user_id, today_datetime))
        if is_settlement and today_datetime.date() != activate_date.date() and \
                        today_datetime.day == activate_date.day and register_date > effective_time:
            liveness_datetime = today_datetime.replace(hour=23, minute=40, second=0)
            result = db.api.fxsys.liveness_record.insert_liveness_record(user_info["id"], liveness_datetime,
                                                                         start_time, end_time, liveness)
            if not result.is_error():
                log.info("insert_liveness_record is success fssys_user_id:{0} today_datetime:{1}".format(
                    user_info["id"], today_datetime))
        elif prompt_settlement:  # 立即结算
            result = db.api.fxsys.liveness_record.insert_liveness_record(user_info["id"], today_datetime,
                                                                         start_time, end_time, liveness)
            if not result.is_error():
                log.info("insert_liveness_record is success fssys_user_id:{0} today_datetime:{1}".format(
                    user_info["id"], today_datetime))
    except Exception, e:
        log.warn("update_liveness_by_userinfo is except exception:{0} fssys_user_id:{1}".format(str(e),
                                                                                                user_info["id"]))


def calc_frozen_rebate():
    """
    计算冻结
    :return:
    """
    result = db.api.fxsys.liveness_record.liveness_record_list()
    if result.is_error():
        log.warn("liveness_record_list is error today_datetime:{0}".format(datetime.datetime.now()))
    for liveness_record in result.result():
        try:
            user_id = liveness_record["user_id"]
            liveness = liveness_record["liveness"]
            today_datetime = liveness_record["date"]
            liveness_id = liveness_record["id"]
            start_time = liveness_record["start_time"]
            end_time = liveness_record["end_time"]
            start_time = start_time.strftime("%Y-%m-%d")
            end_time = end_time.strftime("%Y-%m-%d")
            # 查询需要冻结的静态返利
            static_rebate_result = db.api.fxsys.payments.select_static_rebate_in_cycle(user_id,
                                                                                       start_time, end_time)
            if static_rebate_result.is_error():
                log.warn("select_static_rebate_in_cycle is error user_id:{0}".format(user_id))
                break
            static_rebate = static_rebate_result.result()
            if static_rebate and liveness < FROZEN_LIVENESS:
                static_rebate = '-' + str(static_rebate)
                result = db.api.fxsys.payments.insert_frozen_rebate(liveness_id, user_id, static_rebate,
                                                                    today_datetime)
                if not result.is_error():
                    log.info("insert_frozen_rebate is success user_id:{0} static_rebate:{1}".format(user_id,
                                                                                                    static_rebate))
            else:
                result = db.api.fxsys.liveness_record.update_liveness_record(static_rebate, liveness_id)
                if not result.is_error():
                    log.info("update_liveness_record is success id:{0} static_rebate:{1}".format(liveness_id,
                                                                                                 static_rebate))
        except Exception, e:
            log.warn("calc_frozen_rebate is except exception:{0} user_id:{1}".format(str(e), user_id))
    log.info("calc_frozen_rebate is success today_datetime:{0}".format(datetime.datetime.now()))


def all_user_static_rebate(today_datetime=None):
    """
    所有用户的静态返利计算
    :param today_datetime:
    :return:
    """
    if not today_datetime:
        today_datetime = datetime.datetime.now()
    result = db.api.fxsys.static_rebate.update_static_rebate(today_datetime)
    if result.is_error():
        log.warn("all_user_static_rebate is error today_datetime:{0}".format(today_datetime))
    log.info("all_user_static_rebate is success today_datetime:{0}".format(today_datetime))


def check_all_profit():
    """
    检查所有的数据收益
    :return:
    """
    result = db.api.fxsys.new_asset.check_all_profit()
    if result.is_error():
        log.warn("check_all_profit is error ")
    log.info("check_all_profit is success")


def for_quantitation_cash():
    user_info_list = db.api.fxsys.payments.get_quantitation_cash_back_day()
    if user_info_list.is_error():
        log.warn(u"获取定量返现用户的数据出错")
    else:
        for user_info in user_info_list.result():
            user_id = user_info["id"]
            order_id = ''
            money = user_info["cash_back_day"]
            payments_type = u'1'
            origin = u'每日定量返现'
            date = datetime.datetime.now()
            insert_payments = db.api.fxsys.payments.add_payments(user_id, order_id, money, payments_type, origin, date)
    return insert_payments
