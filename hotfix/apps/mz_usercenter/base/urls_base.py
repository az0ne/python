# -*- coding: utf-8 -*-

"""
@version: 2016/5/19
@author: Jackie
@contact: jackie@maiziedu.com
@file: urls_base.py
@time: 2016/5/19 10:47
@note:  ??
"""
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # 个人中心的index,,进去后再根据角色跳转
    url('^$', 'mz_usercenter.base.views.view_base', name='index'),  # 个人账号设置
    url('^citylist/(?P<province_id>\d+)/$', 'mz_usercenter.base.views.get_city_list', name='get_city_list'),
    url('^myinfo/$', 'mz_usercenter.base.views.get_my_base_info', name='get_my_base_info'),
    url('^mymessage/$', 'mz_usercenter.base.views_message.my_message', name='get_my_message'),
)
