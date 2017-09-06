# -*- coding: utf-8 -*-

"""
@version: 2016/5/16
@author: Jackie
@contact: jackie@maiziedu.com
@file: urls_home.py
@time: 2016/5/16 15:27
@note:  角色命名   学生:s,教师:t,教务:ea
"""

from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    url('^$', 'mz_usercenter.views.home_index', name='index'),  # 个人中心的index,,进去后再根据角色跳转

    url(r'^base/', include('mz_usercenter.base.urls_base', namespace='base')),  # 个人基本信息
    url(r'^settings/', include('mz_usercenter.base.urls_settings', namespace='settings')),  # 账号设置

    url(r'^s/', include('mz_usercenter.student.urls', namespace='student')),  # 学生端
    url(r'^t/', include('mz_usercenter.teacher.urls', namespace='teacher')),  # 老师端
    url(r'^ea/', include('mz_usercenter.eduadmin.urls', namespace='eduadmin')),  # 教务端

    url(r'^ajax_discuss_post/', 'mz_usercenter.views.ajax_discuss_post', name='ajax_discuss_post'),  # 异步提交回复
)
