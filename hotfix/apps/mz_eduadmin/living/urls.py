# -*- coding: utf-8 -*-

__author__ = 'Jackie'

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'mz_eduadmin.living.views.get_living', name='index'),
    url(r'^ajax_living_page/$', 'mz_eduadmin.living.views.ajax_living_page', name='ajax_living_page'),
    url(r'^ajax_living_attendance/(?P<class_id>\d+)/(?P<classmeeting_id>\d+)/$',
        "mz_eduadmin.living.views.ajax_living_attendance", name='ajax_living_attendance'),

)
