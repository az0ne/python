# -*- coding: utf-8 -*-

__author__ = 'changfu'

from django.conf.urls import patterns, url

from mz_wap import views, wiki_views, ad_views
from mz_wap import login_views
from mz_common.views import wap_article_tag_page

urlpatterns = patterns('',
                       # 　首页
                       url(r'^$', views.index_front, name="index_front"),
                       # 企业直通班介绍页
                       url(r'^course/$', views.career_course, name='career_course'),
                       # 企业直通班课程页(职业课程)
                       url(r'^course/(?P<course_id>.*?)-px/$', views.career_course_detail, name='career_course_detail'),

                       # 课程库
                       url(r'^course/all/$', views.course_list_all, name='course_list_all'),
                       # url(r'^course/list/(?P<category>[\w]+)-(?P<tag>[\w]+)/(?P<sort_by>[\d]+)-(?P<page>[\d]+)/$',
                       #     views.course_list, name='course_list'),
                       # 课程库筛选
                       url(r'^course/(?P<category>[\w]+)-(?P<tag>[\w]+)/(?P<sort_by>[\d]+)-(?P<page>[\d]+)/$',
                           views.course_list, name="stage_course_list"),
                       # 小课程页
                       url(r'^course/(?P<course_id>[\d]+)/$', views.course_detail, name='course_detail'),

                       # 小课程视频播放页
                       url(r'^course/(?P<course_id>[\d]+)-(?P<lesson_id>[\d]+)/$', views.lesson_view, name='lesson_detail'),

                       # 职业课程大纲页
                       url(r'^course/(?P<course_id>[-\w0-9]+)/$', views.career_course_syllabus, name='career_course_video_list'),

                       # lps 系统介绍
                       url(r'^lps_introduce/$', views.lps_introduce, name='lps_introduce'),

                       # WAP1.2迭代需求，WAP金牌教师详情页需与PC端金牌教师详情页URL保持一致．
                       # WAP端金牌教师详情页URL被一般老师详情页占用.故将金牌教师页和一般讲师页的URL交换
                       # 老师详情
                       url(
                           r'^u/(?P<teacher_id>[\d]+)/$',
                           views.teacher_detail, name='teacher_detail'
                       ),

                       #金牌教师详情页，根据SEO需求，WAP端金牌讲师URL与PC端金牌讲师保持一致，故增加common/部分
                       url(r'^common/teacher/(?P<teacher_id>\d+)/$', views.teacher_intro, name="teacher_intro"),

                       #分享落地页——视频分享
                       #分享落地页——视频分享
                       # 分享落地页——视频分享
                       url(r'^courses/(?P<course_id>[\d]+)/$', views.video_share, name='video_share'),
                       url(r'^courses/(?P<course_id>[\d]+)-(?P<lesson_id>[\d]+)/$', views.video_share,
                           name='video_play'),

                       # 落地页
                       url(r'^land/ui/$', ad_views.ui, name="wap_ad_ui"),
                       url(r'^land/pm/$', ad_views.pm, name="wap_ad_pm"),
                       url(r'^land/web/$', ad_views.web, name="wap_ad_web"),
                       url(r'^land/python/$', ad_views.python, name="wap_ad_python"),
                       url(r'^land/op/$', ad_views.op, name="wap_ad_op"),

                       # 分享落地页——任务完成分享
                       url(r'^careercourse/(?P<career_course_id>[\d]+)/$', views.task_share, name='task_share'),

                       #  显示讲师招募页
                       url(r'^teacher/recruit/$', views.teacher_recruit_show, name='teacher_recruit'),
                       #  显示麦子讲师申请表单
                       url(r'^teacher/recruit-form/$', views.apply_teacher_show, name='teacher_recruit_form'),
                       # 保存申请表单信息()
                       url(r'^teacher/recruit-form-save/$', views.teacher_recruit_save, name='teacher_recruit_save'),

                       # 登陆注册相关的url
                       url(r'^signup/$', login_views.sign_up, name='signup'),
                       url(r'^find_password/$', login_views.find_password, name='find_password'),

                       # 支付相关页面
                       url(r'^register_career_course/(?P<career_course_id>[\d]+)/$', views.register_career_course,
                           name='register_career_course'),

                       # 用户个人中心
                       url(r'home/base/$', views.wap_student_center, name='wap_student_center'),
                       # 保存个人信息
                       url(r'wap_save_user_info/$', views.wap_save_user_info, name='wap_save_user_info'),
                       # 搜索课程
                       url(r'^search/course/(?P<keyword>.*)-(?P<page_index>\d+)/$', views.wap_search_course,
                           name='wap_search_course'),
                       # 搜索文章
                       url(r'^search/article/(?P<keyword>.*)-(?P<page_index>\d+)/$', views.wap_search_article,
                           name='wap_search_article'),
                       # 搜索wiki
                       url(r'^search/wiki/(?P<keyword>.*)-(?P<page_index>\d+)/$', views.wap_search_wiki,
                           name='wap_search_wiki'),

                       url(r'^search/page/$', views.wap_search_page,
                           name='wap_search_page'),

                       url(r'^article_tag/page/$', wap_article_tag_page,
                           name='wap_article_tag_page'),

                       # wiki首页
                       url(r'^wiki/$', wiki_views.wiki_index, name="wiki_index"),
                       # wiki分类详情页
                       url(r'^wiki/(?P<short_name>\w+)/$', wiki_views.wiki_course_detail, name="wiki_course_detail"),
                       # wiki知识点详情页
                       url(r'^wiki/(?P<course_short_name>\w+|\w+[-_]\w+)/(?P<item_short_name>\w+|\w+[-_]\w+)/$',
                           wiki_views.wiki_item_detail, name="wiki_item_detail"),
                       )
