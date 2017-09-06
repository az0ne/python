# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler
from maiziserver.db.api.activity.activity import daily_data_count, daily_sms_notify


scheduler = BackgroundScheduler()

scheduler.add_job(daily_data_count,'cron',day_of_week='0-6',hour='01',minute='00')
scheduler.add_job(daily_sms_notify,'cron',day_of_week='1-6',hour='10',minute='00')

# scheduler.add_job(daily_sms_notify,'interval',minutes=1)

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()

