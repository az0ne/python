# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from mz_user import views
from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView, TemplateView
from mz_user import signal_view # 初始化信号
from mz_user.views import get_invitation_code, get_invitation_link_page, judge_nick_name_is_exist
from mz_user import wap_views

urlpatterns = patterns('',
                       url(r'^password/find/$',views.find_password,name='find_password'),
                       url(r'^password/find/mobile/$',views.find_password_mobile_code,name='find_password_mobile_code'),
                       url(r'^password/reset/update/view/$',views.update_reset_password_view,name='update_reset_password_view'),
                       url(r'^password/reset/update/$',views.update_reset_password,name='update_reset_password'),
                       url(r'^password/reset/(?P<account>[^/]+)/(?P<code>[^/]+)/$',views.reset_password,name='reset_password'),
                       url(r'^active/(?P<email>[^/]+)/(?P<code>[^/]+)/$',views.do_active,name='do_active'),
                       url(r'^register/email/$',views.email_register,name='email_register'),
                       url(r'^register/mobile/$',views.mobile_register,name='mobile_register'),
                       url(r'^register/mobile_verify/$',views.mobile_register_step_one,name='mobile_register_step_one'),
                       # url(r'^register/mobile/sendsms/$',views.send_sms_code,name='send_sms_code'),#老的验证码发送接口，注释掉
                       url(r'^register/mobile/sendsms_signup/$',views.send_sms_code_signup,name='send_sms_code'),
                       url(r'^login/$',views.user_login,name='login'),
                       url(r'^logout/$',views.user_logout,name='logout'),
                       url(r'^center/$',views.user_center,name='user_center'),
                       url(r'^student/favorite/$',views.student_myfavorite_view,name='student_myfavorite'),
                       url(r'^student/certificate/$',views.student_mycertificate_view,name='student_mycertificate'),
                       url(r'^student/certificate/download/(?P<certificate_id>[\d]+)/$',views.student_mycertificate_download,name='student_mycertificate_download'),
                       url(r'^student/avatar/upload/$', views.avatar_upload,name="avatar_upload"),
                       url(r'^student/avatar/crop/$', views.avatar_crop,name="avatar_crop"),
                       url(r'^message/$',views.user_mymessage_view,name='user_mymessage'),
                       url(r'^info/$',views.user_myinfo_view,name='user_myinfo'),
                       url(r'^info/save/$',views.user_info_save,name='user_info_save'),
                       url(r'^info/email/$',views.user_info_email,name='user_info_email'),
                       url(r'^city/list/$',views.city_list,name='city_list'),
                       url(r'^change/password/$',views.change_password,name='change_password'),
                       url(r'^get/careercourse/$',views.get_careercourse,name='get_careercourse'),
                       url(r'^mobile/update/$',views.user_update_mobile,name='user_update_mobile'),
                       url(r'^mobile/fetch/$',views.user_fetch_mobile,name='user_fetch_mobile'),
                       url(r'^mobile/update/sendsms/$',views.user_update_mobile_sendsms,name='user_update_mobile_sendsms'),
                       url(r'^email/update/$',views.user_update_email,name='user_update_email'),
                       url(r'^email/fetch/$',views.user_fetch_email,name='user_fetch_email'),
                       # 20160331老师端优化去掉老师创建班级入口
                       # url(r'^create/class/save/$',views.create_class_save,name='create_class_save'),
                       url(r'^mobile/register/$',views.mobile_register_view,name='mobile_register_view'),
                       url(r'^mobile/login/$',views.mobile_login_view,name='mobile_login_view'),
                       # url(r'^ucsynlogin/destory/$',views.destory_ucsynlogin_session,name='destory_ucsynlogin_session'),
                       # url(r'^goto/bbs/$',views.user_goto_bbs,name='user_goto_bbs'),
                       url(r'^get_study_goal/$',views.get_study_goal,name='study_goal'),
                       url(r'^get_study_base/$',views.get_study_base,name='study_goal'),
                       # 获取老用户的头像以及真实姓名
                       url(r'^get_photo_and_nickName/$', views.get_photo_and_nickname, name='get_photo_and_nickName'),
                       url(r'^send_again_email/$',views.send_again_mail,name='send_again_emial'),
                       # 第三方登录跳转
                       url(r'^connect/$', views.connect, name='connect'),
                       # 第三方登录回调
                       url(r'^connect/success/$', views.connect_success, name='connect_success'),
                       # 第三方登录接口
                       url(r'^connect/from_fps_settings/$', views.connect_from_fps_settings, name='connect_from_fps_settings'),
                       # 获取邀请码和二维码
                       url(r'^get_invitation_code/$', get_invitation_code, name='get_invitation_code'),
                       # 获取二维码的邀请链接
                       url(r'^get_invitation_link_page/(?P<invitation_code>[\w]+)/$', get_invitation_link_page, name='get_invitation_link_page'),
                       # 判断用户的nick_name是否存在
                       url(r'^nick_name_is_exist/$', judge_nick_name_is_exist, name='nick_name_is_exist'),
                       # 注册页面
                       url(r'^signup/$', views.sign_up, name='sign_up'),
                       # 注册成功页面
                       url(r'^sign_success/$', views.sign_success, name='sign_success'),
                       # 邀请介绍页
                       url(r'^invitation/share/$',  views.invitation_share, name="invitation_share"),
                       # 邀请链接页
                       url(r'^invitation/link/$',  views.invitation_link, name="invitation_link"),
                       # 保存就业信息
                       url(r'^jobintentioninfo/save/$', views.save_job_intention_info, name='jobintentioninfo_save'),
                       # 保存就业信息1.1
                       url(r'^jobintentioninfo31/save/$', views.save_job_intention_info_lps_3_1, name='jobintentioninfo_save_3_1'),
                       # 微信网页鉴权
                       url(r'^get_weixin_auth_token/$', views.get_weixin_auth_token, name='get_weixin_auth_token'),

                       # wap相关的注册,登陆页面, 重新定义view的原因在于, 某些Pc端的view无法重用
                       url(r'^wap_login/$', wap_views.user_login, name='wap_login'),
                       url(r'^register/wap_mobile_verify/$', wap_views.verify_random_code, name='verify_random_code'),
                       url(r'^register/wap_mobile/$', wap_views.wap_mobile_register, name='wap_mobile_register'),
                       # 找回密码, 验证随机验证码, 并发送短信验证码
                       url(r'^password/send_sms_code/$', wap_views.password_send_sms_code, name='password_send_sms_code'),
                       # 重置密码
                       url(r'^password/reset_password/$', wap_views.reset_password, name='password_reset_password'),
)

if settings.FPS_SWITCH:
    urlpatterns += patterns('',
           url(r'^teacher/$',RedirectView.as_view(url=settings.FPS_CENTER), name='teacher_center'),
           url(r'^student/$',RedirectView.as_view(url=settings.FPS_CENTER),name='student_center'),
    )
else:
    urlpatterns += patterns('',
           url(r'^teacher/$',views.teacher_myclass_view, name='teacher_center'),
           url(r'^student/$',views.student_mycourse_view,name='student_center'),
    )

from django.views.decorators.http import *