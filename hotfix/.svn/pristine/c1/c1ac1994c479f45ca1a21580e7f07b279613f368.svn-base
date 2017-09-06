# -*- coding: utf-8 -*-

"""
@version: 2016/6/14
@author: Jackie
@contact: jackie@maiziedu.com
@file: urls.py
@time: 2016/6/14 9:51
@note:  ??
"""

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # 学生的学习面板
    url(r'^c(?P<class_id>\d+)/$', "mz_lps3_free.student.views.class_index", name='class_index'),
    # 学生预约免费试学
    url(r'^make_appointment/$', "mz_lps3_free.student.views.ajax_appointment_free_class",
        name='ajax_appointment_free_class'),
    # 获取问卷
    url(r'^c(?P<class_id>\d+)/get_q(?P<questionnaire_id>\d+)_status/$',
        "mz_lps3_free.student.views_questionnaire.get_student_q_status", name='q'),
    # 提交问卷
    url(r'^c(?P<class_id>\d+)/sub_q(?P<questionnaire_id>\d+)_status/$',
        "mz_lps3_free.student.views_questionnaire.receive_questionnaire", name='sq'),
)
