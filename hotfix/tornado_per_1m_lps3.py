#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'guotao'
import os

from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi

if django.VERSION[1] > 5:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
    django.setup()
from mz_lps3.calc_functions import create_classmeeting, logger, LOGGER_TORNADO, LPS3_ClassOpType, \
    send_sms_attendance, send_sms_start_class_meeting, send_sms_start_class_meeting_free
from mz_lps.models import Class
from mz_lps3.models import ClassMeeting
from mz_eduadmin.stats.interface import DateDefine
from django.conf import settings
from datetime import timedelta, datetime
from tasks import student_status_monitor, calc_class_rank_record, app_push_message
from mz_course.interface_publicMeeting import public_meeting_send_sms_3hours_ago

define('port_1m', type=int, default=8035)


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello from tornado_per_1m_lps3')


def periodic_task():
    LOGGER_TORNADO[0] = '1m_lps3'
    try:
        class_set = Class.objects.xall().filter(
            is_active=True, status=1, lps_version='3.0',
            class_type__in=[Class.CLASS_TYPE_NORMAL, Class.CLASS_TYPE_FREE_488]).order_by('-id')
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e, task_type=LOGGER_TORNADO[0])
            return False
    for each_class in class_set:
        try:
            class_meeting_late = ClassMeeting.objects.select_related().filter(
                classmeetingrelation__class_id=each_class.id, is_temp=False).order_by('-id')[:1]
            class_meeting_lst = ClassMeeting.objects.select_related().filter(
                classmeetingrelation__class_id=each_class.id, status=0).order_by('-id')
            class_meeting_doing = ClassMeeting.objects.select_related().filter(
                classmeetingrelation__class_id=each_class.id, status=2).order_by('-id')
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e, task_type=LOGGER_TORNADO[0], class_id=each_class.id)
                continue

        # 定期轮询各班，若无任何班会记录，或最近一条班会记录状态为已结束，则创建下周班会
        if not class_meeting_late or class_meeting_late[0].status == 1:
            startline = class_meeting_late and class_meeting_late[0].startline or None
            try:
                create_classmeeting(each_class, startline)
            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    logger.error(e, task_type=LOGGER_TORNADO[0], class_id=each_class.id,
                                 class_meeting_id=class_meeting_late[0].id)

            else:
                logger.cache(
                    dict(task_type=LOGGER_TORNADO[0], class_id=each_class.id, method=create_classmeeting.__name__))

        now = datetime.now()
        # 定期轮询各班，如果班会记录状态为未开始，且班会开始前15分钟内，更改班会状态
        for class_meeting in class_meeting_lst:
            delta_time = class_meeting.startline - now
            if delta_time <= timedelta(minutes=15):
                try:
                    class_meeting.status = 2  # 开启直播班会
                    class_meeting.save()
                except Exception, e:
                    if settings.DEBUG:
                        print e
                        assert False
                    else:
                        logger.error(e, task_type=LOGGER_TORNADO[0], class_id=each_class.id)
                        pass
                else:
                    logger.cache(dict(task_type=LOGGER_TORNADO[0], class_id=each_class.id,
                                      user_oper_type=LPS3_ClassOpType.MEETING_OPENED,
                                      class_meeting_id=class_meeting.id))

                if not each_class.class_type == Class.CLASS_TYPE_FREE_488:
                    send_sms_start_class_meeting(each_class, class_meeting)  # 非免费488班会开始15分钟短信

            if each_class.class_type == Class.CLASS_TYPE_FREE_488 and class_meeting.content == u'首次班会' \
                    and delta_time.total_seconds() >= 0 and delta_time <= timedelta(hours=3):
                send_sms_start_class_meeting_free(each_class, class_meeting)

        # 定期轮询各班，如果存在周班会开启时间超过6小时，则关闭直播间，结束班会
        for class_meeting in class_meeting_doing:
            if now > class_meeting.startline + timedelta(hours=6):
                try:
                    class_meeting.status = 1  # 结束直播班会
                    class_meeting.finish_date = now
                    class_meeting.save()
                    # 免费试学班级，当答疑班会结束时，更改班级状态,让班级不在参加循环
                    if each_class.class_type == Class.CLASS_TYPE_FREE_488 and class_meeting.content == u'答疑班会':
                        each_class.status = Class.STATUS_OVER
                        each_class.save()
                except Exception, e:
                    if settings.DEBUG:
                        print e
                        assert False
                    else:
                        logger.error(e, task_type=LOGGER_TORNADO[0], class_id=each_class.id)
                        pass
                else:
                    logger.cache(dict(task_type=LOGGER_TORNADO[0], class_id=each_class.id,
                                      user_oper_type=LPS3_ClassOpType.MEETING_CLOSED,
                                      class_meeting_id=class_meeting.id))

                send_sms_attendance(each_class, class_meeting)  # 班会结束考勤已经短信



def check_studying_task():
    from tasks import check_students_studying

    if datetime.now().hour in (1, 13):
        check_students_studying.main()


def moniter_create_studentquestionnaire_record_in_time():
    from tasks.lps3_eduadmin_stats import moniter_create_studentquestionnaire_record
    # 9: 6
    # if NOW.date() == LAST_DATE_OF_MONTH - ONE_DAY * 6 and NOW.hour == 0:
    dd = DateDefine()
    if dd.NOW.day == dd.LAST_DAY_OF_THIS_MONTH - 6 and dd.NOW.hour == 0:
        moniter_create_studentquestionnaire_record()


def moniter_cal_completion_and_satisfy():
    from tasks.lps3_eduadmin_stats import moniter_cal_month_completion, moniter_cal_tea_month_satisfy

    dd = DateDefine()
    if dd.NOW.day == 1 and dd.NOW.hour == 0:
        moniter_cal_month_completion()
        moniter_cal_tea_month_satisfy()


def main():
    parse_command_line()
    settings = {
    }

    handlers = [
        # other handlers...
        ('/tornado_per_1m', HelloHandler),
    ]

    tornado_app = tornado.web.Application(
        handlers, **settings
    )
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port_1m)

    tornado.ioloop.PeriodicCallback(periodic_task, 1 * 60 * 1000).start()
    tornado.ioloop.PeriodicCallback(check_studying_task, 1 * 1000 * 60 * 60).start()
    tornado.ioloop.PeriodicCallback(moniter_create_studentquestionnaire_record_in_time, 1 * 1000 * 60 * 60).start()
    tornado.ioloop.PeriodicCallback(moniter_cal_completion_and_satisfy, 1 * 1000 * 60 * 60).start()
    tornado.ioloop.PeriodicCallback(student_status_monitor.main, 1000 * 60 * 15).start()
    tornado.ioloop.PeriodicCallback(calc_class_rank_record.main, 1000 * 60 * 60).start()
    tornado.ioloop.PeriodicCallback(app_push_message.main_at, 1000 * 60 * 60).start()
    tornado.ioloop.PeriodicCallback(public_meeting_send_sms_3hours_ago, 1000 * 60 * 30).start()
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
