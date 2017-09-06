# -*- coding: utf-8 -*-

"""
@version: 2016/5/16
@author: Jackie
@contact: jackie@maiziedu.com
@file: urls_home.py
@time: 2016/5/16 15:27
@note:  角色命名   学生:s,教师:t,教务:ea
@FBI WARNING: 18+  SEO需求,对外每个页面一个固定的url,角色的首页统一为/u/xxx(id)/,无其他入口
"""

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # 个人中心的index,,进去后再根据角色跳转
    url('^(?P<user_id>\d+)/$', 'mz_usercenter.views.u_index', name='index'),

    # 学生个人主页---------------------------------------------------------------
    # url('^(?P<user_id>\d+)/s-course/$', 'mz_usercenter.student.views_public.public_mycourse', name='public_mycourse'),
    # 学生体验课程
    url('^(?P<user_id>\d+)/s-expcourse/$', 'mz_usercenter.student.views_public.public_expcourse', name='public_expcourse'),
    # TA的问答
    url('^(?P<user_id>\d+)/discuss/$', 'mz_usercenter.views.u_discuss', name='public_discuss'),
    url('^(?P<user_id>\d+)/ajax_problem/$', 'mz_usercenter.student.views_public.ajax_public_problem', name='ajax_problem'),
    url('^(?P<user_id>\d+)/ajax_answer/$', 'mz_usercenter.student.views_public.ajax_public_answer', name='ajax_answer'),
    # 异步获取回复
    url('^ajax_get_answer_by_problem_id/(?P<problem_id>\d+)/$', 'mz_usercenter.views.ajax_get_answer_by_problem_id',
        name='ajax_get_answer_by_problem_id'),
    # # 教师个人主页---------------------------------------------------------------------------
    # url('^(?P<user_id>\d+)/t-homepage/$', 'mz_usercenter.teacher.views_public.public_homepage',
    #     name='teacher_public_homepage'),
    # # 教务个人主页-------------------------------------------------------
    # url('^(?P<user_id>\d+)/ea-homepage/$', 'mz_usercenter.eduadmin.views_public.public_homepage',
    #     name='eduadmin_public_mycourse'),
)
