#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import django

if django.VERSION[1] > 5:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
    django.setup()

from utils.logger import logger as log
from tornado.options import options, define, parse_command_line
import tornado.ioloop
import tornado.web
import datetime, time
import db.api.lps.teacher_warning
from utils.send_sms_and_message import SendSmsAndMessage

define('port_lps4_teacher_briefing', type=int, default=8038)


def send_briefing_base(sms_tmpname, content_message):
    """
    发送工作简报的基础处理函数
    :param sms_tmpname:
    :param content_message:
    :return:
    """
    # 查询所有未处理并且未发短信的代办
    result = db.api.lps.teacher_warning.get_backlog_doing_all_teacher_id()
    if result.is_error():
        log.warn('filter_warning_backlog is error')
    for teacher_id_dict in result.result():
        teacher_id = teacher_id_dict['teacher_id']
        result = db.api.lps.teacher_warning.get_backlog_briefing_by_teacher_id(teacher_id)
        if result.is_error():
            log.warn('filter_warning_backlog is error')
            continue
        dict_briefing = result.result()
        if dict_briefing['total_count']:
            content_sms = [str(dict_briefing['meeting_count']), str(dict_briefing['learning_count']),
                           str(dict_briefing['q_a_count']), str(dict_briefing['project_count']),
                           str(dict_briefing['coach_count'])]
            custom = {
                "type": 0
                }
            content_message_new = content_message % dict_briefing['total_count']
            SendSmsAndMessage(teacher_id, sms_tmpname, content_sms, content_message_new, custom).send()


def send_briefing9():

    content_message = '【工作简报-待办任务】新的一天开始了，你目前还有%s条待办需要处理，加油吧~'
    send_briefing_base('app_teacher_briefing', content_message)
    # 下次执行的时间
    next_time9 = datetime.datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)+datetime.timedelta(days=1)
    tornado.ioloop.IOLoop.instance().add_timeout(time.mktime(next_time9.timetuple()), send_briefing9)


def send_briefing16():

    content_message = '【工作简报-待办任务】温馨提示，老师截止目前您还有%s条待办信息需要处理~'
    send_briefing_base('app_teacher_briefing', content_message)
    # 下次执行的时间
    next_time16 = datetime.datetime.now().replace(hour=16, minute=0, second=0, microsecond=0)+datetime.timedelta(days=1)
    tornado.ioloop.IOLoop.instance().add_timeout(time.mktime(next_time16.timetuple()), send_briefing16)


def periodic_task():
    now_time = datetime.datetime.now()
    now_time9 = now_time.replace(hour=9, minute=0, second=0, microsecond=0)
    now_time16 = now_time.replace(hour=16, minute=0, second=0, microsecond=0)
    if now_time < now_time9:
        tornado.ioloop.IOLoop.instance().add_timeout(time.mktime(now_time9.timetuple()), send_briefing9)
    else:
        tornado.ioloop.IOLoop.instance().add_timeout(time.mktime((now_time9+datetime.timedelta(days=1)).timetuple()),
                                                     send_briefing9)

    if now_time < now_time16:
        tornado.ioloop.IOLoop.instance().add_timeout(time.mktime(now_time16.timetuple()), send_briefing16)
    else:
        tornado.ioloop.IOLoop.instance().add_timeout(time.mktime((now_time16+datetime.timedelta(days=1)).timetuple()),
                                                     send_briefing16)


def main():
    parse_command_line()
    tornado_app = tornado.web.Application()
    tornado_app.listen(options.port_lps4_teacher_briefing)
    periodic_task()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
