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
import logging

if django.VERSION[1] > 5:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
    django.setup()

# from mz_user.models import *
# from mz_course.models import *
# from mz_lps.models import *
# from mz_lps2.models import *
from mz_lps2.calc_view import *

define('port_30m', type=int, default=8033)

# logger = logging.getLogger('tornado_per_30m')
# BACKEND_CALC_30M_PATH = 'log/tornado_per_30m.log'
# fh = logging.FileHandler(settings.BACKEND_CALC_30M_PATH)
# ch = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# ch.setFormatter(formatter)
# logger.addHandler(fh)
# logger.addHandler(ch)


class HelloHandler(tornado.web.RequestHandler):
  def get(self):
    self.write('Hello from tornado_per_30m')

# 定时任务，每30分钟轮询
# 处理 calc_rank_in_class
def periodic_task():
    # global LOGGER_TORNADO
    LOGGER_TORNADO[0] = '30m'
    try:
        class_set = Class.objects.select_related().filter(is_active=True, status=1)
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0])
            return False
    for each_class in class_set:
        # 定期执行 calc_rank_in_class
        try:
            calc_rank_in_class([each_class])
        except Exception, e:
            if settings.DEBUG:
                print e
                assert False
            else:
                logger.error(e,task_type=LOGGER_TORNADO[0],class_id=each_class.id)
                pass
        else:
            logger.cache(dict(task_type='30m',class_id=each_class.id,method=calc_rank_in_class.__name__))

    #定期执行更新学生的学力排名
    try:
        update_rank_studypoint()
    except Exception, e:
        if settings.DEBUG:
            print e
            assert False
        else:
            logger.error(e,task_type=LOGGER_TORNADO[0])
    else:
        logger.info(update_rank_studypoint.__name__+'    '+'success')

def main():
    parse_command_line()
    settings = {
        }

    handlers = [
        # other handlers...
        ('/tornado_per_30m', HelloHandler),
        ]

    tornado_app = tornado.web.Application(
        handlers, **settings
    )
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port_30m)

    tornado.ioloop.PeriodicCallback(periodic_task, 30*60*1000).start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
  main()
