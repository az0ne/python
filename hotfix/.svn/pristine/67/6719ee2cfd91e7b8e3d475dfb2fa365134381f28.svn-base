#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
from tornado.web import url
import os
# from datetime import date, time, datetime, timedelta
# import logging

if django.VERSION[1] > 5:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
    django.setup()

# from mz_user.models import *
# from mz_course.models import *
# from mz_lps.models import *
# from mz_lps2.models import *
from mz_lps2.calc_view import *

define('port_3s', type=int, default=8031)
# logger = logging.getLogger('tornado_per_3s')
# fh = logging.FileHandler(settings.BACKEND_CALC_3S_PATH)
# ch = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# ch.setFormatter(formatter)
# logger.addHandler(fh)
# logger.addHandler(ch)


class HelloHandler(tornado.web.RequestHandler):
  def get(self):
    self.write('Hello from tornado_per_3s')

# 定时任务，每3秒轮询
# 处理 get_sum_before_classmeeting, get_sum_after_classmeeting,
# get_risk_in_week, calc_study_point_score，
def periodic_task():
    # global LOGGER_TORNADO
    LOGGER_TORNADO[0] = '3s'
    # 更新学力值与评测分
    count, count1 = calc_study_point_score()
    if count!=0 or count1!=0:
        logger.cache(dict(task_type='3s',method=calc_study_point_score.__name__,
                          text='处理异步队列长度: '+str(count)+' 跳过长度: '+str(count1)))

def main():
    parse_command_line()
    settings = {
        }

    handlers = [
        # other handlers...
        ('/tornado_per_3s', HelloHandler),
        ]

    tornado_app = tornado.web.Application(
        handlers, **settings
    )
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port_3s)

    tornado.ioloop.PeriodicCallback(periodic_task, 3*1000).start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
  main()
