# -*- coding: utf-8 -*-

__author__ = 'Jackie'

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^get_classes/$', 'mz_eduadmin.common.views.get_classes', name='get_classes'),
    url(r'^get_eduadmins/$', 'mz_eduadmin.common.views.get_eduadmins', name='get_eduadmins'),
    url(r'^get_teachers/$', 'mz_eduadmin.common.views.get_teachers', name='get_teachers'),
    url(r'^get_career_courses/$', 'mz_eduadmin.common.views.get_career_courses', name='get_career_courses')
)
