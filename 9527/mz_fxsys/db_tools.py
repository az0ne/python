#! /usr/bin/env python
# -*- coding: utf-8 -*-


from apscheduler.schedulers.background import BackgroundScheduler
from calc_fxsys_data import for_quantitation_cash, update_all_liveness, calc_frozen_rebate, \
    all_user_static_rebate, check_all_profit
# ----------------------------------------------- 定时任务 ----------------------------------------------------------- #
# 初始化
# import datetime
# today_datetime = datetime.datetime.strptime("2017-03-9 18:00:00", "%Y-%m-%d %H:%M:%S")
# all_user_static_rebate(today_datetime)
# update_all_liveness(today_datetime)
# calc_frozen_rebate()
scheduler = BackgroundScheduler()
scheduler.add_job(all_user_static_rebate, 'cron', day_of_week='0-6', hour='23', minute='30')  # 统计静态返利
scheduler.add_job(update_all_liveness, 'cron', args=(None, True), day_of_week='0-6', hour='23',minute='40')  # 更新所有活跃度(结算)
scheduler.add_job(calc_frozen_rebate, 'cron', day_of_week='0-6', hour='23', minute='50')  # 计算冻结
scheduler.add_job(update_all_liveness, 'interval', hours=2)  # 更新所有活跃度(不结算)
scheduler.add_job(check_all_profit, 'cron', day_of_week='0-6', hour='06', minute='00')  # 更新总额统计
scheduler.add_job(for_quantitation_cash, 'interval', hours=24, start_date='2017-7-4 23:00')  # 更新定量返现

# 测试数据
#scheduler.add_job(for_quantitation_cash, 'cron', day_of_week='0-6', hour='23', minute='55')  # 更新定量返现
# scheduler.add_job(check_all_profit, 'interval', day_of_week='0-6', hours='13', minutes='00')  # 更新总额统计

# scheduler.add_job(for_quantitation_cash, 'interval', minutes=2, replace_existing=True)  # 更新定量返现
# scheduler.add_job(check_all_profit, 'interval', minutes=3)  # 更新总额统计

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
