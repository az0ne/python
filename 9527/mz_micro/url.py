from django.conf.urls import patterns, url

urlpatterns = patterns("mz_micro.webcast",
                       url(r'^webcast/save/$', 'webcast_save', name='webcast_save'),
                       url(r'^webcast/edit/$', 'webcast_edit', name='webcast_edit'),
                       url(r'^webcast/list/$', 'webcast_list', name='webcast_list'),
                       url(r'^webcast/update_student/$', 'update_student_by_id', name='webcast_update_student'),
                       url(r'^webcast/update_course_date/$', 'update_course_date_by_id', name='update_course_date'),
                       url(r'^webcast/change_status/$', 'webcast_status_change', name='change_status'),
                       url(r'^webcast/update_vod_url/$', 'update_vod_url_by_id', name='update_vod_url'),
                       url(r'^webcast/is_selected_course_time/$', 'is_selected_course_time', name='is_selected_course_time'),
                       )

urlpatterns += patterns("mz_micro.micro_ask",
                        url(r'^webcast/ask/list/$', 'micro_ask_list', name='micro_ask_list'),
                        url(r'^webcast/ask/save/$', 'micro_ask_save', name='micro_ask_save'),
                        url(r'^webcast/ask/reply/$', 'micro_ask_edit', name='micro_ask_reply'),
                        )
