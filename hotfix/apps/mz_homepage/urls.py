# -*- coding: utf-8 -*-

__author__ = 'Jackie'

from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    # url(r'^$', 'mz_homepage.views.homepage', name='index'),
    url(r'^get_course_category/', 'mz_homepage.views.get_course_categorys', name='get_course_category'),
)
