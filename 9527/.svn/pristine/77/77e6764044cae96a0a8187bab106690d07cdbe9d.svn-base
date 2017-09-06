# -*- coding: utf8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns(
    "mz_wechat",
    url(r'reply/edit/$', 'reply.edit_reply', name='edit_reply'),
    url(r'message/options/$', 'message.message_edit', name='edit_message'),
    url(r'message/list/$', 'message.message_list', name='message_list'),
    url(r'manual_update/$', 'message.manual_update', name='manual_update'),
    url(r'manual_update/sync_rules/$', 'message.sync_rules', name='sync_rules'),
    # API
    url(r'^message/upload/img/$', "views.upload_img_to_wechat", name="wechat_upload_img"),
    url(r'^message/get/news/$', "views.get_news_list", name="wechat_get_news_list"),
    url(r'^message/get/voice_or_video/$', "views.get_voice_or_video", name="wechat_get_voice_or_video"),
    url(r'^manual_update/sync_news/$', "views.sync_wechat_news", name="sync_wechat_news"),
    url(r'^manual_update/set_menu/$', "views.set_menu", name="set_menu"),
    url(r'^message/get/material/$', "views.get_material_data", name="get_material_data"),
)


urlpatterns += patterns("mz_wechat.menu",
                        url(r'^menu/list/$', 'wechat_menu_list', name='wechat_menu_list'),
                        url(r'^menu/edit/$', 'wechat_menu_edit', name='wechat_menu_edit'),
                        url(r'^menu/save/$', 'wechat_menu_save', name='wechat_menu_save'),
                        url(r'^menu/reply_list/$', 'menu_reply_list', name='menu_reply_list'),
                        url(r'^menu/reply_edit/$', 'menu_reply_edit', name='menu_reply_edit'),
                        url(r'^menu/reply_save/$', 'menu_reply_save', name='menu_reply_save'),
                        url(r'^menu/reply_del/$', 'menu_reply_delete', name='menu_reply_del'),
                        )

urlpatterns += patterns("mz_wechat.wechat_course.wechat_course_view",
                        url(r'^course/edit/$', 'wechat_course_edit', name='wechat_course_edit'),
                        url(r'^course/delete/$', 'del_wechat_course', name='wechat_course_del'),
                        url(r'^course/lesson/edit/$', 'wechat_lesson_edit', name='wechat_lesson_edit'),
                        url(r'^course/lesson/delete/$', 'del_wechat_lesson', name='wechat_lesson_del'),
                        url(r'^course/list/$', 'wechat_course_list', name='wechat_course_list'),
                        url(r'^course/lesson/list/$', 'wechat_lesson_list', name='wechat_lesson_list'),
                        url(r'^course/career/add_ajax/$', 'add_wechat_career_course', name='wechat_career_add_ajax'),
                        url(r'^course/modify/$', 'add_wechat_course', name='wechat_course_modify'),
                        url(r'^course/lesson/modify/$', 'add_wechat_lesson', name='wechat_lesson_modify'),
                        url(r'^course/career/list_ajax/$', 'list_wechat_career_course', name='wechat_career_list_ajax'),
                        url(r'^course/career/get_ajax/$', 'get_career_course_by_id', name='wechat_career_get_ajax'),
                        )

urlpatterns += patterns("mz_wechat.wechat_course.course_order",
                        url(r'^order/list/$', 'wechat_course_order_list', name='wechat_course_order_list'),
                        url(r'^order/edit/$', 'wechat_course_order_edit', name='wechat_course_order_edit'),
                        url(r'^order/update/$', 'wechat_course_order_update', name='wechat_course_order_update'),
                        )

urlpatterns += patterns("mz_wechat.wechat_course.wechat_course_question",
                        url(r'^question/list/$', 'wechat_question_list', name='wechat_course_question_list'),
                        url(r'^question/edit/$', 'wechat_question_edit', name='wechat_course_question_edit'),
                        url(r'^question/delete/$', 'wechat_question_del', name='wechat_course_question_delete'),
                        url(r'^question/save/$', 'wechat_question_save', name='wechat_course_question_save'),
                        )

urlpatterns += patterns("mz_wechat.wechat_course.wachat_banner",
                        url(r'^banner/list/$', 'wechat_banner_list', name='wechat_banner_list'),
                        url(r'^banner/edit/$', 'wechat_banner_edit', name='wechat_banner_edit'),
                        url(r'^banner/save/$', 'wechat_banner_save', name='wechat_banner_save'),
                        url(r'^banner/delete/$', 'wechat_banner_del', name='wechat_banner_del'),
                        )

urlpatterns += patterns("mz_wechat.wechat_course.wechat_discuss_views",
                        url(r'^discuss/list/$', 'list_parent_discuss', name='wechat_parent_discuss_list'),
                        url(r'^discuss/child_list/$', 'list_child_discuss', name='wechat_child_discuss_list'),
                        url(r'^discuss/edit/$', 'edit_wechat_discuss', name='wechat_discuss_edit'),
                        url(r'^discuss/save/$', 'insert_wechat_child_discuss', name='wechat_child_discuss_save'),
                        url(r'^discuss/delete/$', 'delete_parent_discuss', name='wechat_parent_discuss_delete'),
                        url(r'^discuss/child_delete/$', 'delete_child_discuss', name='wechat_child_discuss_delete'),
                        url(r'^discuss/child_back/$', 'back_to_parent_discuss', name='wechat_child_discuss_back'),
                        )
