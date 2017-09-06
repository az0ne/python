# -*- coding: utf-8 -*-

"""
@version: 2016/5/18
@author: Jackie
@contact: jackie@maiziedu.com
@file: urls.py
@time: 2016/5/18 14:26
@note:  ??
"""
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # 个人中心的index,,进去后再根据角色跳转
    url('^$', 'mz_usercenter.base.views.view_settings', name='index'),  # 个人账号设置
    url(r'^avatar/random/$', 'mz_usercenter.base.views_settings.avatar_random', name='avatar_random'),  # 随机头像
    url(r'^avatar/upload/$', 'mz_usercenter.base.views_settings.avatar_upload', name='avatar_upload'),  # 上传头像
    url(r'^avatar/save/$', 'mz_usercenter.base.views_settings.avatar_save', name='avatar_save'),  # 头像切片保存
    url(r'^bind_mobile/sendsms/$', 'mz_usercenter.base.views_settings.bind_mobile_sendsms', name='bind_mobile_sendsms'),
    url(r'^bind_mobile/$', 'mz_usercenter.base.views_settings.bind_mobile', name='bind_mobile'),
    url(r'^bind_email/sendemail/', 'mz_usercenter.base.views_settings.bind_email_sendemail',
        name='bind_email_sendemail'),
    url('^send_email_again/$', 'mz_usercenter.base.views_settings.send_email_again', name='send_email_again'),
    url('^modpwd/$', 'mz_usercenter.base.views_settings.password_change', name='modpwd'),  # 修改密码
    url('^ositeunbind$', 'mz_usercenter.base.views_settings.unbind_other_site', name='cancel_third_bind'),
)
