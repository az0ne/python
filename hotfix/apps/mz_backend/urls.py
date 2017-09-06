# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from mz_backend.views import *
from mz_backend import adminx_views as backend_views

urlpatterns = patterns('',
                       url(r'^login/$', admin_login, name="admin_login"),
                       url(r'^index/$', admin_index_view, name="admin_index_view"),
                       url(r'^logout/$', admin_logout, name="admin_logout"),
                       url(r'^update/video/length/view/$', update_video_length_view, name="update_video_length_view"),
                       url(r'^update/video/length/lessons/$', get_lessons_list, name="get_lessons_list"),
                       url(r'^update/video/length/(?P<lesson_id>[\d]+)/$', update_video_length, name="update_video_length"),
                       url(r'^join/class/step1/$', join_class_1_view, name="join_class_1_view"),
                       url(r'^join/class/step2/$', join_class_2_view, name="join_class_2_view"),
                       url(r'^join/class/save/$', join_class_save, name="join_class_save"),
                       url(r'^quit/class/step1/$', quit_class_1_view, name="quit_class_1_view"),
                       url(r'^quit/class/step2/$', quit_class_2_view, name="quit_class_2_view"),
                       url(r'^quit/class/save/$', quit_class_save, name="quit_class_save"),
                       url(r'^change/class/step1/$', change_class_1_view, name="change_class_1_view"),
                       url(r'^change/class/step2/$', change_class_2_view, name="change_class_2_view"),
                       url(r'^change/class/save/$', change_class_save, name="change_class_save"),
                       url(r'^order/list/$', order_list_view, name="order_list_view"),
                       url(r'^coupon/list/$', coupon_list_view, name="coupon_list_view"),
                       url(r'^coupon/list/details/(?P<coupon_id>[\d]+)/$', coupon_list_details, name="coupon_list_details"),
                       url(r'^main/$', admin_main, name="admin_main"),
                       url(r'^sync/avatar/view/$', sync_avatar_view, name="sync_avatar_view"),
                       url(r'^sync/avatar/users/$', get_user_list, name="get_user_list"),
                       url(r'^sync/avatar/sync/$', sync_avatar, name="sync_avatar"),
                       url(r'^recommend/reading/index/$', recommend_reading_index, name="recommend_reading_index"),
                       url(r'^recommend/reading/add/$', recommend_reading_edit, name="recommend_reading_add"),
                       url(r'^recommend/reading/edit/(?P<reading_id>[\d]+)/$', recommend_reading_edit, name="recommend_reading_edit"),
                       url(r'^recommend/reading/delete/(?P<reading_id>[\d]+)/$', recommend_reading_delete, name="recommend_reading_delete"),
                       url(r'^update/uuid/$', update_uuid, name="update_uuid"),
                       url(r'^liveroom/list/$', live_room_list, name="live_room_list"),
                       url(r'^create/liveroom/$', create_live_room, name="create_live_room"),
                       url(r'^update/liveroom/$', update_live_room, name="update_live_room"),
                       url(r'^msgbox/list/$', msg_send_list, name="msg_send_list"),
                       url(r'^create/msgbox/$', create_msg, name="create_msg"),
                       url(r'^acauser/list/$', acauser_list, name="acauser_list"),
                       url(r'^acauser/import/$', acauser_import, name="acauser_import"),
                       url(r'^acauser/export/$', acauser_export, name="acauser_export"),
                       url(r'^acauser/delete/$', acauser_delete, name="acauser_delete"),
                       url(r'^clear/cache/$', clear_cache, name="clear_cache"),
                       url(r'^clear/courses_cache/$', clear_courses_cache, name="clear_courses_cache"),#企业直通班缓存
                       #lps2.0升级使用（暂时，升级首次执行,升级完后可删除）
                       #url(r'^lps2/pay/update/$', lps2_pay_update, name="lps2_pay_update"),

                       #add by hidden
                       url(r'^update_video_length_view/$', backend_views.update_video_length_view, name="update_video_length_view"),
                       url(r'^join_class_step1/$', backend_views.join_class_1_view, name="join_class_step1"),
                       url(r'^quit_class_step1/$', backend_views.quit_class_1_view, name="quit_class_step1"),
                       url(r'^change_class_step1/$', backend_views.change_class_1_view, name="change_class_step1"),
                       url(r'^order_list/$', backend_views.order_list_view, name="order_list"),
                       url(r'^coupon_list/$', backend_views.coupon_list_view, name="coupon_list"),
                       url(r'^sync_avatar_view/$', backend_views.sync_avatar_view, name="sync_avatar_view"),
                       url(r'^recommend_reading_index/$', backend_views.recommend_reading_index, name="recommend_reading_index"),
                       url(r'^liveroom_list/$', backend_views.live_room_list, name="liveroom_list"),
                       url(r'^msgbox_list/$', backend_views.msg_send_list, name="msgbox_list"),
                       url(r'^acauser_list/$', backend_views.acauser_list, name="acauser_list"),
                       # url(r'^clear_cache/$', backend_views.clear_cache, name="clear_cache"),
                       #url(r'^lps2_pay_update/$', backend_views.lps2_pay_update, name="lps2_pay_update"),
                       url(r'^create_order/$', backend_views.create_order, name="create_order"),    # 财务手动录入线下转账
                       url(r'^get_course_price/$', backend_views.get_course_price, name="get_course_price"),    # 异步获取课程价格
                       url(r'^export_order/$', export_order , name="export_order")
  )