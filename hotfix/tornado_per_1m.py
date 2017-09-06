#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,logging
from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
from tornado.web import url
if django.VERSION[1] > 5:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
    django.setup()
from mz_lps2.calc_view import get_sum_after_classmeeting,get_sum_before_classmeeting,get_risk_in_week ,\
    start_liveroom,close_liveroom,LOGGER_TORNADO,ClassOpType,logger
from mz_lps.models import Class
from mz_lps2.models import ClassMeetingTask
from mz_lps2.models import GiveScoreUserTask
from django.conf import settings
from datetime import timedelta, datetime

define('port_1m', type=int, default=8034)
# logger = logging.getLogger('tornado_per_1m')
# fh = logging.FileHandler(settings.CLASS_MEETING_TASK)
# ch = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# ch.setFormatter(formatter)
# logger.addHandler(fh)
# logger.addHandler(ch)

class HelloHandler(tornado.web.RequestHandler):
  def get(self):
    self.write('Hello from tornado_per_1m')


# 定时任务，每3秒轮询
# 处理 get_sum_before_classmeeting, get_sum_after_classmeeting,
def periodic_task():
    LOGGER_TORNADO[0] = '1m'
    try:
        class_set = Class.objects.select_related().filter(is_active=True, status=1).order_by('-id')
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0])
            return False
    for each_class in class_set:
        try:
            class_meeting_task_set = ClassMeetingTask.objects.select_related()\
                        .filter(user_class=each_class, is_temp=False).order_by('-id')[:2]
            tmp_class_meeting_task_set = ClassMeetingTask.objects.select_related()\
                        .filter(user_class=each_class, is_temp=True).order_by('-id')[:1]
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e,task_type=LOGGER_TORNADO[0],class_id=each_class.id)
                continue
        now = datetime.now()
        # 定期轮询各班，若无任何班会记录，或最近一条班会记录状态为已结束，则进入
        # get_sum_after_classmeeting
        if not class_meeting_task_set or class_meeting_task_set[0].status == 1:
            startline = class_meeting_task_set and class_meeting_task_set[0].startline or None
            try:
                get_sum_after_classmeeting([each_class], startline)
            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    logger.error(e,task_type=LOGGER_TORNADO[0],class_id=each_class.id)
                    pass
            else:
                logger.cache(dict(task_type='1m',class_id=each_class.id,method=get_sum_after_classmeeting.__name__))

        # 定期轮询各班，若最新一条班会记录状态为未开始，特定任务未执行，班会开始前15分钟内，则进入
        # get_sum_before_classmeeting
        if class_meeting_task_set and class_meeting_task_set[0].status == 0\
            and not class_meeting_task_set[0].is_check_before_classmeeting\
            and class_meeting_task_set[0].startline - now <= timedelta(minutes=15):
            try:
                get_sum_before_classmeeting([each_class], [class_meeting_task_set[0]])
                class_meeting_task_set[0].is_check_before_classmeeting = True
                class_meeting_task_set[0].status = 2 # 开启直播班会
                class_meeting_task_set[0].save()
                infodict=dict(task_type=LOGGER_TORNADO[0],class_id=each_class.id,
                      user_oper_type=ClassOpType.MEETING_OPENED,
                        classmeetingtask_id=class_meeting_task_set[0].id)
                logger.cache(infodict)
            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    logger.error(e,task_type=LOGGER_TORNADO[0],class_id=each_class.id)
                    pass
            else:
                logger.cache(dict(task_type='1m',class_id=each_class.id,method=get_sum_before_classmeeting.__name__))
        # 定期轮询各班，若已经是上次班会结束后（约为本次班会创建后）3天，且特定任务未执行，则进入
        # get_risk_in_week
        if class_meeting_task_set.count() > 1 and not \
            class_meeting_task_set[1].is_check_get_risk_in_week\
            and now - class_meeting_task_set[0].create_datetime >= timedelta(days=3): # to do
            try:
                get_risk_in_week([class_meeting_task_set[1]])
                class_meeting_task_set[1].is_check_get_risk_in_week = True
                class_meeting_task_set[1].save()
            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    logger.error(e,task_type=LOGGER_TORNADO[0],class_id=each_class.id)
                    pass
            else:
                logger.cache(dict(task_type='1m',class_id=each_class.id,method=get_risk_in_week.__name__))
        # 定期轮询各班，若存在「未开始临时」直播班会，且当前时间为开始时间前15分钟，则开启该临时直播班会
        if tmp_class_meeting_task_set and tmp_class_meeting_task_set[0].status == 0 \
                and tmp_class_meeting_task_set[0].startline - now <= timedelta(minutes=15):
            try:
                tmp_class_meeting_task_set[0].status = 2 # 开启临时班会
                tmp_class_meeting_task_set[0].save()
                start_liveroom(tmp_class_meeting_task_set[0].user_class) # 无条件开启直播室，不考虑当前该直播室状态
            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    logger.error(e,task_type=LOGGER_TORNADO[0],class_id=each_class.id)
                    pass
            else:
                logger.cache(dict(task_type='1m',class_id=each_class.id,method='start tmp classmeeting'))
        # 定期轮询各班，如果存在周班会开启时间超过3小时，则关闭直播间，结束班会
        if class_meeting_task_set and class_meeting_task_set[0].status == 2 \
            and now > class_meeting_task_set[0].startline + timedelta(hours=3):
            try:
                class_meeting_task_set[0].status = 1 # 结束周班会
                class_meeting_task_set[0].finish_date = now
                class_meeting_task_set[0].save()
                close_liveroom(class_meeting_task_set[0].user_class) # 无条件关闭直播室，不考虑当前该直播室状态
                infodict=dict(task_type=LOGGER_TORNADO[0],class_id=each_class.id,
                      user_oper_type=ClassOpType.MEETING_CLOSED,
                        classmeetingtask_id=class_meeting_task_set[0].id)
                logger.cache(infodict)
				# zhangyu 推送班会打分任务
                if not class_meeting_task_set[0].is_temp:
                    gsut = GiveScoreUserTask()
                    gsut.user = class_meeting_task_set[0].user_class.teacher
                    gsut.week = class_meeting_task_set[0]
                    gsut.startline = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    gsut.status = 2
                    gsut.save()
            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    logger.error(e,task_type=LOGGER_TORNADO[0],class_id=each_class.id)
                    pass
            else:
				logger.cache(dict(task_type='1m',class_id=each_class.id,method='end classmeeting'))
        # 定期轮询各班，如果存在临时班会开启时间超过3小时，则关闭直播间，结束班会
        if tmp_class_meeting_task_set and tmp_class_meeting_task_set[0].status == 2 \
            and now > tmp_class_meeting_task_set[0].startline + timedelta(hours=3):
            try:
                tmp_class_meeting_task_set[0].status = 1 # 结束临时班会
                tmp_class_meeting_task_set[0].finish_date = now
                tmp_class_meeting_task_set[0].save()
                if class_meeting_task_set[0].status !=2: #如果周班会正在进行则不关闭直播室
                    close_liveroom(tmp_class_meeting_task_set[0].user_class)
            except Exception, e:
                if settings.DEBUG:
                    print e
                    assert False
                else:
                    logger.error(e,task_type=LOGGER_TORNADO[0],class_id=each_class.id)
            else:
                logger.cache(dict(task_type='1m',class_id=each_class.id,method='end tmp classmeeting'))


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

    tornado.ioloop.PeriodicCallback(periodic_task, 1*60*1000).start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
  main()
