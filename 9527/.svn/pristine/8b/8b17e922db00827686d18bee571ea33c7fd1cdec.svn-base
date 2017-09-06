# -*- coding:utf-8 -*-
import copy
import decimal
from mz_fxsys.tool import get_cycle_start_time
from mz_fxsys.constant_pool import EVERYDAY_MAX_REBATE_AMOUNT, SALE_COURSE_PRICE
from db.api.apiutils import APIResult
from utils.logger import logger as log
from utils.tool import dec_timeit
from db.cores.mysqlconn import dec_make_conn_cursor


@dec_timeit
@dec_make_conn_cursor
def update_static_rebate(conn, cursor, today_datetime):

    # 当日总收益
    sql_totoal_revenue = """
        select total_revenue,id
        from mz_fxsys_total_revenue
        WHERE is_exe=0 and  TO_DAYS(date) = TO_DAYS(%s) ORDER BY `date` DESC
    """
    # 查询所有可以反奖学金的用户
    sql_all_user = """
        select user.id,user.role_id,rt.rebate_no,ass.total_rebate,user.activate_date from mz_fxsys_user as user
        left join mz_fxsys_new_asset as ass on user.id=ass.user_id
        left join mz_fxsys_rebatetype as rt on user.rebate_type_id=rt.id
        WHERE user.activate_date  is not null
            and user.is_suspend = 0
            and ass.total_rebate < (case user.role_id
                                    when 1 then 2999
                                    when 2 then 6999
                                    when 3 then 8800
                                    when 4 then 15800
                                    else 0
                                    END) * rt.rebate_no 
    """
    # 总余额
    sql_balances = """
        select COALESCE(sum(money),0) as balances
        from mz_fxsys_payments WHERE user_id = %s
    """
    sql_insert_payments = """
      insert into mz_fxsys_payments (user_id,order_id,payments_type,origin,money,total_money,`date`)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    # 累计返利
    sql_total_rebate = """
        select coalesce(SUM(money),0) as total_rebate
        from mz_fxsys_payments
        WHERE user_id = %s and payments_type = 1
        """
    # 当前返利
    sql_current_rebate = """
        select coalesce(SUM(money),0) as current_rebate
        from mz_fxsys_payments
        WHERE user_id = %s and payments_type in (1,7,9)
        """
    # 可提现
    sql_available_rebate = """
        select coalesce(SUM(money),0) as available_rebate
            from mz_fxsys_payments
            WHERE user_id = %s and payments_type = 1 and to_days(date) <= to_days(%s)
            or payments_type in (7,9) and user_id = %s
        """

    # 已经提现返利
    sql_already_rebate = """
        select coalesce(SUM(money),0) as already_rebate
        from mz_fxsys_payments
        WHERE user_id = %s and payments_type = 7
        """
    # 冻结返利
    sql_frozen_rebate = """
        select coalesce(SUM(money),0) as frozen_rebate
        from mz_fxsys_payments
        WHERE user_id = %s and payments_type = 9
        """
    # 总累计收益
    sql_total_profit = """
        select coalesce(SUM(money),0) as total_profit
        from mz_fxsys_payments
        WHERE user_id = %s and payments_type in (1,2)
        """
    # 推广可提现收益
    sql_available_reward = """
        select coalesce(SUM(money),0) as available_reward
        from mz_fxsys_payments
        WHERE user_id = %s and payments_type in (2,8)
        """

    sql_new_asset = """
        insert INTO mz_fxsys_new_asset
          (user_id,total_profit,total_available_cash,yesterday_rebate,total_rebate,current_rebate,available_rebate,
          already_rebate,frozen_rebate)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        ON DUPLICATE KEY UPDATE total_profit=%s,total_available_cash = %s,yesterday_rebate=%s,total_rebate=%s,
          current_rebate=%s,available_rebate=%s,already_rebate=%s,frozen_rebate=%s
    """
    sql_up_total_revenue = """
       update mz_fxsys_total_revenue set is_exe=1 WHERE id=%s
    """
    try:
        cursor.execute(sql_totoal_revenue, (today_datetime,))
        totoal_revenue_rl = cursor.fetchone()

        if totoal_revenue_rl:
            totoal_revenue = totoal_revenue_rl.get('total_revenue')
            totoal_revenue_id = totoal_revenue_rl.get('id')
            cursor.execute(sql_all_user)
            user_list = cursor.fetchall()
            user_count = len(user_list)
            base_rebate_num = ('%.2f' % (totoal_revenue / user_count))
            for user in user_list:
                actual_rebate_num = decimal.Decimal(copy.deepcopy(base_rebate_num))
                # 判断今天返利金额是否大于该身份的最大每日返利金额，超过就按角色身份的最大值返利
                curr_max_rebate = decimal.Decimal(EVERYDAY_MAX_REBATE_AMOUNT[str(user['role_id'])])
                if actual_rebate_num > curr_max_rebate:
                    actual_rebate_num = curr_max_rebate
                # 判断累计静态返利是否已超过最大返利金额
                max_rebate = decimal.Decimal(SALE_COURSE_PRICE[str(user['role_id'])]) * user['rebate_no']
                if (user['total_rebate'] + actual_rebate_num) > max_rebate:
                    actual_rebate_num = max_rebate - user['total_rebate']
                # 计算总余额并且插入收支表
                cursor.execute(sql_balances, (user["id"],))
                balances_result = cursor.fetchone()
                if balances_result:
                    balances = actual_rebate_num + balances_result["balances"]
                    cursor.execute(sql_insert_payments,
                                   (user['id'], 0, '1', '当日平台奖学金', actual_rebate_num, balances, today_datetime))
                # 累计返利
                cursor.execute(sql_total_rebate, (user['id'],))
                total_rebate = cursor.fetchone()["total_rebate"]
                # 当前返利
                cursor.execute(sql_current_rebate, (user['id'],))
                current_rebate = cursor.fetchone()["current_rebate"]
                # 可提现返利
                activate_date = user["activate_date"]
                now_date = today_datetime
                if activate_date:
                    now_date = get_cycle_start_time(activate_date, now_date)
                cursor.execute(sql_available_rebate, (user['id'], now_date, user['id']))
                available_rebate = cursor.fetchone()["available_rebate"]
                # 已经提现返利
                cursor.execute(sql_already_rebate, (user['id'],))
                already_rebate = cursor.fetchone()["already_rebate"]
                # 冻结返利
                cursor.execute(sql_frozen_rebate, (user['id'],))
                frozen_rebate = cursor.fetchone()["frozen_rebate"]
                # 总收益
                cursor.execute(sql_total_profit, (user['id'],))
                total_profit = cursor.fetchone()["total_profit"]
                # 总可提现
                cursor.execute(sql_available_reward, (user['id'],))
                available_reward = cursor.fetchone()["available_reward"]
                total_available = available_reward + available_rebate
                # 插入并更新资产表
                params = [total_profit, total_available, actual_rebate_num, total_rebate, current_rebate,
                          available_rebate, abs(already_rebate), abs(frozen_rebate)]
                cursor.execute(sql_new_asset, [user['id']]+params+params)
            cursor.execute(sql_up_total_revenue, (totoal_revenue_id,))
            conn.commit()
    except Exception as e:
        log.warn(
            "execute exception: %s. "
            "statement: %s" % (e, cursor.statement))
        raise e
    return APIResult(result=True)


@dec_timeit
@dec_make_conn_cursor
def validate_new_asset_if_exist(conn, cursor, user_id):
    """
    验证某用户的新收支明细情况是否已存在
    :param conn:
    :param cursor:
    :param user_id:
    :return:
    """
    try:
        cursor.execute(
            """
                select count(id) as counts from mz_fxsys_asset WHERE user_id=%s
            """, (user_id,)
        )
        asset_counts = cursor.fetchone()
    except Exception as e:
        log.warn(
            "execute exception: %s."
            "statement: %s" % (e, cursor.statement)
        )
        raise e
    return APIResult(result=asset_counts)