# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # 老师面板
    url(r'^c(?P<class_id>\d+)/$', "mz_lps3_free.teacher.views.class_index", name='class_index'),
    # 查看学习信息
    url(r'^c(?P<class_id>\d+)/(?P<student_id>\d+)_(?P<stagetask_id>\d+)/$', "mz_lps3_free.teacher.views.teacher_task",
        name='teacher_task'),
    # 刷新班会信息
    url(r'^c(?P<class_id>\d+)/(?P<class_meeting_id>\d+)/$', "mz_lps3_free.teacher.views.flush_meeting",
        name='flush_meeting'),
)
