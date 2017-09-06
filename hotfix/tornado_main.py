#!/usr/bin/env python

# Run this with
# PYTHONPATH=. DJANGO_SETTINGS_MODULE=testsite.settings testsite/tornado_main.py
# Serves by default at
# http://localhost:8080/hello-tornado and
# http://localhost:8080/hello-django

# -*- coding: utf-8 -*-

from tornado.options import options, define, parse_command_line
import django.core.handlers.wsgi
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os
from tornado.web import url

if django.VERSION[1] > 5:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
    django.setup()

define('port', type=int, default=8080)

class HelloHandler(tornado.web.RequestHandler):
  def get(self):
    self.write('Hello from tornado')

# def calc_study_point():
#     print "hello study point"

def main():
    parse_command_line()
    wsgi_app = tornado.wsgi.WSGIContainer(
        django.core.handlers.wsgi.WSGIHandler())
    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "upload_path": os.path.join(os.path.dirname(__file__), "uploads"),
        #'debug': True,
        }

    handlers = [
        # other handlers...
        ('/hello-tornado', HelloHandler),
        ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
        # url(r"/uploads/(.+)", tornado.web.StaticFileHandler, dict(path=settings['upload_path']), name='upload_path'),
        # #("/uploads", tornado.web.StaticFileHandler),
        ]

    tornado_app = tornado.web.Application(
        handlers, **settings
    )
    # tornado_app = tornado.web.Application(
    #     [
    #       ('/hello-tornado', HelloHandler),
    #       url(r"/upload/(.+)", tornado.web.StaticFileHandler, dict(path=settings['upload_path']), name='upload_path')
    #       ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
    #       ], static_path =os.path.join(os.path.dirname(__file__), "static"), media_path = os.path.join(os.path.dirname(__file__),'uploads'))
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)

    # il=tornado.ioloop.IOLoop()
    # #il.start()
    # tornado.ioloop.PeriodicCallback(calc_study_point,3000).start()
    # il.start()

    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
  main()
