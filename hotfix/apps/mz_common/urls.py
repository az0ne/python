# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from django.conf import settings
from django.views.decorators.cache import cache_page
from mz_common import views

urlpatterns = patterns('',
                       url(r'^course/list/$', views.index_course_ajax_page, name="index_course_ajax_page"),
                       url(r'^terminal/$', views.terminal, name="terminal"),
                       url(r'^recommend_keyword/$', cache_page(settings.CACHE_TIME)(views.recommend_keyword),
                           name="recommend_keyword"),
                       url(r'^course/search/$', views.course_search, name="course_search"),
                       url(r'^terminal/$', views.terminal, name="terminal"),
                       url(r'^apppage/$', views.apppage, name="apppage"),
                       url(r'^mobile/search/$', views.mobile_search, name="mobile_search"),
                       url(r'^newmessage/count/$', views.get_new_message_count, name="get_new_message_count"),
                       url(r'^coupon/vlidate/$', views.coupon_vlidate, name="coupon_vlidate"),
                       url(r'^browser/warning/$', TemplateView.as_view(template_name="mz_common/browser_warning.html"),
                           name="browser_warning"),
                       url(r'^lps/demo/$', views.lps_demo, name="lps_demo"),
                       url(r'^ajax/careercourse_list/$', views.index_ajax_careercourse_list,
                           name="index_ajax_careercourse_list"),
                       url(r'^app_consult_info/add/$', views.app_consult_info_add, name="app_consult_info_add"),
                       url(r'^app_consult_info_stream/add/$', views.app_consult_info_add_stream, name="app_consult_info_add_stream"),
                       url(r'^about/$', views.aboutus, name="about_us"),
                       url(r'^join/$', views.JoinUs.as_view(), name="join_us"),
                       url(r'^contact/$', views.contactus, name="contact_us"),
                       url(r'^study/$', TemplateView.as_view(template_name="study.html"), name="study"),
                       url(r'^aca_about/$', views.aca_about, name="aca_about"),
                       url(r'^novice/$', views.novice, name="novice"),
                       url(r'^we_share_token/$', views.wechat_share, name="wechat_share_token"),

                       # url(r'^article/list/$', views.article_list_view, name="article_list_view"),
                       # url(r'^article/(?P<article_id>[\d]+)$', views.article_detail_view, name="article_detail_view"),
                       # url(r'^teacher_recruit/$', views.teacher_recruit, name="teacher_recruit"),
                       # url(r'^teacher_recruit_form/$', views.teacher_recruit_form, name="teacher_recruit_form"),
                       # 用户反馈数据保存
                       url(r'^feedback/save/$', views.feedback_save, name="feedback_save"),
                       url(r'^feedback/image_upload/$', views.feedback_image_upload, name="feedback_image_upload"),
                       # #########################################################
                       # ajax interface
                       # #########################################################
                       url(r'^ajax/get/discuss', views.ajax_get_discuss, name="get_discuss"),
                       url(r'^ajax/add/discuss', views.add_discuss, name="add_discuss"),
                       url(r'^ajax/like/article', views.like_article, name="like_article"),
                       url(r'^ajax/teacher_recruit_form/$', views.ajax_teacher_recruit_form,
                           name="ajax_teacher_recruit_form"),

                       # #########################################################
                       # teacher interface
                       # @todo 讨论是否建立mz_teacher的APP来处理
                       # #########################################################
                       url(r'^teacher/(?P<teacher_id>\d+)/$', views.teacher_introduce, name="teacher_introduce"),
                       # ueditor上传地址
                       url(r'^upload/controller$', views.upload_controller, name="upload_controller"),

                       # #########################################################
                       # discuss interface
                       # #########################################################
                       # 提问
                       url(r'question_post/$', 'mz_common.views_discuss.question_post', name="discuss_post"),
                       # 回复
                       url(r'answer_post/$', 'mz_common.views_discuss.answer_post', name="discuss_post"),
                       # 全部问题加载更多
                       url(r'all_more/(?P<object_id>\d+)/(?P<last_id>\d+)/$',
                           'mz_common.views_discuss.get_all_questions', name="all_more"),
                       # 我的问题加载更多
                       url(r'my_more/(?P<object_id>\d+)/(?P<last_id>\d+)/$',
                           'mz_common.views_discuss.get_my_questions', name="my_more"),
                       # 一个问题加载更多
                       url(r'one_more/(?P<discuss_id>\d+)/(?P<last_id>\d+)/$',
                           'mz_common.views_discuss.view_get_one_question', name="one_more"),
                       # 上传问题图片
                       url(r'img/upload/$',
                           'mz_common.views_discuss.img_upload', name="img_upload"),


                       # 提问
                       url(r'question_post_lps4/$', 'mz_common.views_discuss.question_post_lps4', name="discuss_post_lps4"),
                       # 回复
                       url(r'answer_post_lps4/$', 'mz_common.views_discuss.answer_post_lps4', name="discuss_post_lps4"),
                       # 全部问题加载更多
                       url(r'all_more_lps4/(?P<object_id>\d+)/(?P<last_id>\d+)/$',
                           'mz_common.views_discuss.get_all_questions_lps4', name="all_more_lps4"),
                       # 我的问题加载更多
                       url(r'my_more_lps4/(?P<object_id>\d+)/(?P<last_id>\d+)/$',
                           'mz_common.views_discuss.get_my_questions_lps4', name="my_more_lps4"),
                       )

