# -*- coding:utf-8 -*-

import datetime
import calendar
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult, dec_make_conn_cursor
from utils import tool

USER_TYPE = {'1': '会员', '2': '合作伙伴'}
USER_ROLE = {'0': '', '1': '银勋', '2': '金勋', '3': '王牌', '4': '荣誉'}
PAYMENTS_TYPE = {'1': '扶助奖学金', '2': '推广佣金', '3': '感恩奖', '4': '领导奖', '5': '提现', '6': '消费',
                 '7': '返利提现', '8': '推广提现', '9':'冻结'}


def cycle_liveness(activate_date, now_date):
    """
    循环的活跃度周期
    :param activate_date:
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


@dec_timeit("user_login")
@dec_make_conn_cursor
def validate_login(conn, cursor, uname, pwd):
    """用户登录验证"""
    try:
        cursor.execute("select count(*) as validate_result from mz_fxSys_user where username=%s and password=%s",
                       (uname, pwd))
        user = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=user)


@dec_timeit("does the username exsit?")
@dec_make_conn_cursor
def get_user_info_by_username(conn, cursor, username):
    """查询用户信息"""
    try:
        cursor.execute(
            """
                select id,username,full_name,type_id,role_id,password,register_date,activate_date,last_login,liveness,
                is_suspend, is_graduate, liveness_update_date
                from mz_fxSys_user where username = %s
            """, (username,))
        user_info = cursor.fetchone()
        user_info['type_name'] = USER_TYPE[str(user_info.get('type_id', 0))]
        user_info['role_name'] = USER_ROLE[str(user_info.get('role_id', 0))]
    except Exception as e:
        log.warn(
            "cursor exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=user_info)


@dec_timeit("update_last_login_time")
@dec_make_conn_cursor
def update_last_login_time_by_userId(conn, cursor, uid):
    try:
        cursor.execute('update mz_fxSys_user set last_login = %s where id= %s',
                       (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), uid))
        conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=True)


# ----------------------------------------------- user table end ----------------------------------------------------- #


# --------------------------------------------- payments table start ------------------------------------------------- #

@dec_timeit("get_payments_by_user_id_and_page")
@dec_make_conn_cursor
def get_payments_by_user_id_and_page(conn, cursor, user_id, start_date, end_date, page_index=1, page_size=10):
    """根据用户id分页查询收支情况表"""
    base_sql = "select {fields} from mz_fxsys_payments WHERE 1=1"
    condition = " AND user_id={0}".format(user_id)
    pagination_sql = base_sql.format(fields="*")
    count_sql = base_sql.format(fields="count(id) as counts")
    if start_date != '':
        condition += " AND date >='{0}'".format(start_date)
    if end_date != '':
        end_date += " 23:59:59"
        condition += " AND date <='{0}'".format(end_date)
    order_by = " ORDER BY id DESC"
    limit = " LIMIT {0},{1}".format((int(page_index) - 1) * page_size, page_size)
    if condition != "":
        pagination_sql += condition
        count_sql += condition
    pagination_sql += order_by
    pagination_sql += limit
    try:
        cursor.execute(pagination_sql)
        payments = cursor.fetchall()

        cursor.execute(count_sql)
        rows_counts = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    for payment in payments:
        if payment['payments_type']:
            payment['payments_name'] = PAYMENTS_TYPE[str(payment['payments_type'])]
        else:
            payment['payments_name'] = ''

    data = {
        "payments": payments,
        "rows_counts": rows_counts['counts'],
        "page_counts": tool.get_page_count(rows_counts['counts'], page_size)
    }

    return APIResult(result=data)

# --------------------------------------------- payments table end --------------------------------------------------- #
# if __name__ == '__main__':
#     insert_order(order_id=11111)
