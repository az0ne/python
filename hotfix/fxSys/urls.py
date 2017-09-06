# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from fxSys import views

urlpatterns = patterns('',
                       url(r'login/$', views.login, name="login"),
                       url(r'logout/$', views.logout, name="logout"),
                       url(r'index/$', views.index, name="index"),
                       url(r'close_notify/$', views.close_liveness_notify, name="close_liveness_notify"),
                       url(r'register/$', views.register, name="register"),
                       url(r'^rules/$', views.rules, name='rules'),
                       url(r'test/$', views.test),
                       url(r'^score_record/$', views.score_record, name='score_record'),
                       url(r'^score_record_more/$', views.score_record_more, name='score_record_more'),
                       )
