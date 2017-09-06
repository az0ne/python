# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import RedirectView, TemplateView
from mz_common.views import *
from mz_user.uc import *
from xadmin.plugins import xversion
import xadmin

import mz_common

xversion.register_models()

urlpatterns = patterns(
    '',
    # 首页
    url(r'^$', 'mz_homepage.views.homepage', name="index_front"),
    # APPAPI
    url(r'^v4/', include('website.api.urls', namespace='app_api')),
    # 公共模块
    url(r'^common/', include('mz_common.urls', namespace='common')),
    # 用户模块
    url(r'^user/', include('mz_user.urls', namespace='user')),
    # 校园专区模块
    url(r'^academic/', include('aca_course.urls', namespace='academiccourse')),
    # 课程模块
    url(r'^course/', include('mz_course.urls_course', namespace='course')),
    url(r'^lesson/', include('mz_course.urls_lesson', namespace='lesson')),
    # 支付模块
    url(r'^pay/', include('mz_pay.urls', namespace='pay')),
    # lps模块
    url(r'^lps/', include('mz_lps.urls', namespace='lps')),
    # lps2.0模块
    url(r'^lps2/', include('mz_lps2.urls', namespace='lps2')),
    # lps3.0模块
    url(r'^lps3/', include('mz_lps3.urls', namespace='lps3')),
    # 首页模块改版
    url(r'^homepage/', include('mz_homepage.urls', namespace='homepage')),
    # 后台
    url(r'^xadmin/', include(xadmin.site.urls)),
    # 自定义后台
    url(r'^backend/', include('mz_backend.urls', namespace='backend')),
    # app接口
    url(r'^service/', include('mz_service.urls', namespace='service')),
    # 媒体文件和静态文件URL路径配置
    url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JS_DIRS}),
    url(r'^2016/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JSNEW_DIRS}),
    url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CSS_DIRS}),
    url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.IMAGE_DIRS}),
    # 验证码
    url(r'^captcha/', include('captcha.urls')),
    # 滑杆验证码
    url(r'^geetest/', include('geetest.urls')),
    # ucenter整合url,(不能再后面再加/，否则会出错)
    url(r'^api/uc.php$', uc_index, name="uc_index"),
    # android app下载链接
    url(r'^app/download/$', app_download, name="app_download"),

    # 重定向手机app接口和活动页面
    url(r'^services-api/app/$',
        RedirectView.as_view(url='http://old.maiziedu.com/services-api/app/')),
    url(r'^services-api/app/[^/]+$', old_redirect, name="old_redirect"),
    url(r'^activitypage/activitypage.html$', activitypage, name="activitypage"),
    url(r'^peixun/1017.html$', def_1017, name="def_1017"),
    url(r'^peixun/1018.html$', def_1018, name="def_1018"),
    url(r'^ios/ios.html$', ios, name="ios"),
    url(r'^ios/ios8.html$', ios8, name="ios8"),
    url(r'^tuijian/osc.html$', osc, name="osc"),
    url(r'^ios/protocol.htm$', protocol, name="protocol"),
    url(r'^live800/faq.html$', faq, name="faq"),

    # robots.txt和sitemap.xml
    url(r'^robots.txt', TemplateView.as_view(template_name="mz_common/robots.txt")),
    url(r'^sitemap1.xml$', TemplateView.as_view(template_name="sitemap/sitemap1.xml")),
    url(r'^sitemap2.xml$', TemplateView.as_view(template_name="sitemap/sitemap2.xml")),
    url(r'^sitemap3.xml$', TemplateView.as_view(template_name="sitemap/sitemap3.xml")),
    url(r'^sitemap4.xml$', TemplateView.as_view(template_name="sitemap/sitemap4.xml")),
    url(r'^sitemap5.xml$', TemplateView.as_view(template_name="sitemap/sitemap5.xml")),
    url(r'^sitemap6.xml$', TemplateView.as_view(template_name="sitemap/sitemap6.xml")),
    url(r'^sitemap7.xml$', TemplateView.as_view(template_name="sitemap/sitemap7.xml")),
    url(r'^baidu-verify-88F08C31E3.txt',
        TemplateView.as_view(template_name="mz_common/baidu-verify-88F08C31E3.txt")),

    url(r'^pages/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.PAGES_DIRS}),
    url(r'^aboutgaoxiao$', TemplateView.as_view(template_name="about.html")),
    # 高校专区restAPI数据接口
    url(r'^aca_api/', include('mz_service.rest_urls', namespace='aca_api')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # wap 站点
    url(r'^wap/', include('mz_wap.urls', namespace='wap')),

    # 其他用户
    url(r'^u/', include('mz_usercenter.urls_u', namespace='u')),
    # 个人中心
    url(r'^home/', include('mz_usercenter.urls_home', namespace='home')),
    # 文章详情
    url(r'^article/(?P<article_id>[\d]+)/$', article_detail_view, name="article_detail_view"),
    # 文章列表
    url(r'^article/(?P<article_type>[\w]*)/$', article_list_view, name="article_list_view"),
    # 文章列表标签
    url(r'^article/tag/(?P<tag_id>\d+)/$', mz_common.views.artilcle_list_tag_view, name="artilcle_list_tag_view"),

    url(r'^teacher/recruit/$', mz_common.views.teacher_recruit, name="teacher_recruit"),
    url(r'^teacher/recruit-form/$', mz_common.views.teacher_recruit_form, name="teacher_recruit_form"),

    url(r'^lps3f/', include('mz_lps3_free.urls', namespace='lps3f')),
	# wiki
    url(r'^wiki/', include('mz_wiki.urls', namespace='wiki')),

	# 微课
    url(r'^wike/', include('mz_wike.urls', namespace='wike')),

    # 全文搜索
    url(r'^search/', include('mz_homepage.url_search', namespace='search')),

    # lps4
    url(r'^lps4/', include('mz_lps4.urls', namespace='lps4')),

    # lps4_index
    url(r'^lps-(?P<career_id>\w+)/$', "mz_lps4.views_lps.lps4_index", name='lps4_index'),

    # fxSys
    url(r'^fxsys/', include("fxSys.urls", namespace="fxsys")),

    # APP domain
    url(r'^launchMainURL/$', "website.api.user.views.app_domain", name='app_domain'),

    # 落地页
    url(r'^land/', include("mz_ad.urls", namespace="land")),

    # line页面
    url(r'^line/', include("mz_line.urls", namespace="line")),
)


if settings.IS_MOBILE:  # 扩展wap的url
    from mz_wap.urls import urlpatterns as wap_urlpatterns
    urlpatterns = wap_urlpatterns + urlpatterns

# 定义404、500和维护模式页面处理
handler404 = 'mz_common.views.page_not_found'
handler500 = 'mz_common.views.page_error'
handler503 = 'mz_common.views.page_maintenance'
