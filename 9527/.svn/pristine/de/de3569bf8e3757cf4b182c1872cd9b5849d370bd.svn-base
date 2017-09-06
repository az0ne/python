# -*- coding:utf-8 -*-
import decimal
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def select_static_rebate_in_cycle(conn, cursor, user_id, start_time, end_time):
    """
    查询活跃周期类的静态返利
    :param conn:
    :param cursor:
    :param user_id:
    :param start_time:
    :param end_time:
    :return:
    """
    sql_total_rebate = """
        select coalesce(SUM(money),0) as static_rebate
        from mz_fxsys_payments
        WHERE user_id = %s and payments_type = 1 and DATE(date) BETWEEN %s AND %s
        """
    try:
        cursor.execute(sql_total_rebate, (user_id, start_time, end_time))
        static_rebate = cursor.fetchone()["static_rebate"]
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=static_rebate)


@dec_timeit
@dec_make_conn_cursor
def insert_frozen_rebate(conn, cursor, liveness_id, user_id, frozen_rebate, today_datetime):
    """
    插入活跃周期类冻结的静态返利
    :param conn:
    :param cursor:
    :param user_id:
    :param frozen_rebate:
    :param today_datetime:
    :return:
    """
    sql_balances = """
        select COALESCE(sum(money),0) as balances
        from mz_fxsys_payments WHERE user_id = %s
    """
    sql_insert_payments = """
      insert into mz_fxsys_payments (user_id,order_id,payments_type,origin,money,total_money,`date`)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    sql_new_asset = """
        update mz_fxsys_new_asset
        set current_rebate = current_rebate-%s,frozen_rebate=frozen_rebate+%s
        WHERE user_id=%s
    """
    sql_update_liveness = """
        update mz_fxsys_liveness_record set status=2,profit=%s where id=%s
    """
    try:
        # 计算总余额并且插入收支表
        cursor.execute(sql_balances, (user_id,))
        balances_result = cursor.fetchone()
        if balances_result:
            balances = float(frozen_rebate) + float(balances_result["balances"])
            cursor.execute(sql_insert_payments,
                           (user_id, 0, '9', '冻结当月奖学金', frozen_rebate, balances, today_datetime))
            frozen_rebate = abs(decimal.Decimal(frozen_rebate))
            cursor.execute(sql_new_asset, (frozen_rebate, frozen_rebate, user_id))
            cursor.execute(sql_update_liveness, (frozen_rebate, liveness_id))
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
def add_payments(conn, cursor, user_id, order_id, money, payments_type, origin, date):
    """
    新插入一条收支明细
    :param conn:
    :param cursor:
    :param user_id:
    :param order_id:
    :param money:
    :param payments_type:
    :param origin:
    :param date:
    :return:
    """

    sql_balances = """
        select COALESCE(sum(money),0) as balances
        from mz_fxsys_payments WHERE user_id = %s
    """
    try:
        # 计算总余额并且插入收支表
        cursor.execute(sql_balances, (user_id,))
        balances_result = cursor.fetchone()
        if balances_result:
            if payments_type in (7, 8, 9):
                money = '-' + money
            balances = float(money) + float(balances_result["balances"])
            cursor.execute(
                "insert into mz_fxsys_payments (user_id,order_id,money,payments_type,origin,total_money,date) "
                "VALUES (%s,%s,%s,%s,%s,%s,%s)", (user_id, order_id, money, payments_type, origin, balances,
                                                  date))
            if payments_type == 1:
                sql_new_asset = """
                    update mz_fxsys_new_asset
                    set total_profit = total_profit+%s, yesterday_rebate=yesterday_rebate+%s,
                        total_rebate = total_rebate+%s,current_rebate=current_rebate+%s
                    WHERE user_id=%s
                """
                cursor.execute(sql_new_asset, (money, money, money, money, user_id))
            if payments_type == 2:
                sql_new_asset = """
                    update mz_fxsys_new_asset
                    set  total_profit=total_profit+%s, total_available_cash=total_available_cash+%s,
                          current_reward=current_reward+%s,total_reward=total_reward+%s,
                          available_reward=available_reward+%s
                    WHERE user_id=%s
                """
                cursor.execute(sql_new_asset, (money, money, money, money, money, user_id))
            if payments_type == 7:
                sql_new_asset = """
                    update mz_fxsys_new_asset
                    set total_available_cash=total_available_cash-%s, current_rebate=current_rebate-%s,
                        available_rebate=available_rebate-%s, already_rebate=already_rebate+%s
                    WHERE user_id=%s
                """
                money = abs(float(money))
                cursor.execute(sql_new_asset, (money, money, money, money, user_id))
            if payments_type == 8:
                sql_new_asset = """
                    update mz_fxsys_new_asset
                    set total_available_cash=total_available_cash-%s, current_reward=current_reward-%s,
                        available_reward=available_reward-%s, already_reward=already_reward+%s
                    WHERE user_id=%s
                """
                money = abs(float(money))
                cursor.execute(sql_new_asset, (money, money, money, money, user_id))

            if payments_type == 9:
                sql_new_asset = """
                    update mz_fxsys_new_asset
                    set current_rebate = current_rebate-%s,frozen_rebate=frozen_rebate+%s
                    WHERE user_id=%s
                """
                money = abs(float(money))
                cursor.execute(sql_new_asset, (money, money, user_id))
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
def delete_payments_by_id(conn, cursor, _id):
    """根据收支明细的ID，删除收支明细"""
    try:
        cursor.execute("select money, payments_type, user_id from mz_fxsys_payments WHERE id = %s", (_id,))
        payments = cursor.fetchone()
        if payments:
            money = payments["money"]
            payments_type = payments["payments_type"]
            user_id = payments["user_id"]
            if payments_type == 1:
                sql_new_asset = """
                    update mz_fxsys_new_asset
                    set total_profit = total_profit-%s, yesterday_rebate=yesterday_rebate-%s,
                        total_rebate = total_rebate-%s,current_rebate=current_rebate-%s
                    WHERE user_id=%s
                """
                cursor.execute(sql_new_asset, (money, money, money, money, user_id))
            if payments_type == 2:
                sql_new_asset = """
                    update mz_fxsys_new_asset
                    set  total_profit=total_profit-%s, total_available_cash=total_available_cash-%s,
                          current_reward=current_reward-%s,total_reward=total_reward-%s,
                          available_reward=available_reward-%s
                    WHERE user_id=%s
                """
                cursor.execute(sql_new_asset, (money, money, money, money, money, user_id))
            if payments_type == 7:
                sql_new_asset = """
                    update mz_fxsys_new_asset
                    set total_available_cash=total_available_cash+%s, current_rebate=current_rebate+%s,
                        available_rebate=available_rebate+%s, already_rebate=already_rebate-%s
                    WHERE user_id=%s
                """
                money = abs(float(money))
                cursor.execute(sql_new_asset, (money, money, money, money, user_id))
            if payments_type == 8:
                sql_new_asset = """
                    update mz_fxsys_new_asset
                    set total_available_cash=total_available_cash+%s, current_reward=current_reward+%s,
                        available_reward=available_reward+%s, already_reward=already_reward-%s
                    WHERE user_id=%s
                """
                money = abs(float(money))
                cursor.execute(sql_new_asset, (money, money, money, money, user_id))

            if payments_type == 9:
                sql_new_asset = """
                    update mz_fxsys_new_asset
                    set current_rebate = current_rebate+%s,frozen_rebate=frozen_rebate-%s
                    WHERE user_id=%s
                """
                money = abs(float(money))
                cursor.execute(sql_new_asset, (money, money, user_id))

            cursor.execute("delete from mz_fxsys_payments WHERE id = %s", (_id,))
            conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s,"
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=True)



@dec_timeit
@dec_make_conn_cursor
# 获取定量的每天返现
def get_quantitation_cash_back_day(conn, cursor):
    sql = """
        select * from mz_fxsys_user where cash_back_way=2 and is_suspend = 0 and is_graduate = 0
    """
    try:
        cursor.execute(sql, )
        quantitation = cursor.fetchall()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=quantitation)

