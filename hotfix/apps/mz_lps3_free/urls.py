# -*- coding: utf-8 -*-

"""
@version: 2016/6/12
@author: Jackie
@contact: jackie@maiziedu.com
@file: urls.py
@time: 2016/6/12 16:13
@note:  ??
"""

from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    # add by jackie 20160612  488免费试学引导
    # 课程大纲引导页
    url(r'^(?P<course_short_name>.*?)/syllabus/$',
        "mz_lps3_free.student.views.syllabus_index", name='syllabus'),

    # 课程预约页
    url(r'^(?P<course_short_name>.*?)/appointment/$',
        "mz_lps3_free.student.views.appointment_index", name='appointment'),

    # 学生端
    url(r'^s/', include('mz_lps3_free.student.urls', namespace='student')),

    # 老师端
    url(r'^t/', include('mz_lps3_free.teacher.urls', namespace='teacher')),
)
