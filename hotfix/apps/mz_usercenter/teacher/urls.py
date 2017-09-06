# -*- coding: utf-8 -*-
"""
@version: 2016/5/11
@author: zhangyunrui
@contact: david.zhang@maiziedu.com
@file: url.py
@time: 2016/5/11 16:38
@note:  教师端url
"""
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'mz_usercenter.teacher.views.view_index', name='teacher_index'),  # 教师个人主页
    url(r'^class/$', 'mz_usercenter.teacher.views.view_processing_classes', name='processing_classes'),  # 进行中班级

    url(r'^oclass/$', 'mz_usercenter.teacher.views.view_lps2_classes', name='old_classes'),  # 进行中班级

    url(r'^gclass/$', 'mz_usercenter.teacher.views.view_graduated_classes', name='graduated_classes'),  # 已毕业班级

    url(r'^fclass/$', 'mz_lps3_free.teacher.views.view_free_classes', name='free_classes'),  # 免费试学班

    url(r'^sdiscuss/$', 'mz_usercenter.teacher.views.view_student_discuss', name='student_discuss'),  # 学生问答
    url(r'^one_meeting/$', 'mz_usercenter.teacher.views.onevone_meeting', name='onevone_meeting'),  # 1v1直播
    url(r'^onevone_service/$', 'mz_usercenter.teacher.views.onevone_service', name='onevone_service'),  # 1v1直播

    url(r'^ajax_onevone_add_list/$', 'mz_usercenter.teacher.views.ajax_onevone_add_list', name='ajax_onevone_add_list'),  # 1v1直播列表
    # url(r'^ajax_create_onevone/$', 'mz_usercenter.teacher.views.ajax_create_onevone', name='ajax_create_onevone'),  # 创建1v1直播列表
    url(r'^ajax_del_onevone/$', 'mz_usercenter.teacher.views.ajax_del_onevone', name='ajax_del_onevone'),  # 删除1v1直播列表
    url(r'^ajax_insert_onevone_attendance/$', 'mz_usercenter.teacher.views.ajax_insert_onevone_attendance',
        name='ajax_insert_onevone_attendance'),  # 插入老师考勤

    url(r'^ajax_check_free_class/$', 'mz_lps3_free.teacher.views.ajax_check_free_class',
        name='ajax_check_free_class'),  # 验证试验有免费试学班级

    url(r'^ajax_sdiscuss/(?P<class_type>\d+)/$', 'mz_usercenter.teacher.views.ajax_student_discuss',
        name='ajax_student_discuss'),  # 学生问答
)
