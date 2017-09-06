# -*- coding: utf-8 -*-

import datetime
import calendar

effective_time = datetime.datetime.now().replace(year=2017, month=3, day=1, hour=0, minute=0, second=0)


def _calc_cycle_liveness(activate_date, now_date):
    """
    计算活跃度周期
    :param activate_date:
    :param now_date:
    :return:
    """
    def add_months(dt, months):
        month = dt.month - 1 + months
        year = dt.year + month / 12
        month = month % 12 + 1
        day = min(dt.day, calendar.monthrange(year, month)[1])
        return dt.replace(year=year, month=month, day=day)

    activate_date_day = min(activate_date.day, calendar.monthrange(now_date.year, now_date.month)[1])
    if now_date.day > activate_date.day:
        start_time = now_date.replace(day=activate_date_day)
        end_time = add_months(start_time, +1)
    else:
        end_time = now_date.replace(day=activate_date_day)
        start_time = add_months(end_time, -1)
    return start_time, end_time


def get_cycle_liveness(activate_date, now_date):
    """
    获取循环的活跃度周期
    :param activate_date:
    :param now_date:
    :return:
    """
    start_time, end_time = _calc_cycle_liveness(activate_date, now_date)
    #  设置活跃度生效日期
    if start_time < effective_time:
        start_time = effective_time
    return start_time, end_time


def get_cycle_start_time(activate_date, now_date):
    """
    获取循环的活跃度周期开始时间
    :param activate_date:
    :param now_date:
    :return:
    """
    start_time, end_time = _calc_cycle_liveness(activate_date, now_date)
    return start_time
