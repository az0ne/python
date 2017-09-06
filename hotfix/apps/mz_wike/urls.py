# -*- coding: utf-8 -*-

__author__ = 'changfu'

from django.conf.urls import patterns, url
import views_wechat
import views


urlpatterns = patterns(
    '',
    # 微课列表页
    url(r'^$', views.wike_list, name='wike_list'),
    # # 微课详情页
    url(r'^(?P<wike_id>\d+)/$', views.wike_detail, name='wike_detail'),
    # 微课问答列表
    url(r'^wike_ask/$', views.wike_ask_list, name='wike_ask_list'),
    # 微课问答点赞
    url(r'^like_ask/$', views.like_micro_course_ask, name='like_wike_ask'),
    # 添加微课问答
    url(r'^add_wike_ask/$', views.add_wike_ask, name='add_wike_ask')
)

# 微信课程购买
urlpatterns += patterns(
    '',
    # 授权回调
    url(r'^wechat_callback/$', views_wechat.wechat_callback, name='wechat_callback'),
    # 课程列表
    url(r'^course_list/$', views_wechat.wechat_course_list, name='wechat_course_list'),
    # 课程详情
    url(r'^course/(?P<course_id>[\d]+)/$', views_wechat.wechat_course, name='wechat_course'),
    # 章节详情
    url(r'^course/(?P<course_id>[\d]+)-(?P<lesson_id>[\d]+)/$', views_wechat.wechat_lesson, name='wechat_lesson'),
    # 章节详情
    url(r'^my_course/$', views_wechat.my_course, name='my_course'),
    # 提交评论
    url(r'^post_discuss/$', views_wechat.post_discuss, name='post_discuss'),
    # 支付页
    url(r'^pay/$', views_wechat.wechat_course_pay, name='wechat_course_pay'),
    # 下单
    url(r'^order/$', views_wechat.wechat_submit_order, name='wechat_submit_order'),
    # 支付回调
    url(r'^notify/$', views_wechat.wechat_pay_notify, name='wechat_pay_notify'),

)
