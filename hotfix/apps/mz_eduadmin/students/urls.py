# -*- coding: utf-8 -*-

__author__ = 'Jackie'

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'mz_eduadmin.students.views.index', name='index'),
    url(r'^(?P<class_id>\d+)_(?P<student_id>\d+)/change/$',
        'mz_eduadmin.students.views.student_change_class', name='student_change_class'),
    url(r'^(?P<class_id>\d+)_(?P<student_id>\d+)/quit/$',
        'mz_eduadmin.students.views.student_quit_class', name='student_quit_class'),
    url(r'^(?P<class_id>\d+)_(?P<student_id>\d+)/pause/$',
        'mz_eduadmin.students.views.student_pause', name='student_pause'),
    url(r'export_class_students/(?P<class_id>\d+)/$',
        'mz_eduadmin.students.views.export_class_students', name='export_class_students')
)
