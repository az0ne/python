# -*- coding: utf-8 -*-

__author__ = 'Jackie'

from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    url(r'^$', 'mz_eduadmin.students.views.index', name='index'),
    url(r'^students/', include('mz_eduadmin.students.urls', namespace='students')),
    url(r'^classes/', include('mz_eduadmin.classes.urls', namespace='classes')),
    url(r'^living/', include('mz_eduadmin.living.urls', namespace='living')),
    url(r'^stats/', include('mz_eduadmin.stats.urls', namespace='stats')),
    url(r'^common/', include('mz_eduadmin.common.urls', namespace='common')),
)
