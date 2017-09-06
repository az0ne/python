# -*- coding: utf-8 -*-
"""
@version: 2016/5/17 0017
@author: lewis
@contact: lewis@maiziedu.com
@file: urls.py
@time: 2016/5/17 0017 10:48
@note:  学生端URLS
"""
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^course/$', 'mz_usercenter.student.views_course.view_mycourse', name='mycourse'),
    url(r'^ocourse/$', 'mz_usercenter.student.views_course.view_old_course', name='omycourse'),
    url(r'^ecourse/$', 'mz_usercenter.student.views_course.view_expcourse', name='expcourse'),
    url(r'^study/$', 'mz_usercenter.student.views.view_study_info', name='study_info'),
    url(r'^job/$', 'mz_usercenter.student.views.view_job_info', name='job_info'),
    url(r'^resume/$', 'mz_usercenter.student.views.view_resume_info', name='resume_info'),
    url(r'^order/$', 'mz_usercenter.student.views.view_order_info', name='order_info'),
    url(r'^discuss/$', 'mz_usercenter.student.views.view_my_discuss', name='my_discuss'),
    url(r'^ajax_studing_div/$', 'mz_usercenter.student.views.ajax_studying_div', name='ajax_studying_div'),
    url(r'^ajax_save_studybase/$', 'mz_usercenter.student.views.ajax_save_studybase', name='ajax_save_studybase'),
    url(r'^ajax_save_job/$', 'mz_usercenter.student.views.ajax_save_job', name='ajax_save_job'),
    url(r'^ajax_get_my_problem/$', 'mz_usercenter.student.views.ajax_get_my_problem', name='ajax_get_my_problem'),
    url(r'^ajax_get_my_answer/$', 'mz_usercenter.student.views.ajax_get_my_answer', name='ajax_get_my_answer'),
    url(r'^ajax_praise/$', 'mz_usercenter.student.views.ajax_praise', name='ajax_praise'),
    url(r'^ajax_save_resume_user_info/$', 'mz_usercenter.student.views.ajax_save_resume_user_info', name='ajax_save_resume_user_info'),
    url(r'^ajax_save_resume_work/$', 'mz_usercenter.student.views.ajax_save_resume_work', name='ajax_save_resume_work'),
    url(r'^ajax_del_resume_work/$', 'mz_usercenter.student.views.ajax_del_resume_work', name='ajax_del_resume_work'),
    url(r'^ajax_save_resume_edu/$', 'mz_usercenter.student.views.ajax_save_resume_edu', name='ajax_save_resume_edu'),
    url(r'^ajax_del_resume_edu/$', 'mz_usercenter.student.views.ajax_del_resume_edu', name='ajax_del_resume_edu'),
)
