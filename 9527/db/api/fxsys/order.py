# -*- coding:utf-8 -*-

import decimal
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.api.apiutils import APIResult
from db.cores.mysqlconn import dec_make_conn_cursor
from mz_fxsys.constant_pool import SALE_COURSE_PRICE, SPREAD_BROKERAGE_SON, COURSE_PRICE


@dec_timeit
@dec_make_conn_cursor
def add_order(conn, cursor, user_id, order_No, order_price, student_name, date):
    """
    新插入一条订单信息
    :param conn:
    :param cursor:
    :param user_id:
    :param order_No:
    :param order_price:
    :param student_name:
    :param date:
    :return:
    """
    # 插入订单
    sql_insert_order = """
        insert into mz_fxsys_orders (user_id,order_No,order_price,student_name,date) VALUES (%s,%s,%s,%s,%s)
    """
    # 最后插入的订单ID
    last_order_id = """
        SELECT last_insert_id() AS last_order_id
        """

    # 总余额
    sql_balances = """
        select COALESCE(sum(money),0) as balances
        from mz_fxsys_payments WHERE user_id = %s
    """

    # 出入收支详情表
    sql_insert_payments = """
      insert into mz_fxsys_payments (user_id, order_id,payments_type,origin,money,total_money,`date`)
              VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    # 更新资产表
    sql_new_asset = """
      insert INTO mz_fxsys_new_asset
          (user_id,total_profit,total_available_cash,current_reward,total_reward,available_reward,reward_count)
      VALUES (%s,%s,%s,%s,%s,%s,%s)
      ON DUPLICATE KEY UPDATE total_profit=total_profit+%s, total_available_cash=total_available_cash+%s,
          current_reward=current_reward+%s,total_reward=total_reward+%s,
          available_reward=available_reward+%s,reward_count=reward_count+%s
    """

    try:
        # 插入订单表
        cursor.execute(sql_insert_order, (user_id, order_No, COURSE_PRICE[order_price], student_name, date))
        cursor.execute(last_order_id)
        order_id = cursor.fetchone()["last_order_id"]
        # 计算并且插入余额
        reward = decimal.Decimal(SALE_COURSE_PRICE[order_price]) * decimal.Decimal(SPREAD_BROKERAGE_SON[order_price])
        cursor.execute(sql_balances, (user_id,))
        balances = cursor.fetchone()["balances"]
        total_money = balances+reward
        cursor.execute(sql_insert_payments, (user_id, order_id, '2', student_name, reward, total_money,
                                             date))
        # 插入并更新资产表
        params = [reward, reward, reward, reward, reward, 1]
        cursor.execute(sql_new_asset, [user_id]+params+params)
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
def del_order(conn, cursor, order_id):
    """
    删除订单
    :param conn:
    :param cursor:
    :param order_id:
    :return:
    """
    # 删除
    sql_del_order = """
        delete from mz_fxsys_orders where id=%s
    """
    # 删除收支详情
    sql_del_payments = """
      delete from mz_fxsys_payments WHERE order_id = %s
    """
    # 查询推广基金
    sql_payments = """
        select money,user_id from mz_fxsys_payments WHERE order_id = %s
    """
    # 更新资产表
    sql_new_asset = """
      insert INTO mz_fxsys_new_asset
          (user_id,total_profit,total_available_cash,current_reward,total_reward,available_reward,reward_count)
      VALUES (%s,%s,%s,%s,%s,%s,%s)
      ON DUPLICATE KEY UPDATE total_profit=total_profit-%s, total_available_cash=total_available_cash-%s,
          current_reward=current_reward-%s,total_reward=total_reward-%s,
          available_reward=available_reward-%s,reward_count=reward_count-%s
    """

    try:
        # 删除订单表
        cursor.execute(sql_del_order, (order_id,))
        # 查询删除的推广基金
        cursor.execute(sql_payments, (order_id,))
        payments = cursor.fetchone()
        if payments:
            user_id = payments["user_id"]
            money = payments["money"]
            cursor.execute(sql_del_payments, (order_id,))

            params = [money, money, money, money, money, 1]
            cursor.execute(sql_new_asset, [user_id]+params+params)
            conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=True)

