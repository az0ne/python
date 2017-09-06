# -*- coding: utf-8 -*-
"""
该脚本定时(90minutes)执行获取微信token的脚本
"""

from tornado.options import options, define, parse_command_line
import tornado.web
import tornado.httpserver

import os
import django

if django.VERSION[1] > 5:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
    django.setup()

from tasks import get_weixin_jsapi_ticket

define('port_90m', type=int, default=8036)


class HelloHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello from tornado_per_90m')

LOOP_TIME = 1.5 * 60 * 60 * 1000
# LOOP_TIME = 1000

def test():
    print 'I am working'

def main():
    parse_command_line()
    settings = {
    }

    handlers = [
        # other handlers...
        ('/tornado_per_90m', HelloHandler),
    ]

    tornado_app = tornado.web.Application(
        handlers, **settings
    )
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port_90m)

    tornado.ioloop.PeriodicCallback(get_weixin_jsapi_ticket.main, LOOP_TIME).start()
    # tornado.ioloop.PeriodicCallback(test, LOOP_TIME).start()
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
