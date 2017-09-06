# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from mz_course import views, views_course_list, views_publicMeeting,interface_publicMeeting
from mz_course import functions

urlpatterns = patterns('',

                       # 课程详情页
                       url(r'^(?P<course_id>[\d]+)/$', views.course_detail_view, name="course_detail_view"),

                       # url(r'^list/$', views.CourseListView.as_view(), name="stage_course_list"),
                       url(r'^all/$', views_course_list.courses_list_all, name="stage_course_list_all"),
                       url(r'^(?P<catagories>[\w]+)-(?P<tag>[\w]+)/(?P<sort_by>[\d]+)-(?P<page_index>[\d]+)/$',
                           views_course_list.courses_list, name="stage_course_list"),
                       # 基于新架构和库表设计的课程库
                       # url(r'^list/$', views.CourseListViewNew.as_view(), name="stage_course_list"),

                       # 章节播放页
                       url(r'^(?P<course_id>[\d]+)-(?P<lesson_id>[\d]+)/$', views.lps4_lesson_video_view, name="lesson_video_view"),
                       # 课程价格检查页
                       url(r'^check/$', views.career_course_price_list, name='career_course_price_list'),
                       # 直通班学员动态
                       url(r'^get_student_dynamic/$', views.get_student_dynamic, name='get_student_dynamic'),
                       url(
                           r'^$',
                           views.CareerCourseListView.as_view(),
                           name='career_course_list'
                       ),
                       url(
                           r'^teachers/$',
                           views.TeacherListView.as_view(),
                           name='teacher_list'
                       ),

                       url(r'^onlinecode/$', views.get_code_result, name='get_command_result'),  # add by ym
                       url(r'^commandsave/$', views.save_code_result, name='save_code_result'),  # add by yx
                       url(r'^ajax/$', views.course_list_view_ajax, name='course_list_ajax'),
                       url(r'^score/$', views.score, name='score'),
                       # url(r'^onlinecode/$', views.get_code_result, name='get_command_result'),
                       url(r'^(?P<course_id>[\d]+)/$', views.oldcourse_view, name='oldcourse_detail'),
                       # 原课程介绍页
                       # url(r'^(?P<course_id>.*?)-px/$', views.CourseIntroductionView.as_view(), name='course_detail'),
                       # 机器学习URL
                       # url(r'^ai-px/$', "mz_course.views_intro.course_ai", name='mz_course_ai'),

                       # add_by_zhangyunrui 网站改版20160118 课程介绍页
                       url(r'^(?P<course_id>.*?)-px/$', "mz_course.views_intro.c_course_intro", name='course_detail'),

                       # 从课程介绍页进入学习页
                       url(r'^(?P<course_id>.*?)-px/study/$', "mz_course.views_intro.access_to_class",
                           name='access_to_class'),

                       url(r'^(?P<course_id>[-\w0-9]+)/$', views.course_view, name='career_course_detail'),
                       url(r'^(?P<course_id>[\d]+)/(?P<university_id>[\d]+)$', views.course_view,
                           name='course_detail_academic'),
                       url(r'^add/comment/$', views.add_comment, name='add_comment'),
                       url(r'^(?P<course_id>[\d]+)/recent/play/$', views.course_recent_play, name='course_recent_play'),
                       url(r'^(?P<course_id>[\d]+)/favorite/update/$', views.update_favorite, name='update_favorite'),
                       # url(r'^(?P<careercourse_id>[\d]+)/pay/other/$',views.course_pay_other,name='course_pay_other'),

                       url(
                           r'^(?P<careercourse>.*?)/(?P<course_id>[\d]+)-(?P<lesson_id>[\d]+)/$',
                           views.lesson_view,
                           name='lesson_view'
                       ),
                       #  职业课程公开课（预约直播课）
                       url(r'^publicmeeting/(?P<career_id>[\d]+)/$',views_publicMeeting.public_meeting_show, name='public_meeting_show'),
                       url(r'^publicmeeting/save/$',views_publicMeeting.public_meeting_save, name='public_meeting_data_save'),
                       url(r'^mobile/sendsms/$', interface_publicMeeting.mobile_send_captcha, name='mobile_send_sms'),
                       url(r'^mobile/verify/$', interface_publicMeeting.mobile_verify_captcha, name='mobile_verify'),
                       )
