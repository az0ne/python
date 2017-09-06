#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('mz_common.studyinfo',
                       url(r'^querystudy/infostu/$', 'studyinfo_query', name="studyinfoquery"),
                       url(r'^querystudy/infoquery/$', 'studyinfo_student', name="studyinfo"),
                       url(r'^querystudy/infodetail/', 'studyinfo_studentinfo', name="studydetail"),
                       )

urlpatterns += patterns('mz_common.careerObjRelation',
                        url(r'^careerobj_relation/list/$', 'careerObjRelation_list', name='careerobjrelation_list'),
                        url(r'^careerobj_relation/edit/add/$', 'careerObjRelation_add', name='careerobjrelation_add'),
                        url(r'^careerobj_relation/edit/$', 'careerObjRelation_edit', name='careerobjrelation_edit'),
                        url(r'^careerobj_relation/edit/update/$', 'careerobjrelation_update',
                            name='careerobjrelation_update'),
                        url(r'^careerobj_relation/ajax_check/$', 'careerobjrelation_ajax_check',
                            name='careerobjrelation_check')
                        )

urlpatterns += patterns('mz_common.androidVersion',
                        # android版本信息
                        url(r'^androidVersion/list/$', 'android_version_list', name='androidVersion_list'),
                        url(r'^androidVersion/edit/$', 'android_version_edit', name='androidVersion_edit'),
                        url(r'^androidVersion/save/$', 'android_version_save', name='androidVersion_save'),
                        )

urlpatterns += patterns('mz_common.iosVersion',
                        # ios版本信息
                        url(r'^iosVersion/list/$', 'ios_version_list', name='iosVersion_list'),
                        url(r'^iosVersion/edit/$', 'ios_version_edit', name='iosVersion_edit'),
                        url(r'^iosVersion/save/$', 'ios_version_save', name='iosVersion_save'),
                        )

urlpatterns += patterns('mz_common.feedback.feedback',
                        url(r'^feedback/list/$', 'feed_back_list', name='feed_back_list'),
                        url(r'^feedback/record/$', 'feedback_edit', name='feed_back_record'),
                        url(r'^feedback/save/$', 'feedback_save', name='feed_back_save'),
                        url(r'^feedback/list/export_excle/$', 'export_excle', name='feed_back_export_excle'),
                        )

urlpatterns += patterns('mz_common.course_wiki',
                        url(r'^courseWiki/list/$', 'course_wiki_list',
                            name='courseWiki_list'),
                        url(r'^courseWiki/edit/$', 'course_wiki_edit',
                            name='courseWiki_edit'),
                        url(r'^courseWiki/save/$', 'course_wiki_save',
                            name='courseWiki_save'),
                        )

urlpatterns += patterns('mz_common.login_statistical.views',
                        url(r'^statistical/ajax/$', 'get_login_statistical_num', name='statistical_ajax'),
                        url(r'^statistical/list/$', 'login_statistical', name='statistical_list'),
                        )

urlpatterns += patterns('mz_common.onevone.onevone_meeting',
                        url(r'^onevone_meeting/edit/$', 'onevone_meeting_edit', name='onevone_meeting_edit'),
                        url(r'^onevone_meeting/list/$', 'onevone_meeting_list', name='onevone_meeting_list'),
                        url(r'^onevone_meeting/update/$', 'onevone_meeting_update', name='onevone_meeting_update'),
                        url(r'^onevone_meeting/update_status/$', 'onevone_meeting_update_status',
                            name='onevone_meeting_update_status'),
                        url(r'^onevone_meeting/delete/$', 'onevone_meeting_delete', name='onevone_meeting_delete'),
                        )
urlpatterns += patterns('mz_common.onevone.userMeetingCount',
                        url(r'^meetingCount/list/$', 'userMeetingCount_list', name='userMeetingCount_list'),
                        url(r'^meetingCount/edit/$', 'userMeetingCount_edit', name='userMeetingCount_edit'),
                        url(r'^meetingCount/save/$', 'userMeetingCount_save', name='userMeetingCount_save'),
                        )

urlpatterns += patterns('mz_common.onevone.career_teacher',
                        url(r'^careerTeacher/list/$', 'careerTeacherList', name='careerTeacher_list'),
                        url(r'^careerTeacher/edit/$', 'careerTeacherEdit', name='careerTeacher_edit'),
                        url(r'^careerTeacher/save/$', 'careerTeacherSave', name='careerTeacher_save'),
                        )

urlpatterns += patterns('mz_common.resume',
                        url(r'^resume/show/$', 'resume_show', name='resume_show'),
                        url(r'^resume/list/$', 'resume_list', name='resume_list'),
                        url(r'^resume/docx/$', 'resume_to_docx', name='resume_docx'),
                        )

urlpatterns += patterns('mz_common.onevone.onevone_ops',
                        url(r'^ops/list/$', 'onevone_ops_list', name='onevone_ops_list'),
                        url(r'^ops/change_isdone/$', 'change_ops_is_done', name='onevone_ops_is_done'),
                        url(r'^ops/export/(?P<data_type>\d+)/$', 'export_excle', name='onevone_ops_export')
                        )

urlpatterns += patterns('mz_common.export_excel_about_lps',
                        url(r'^lpsData/excel/$', 'export_excel_about_lps', name='export_excel_about_lps'),
                        url(r'^lpsData/show/$', 'show_export_excel_about_lps', name='show_export_excel_about_lps'),
                        url(r'^lpsData/check/$', 'check_is_have_data', name='lps_check_is_have_data'),
                        )

urlpatterns += patterns('mz_common.app_consult_info_stream_views',
                        url(r'^app_consult_stream/list/$', 'app_consult_info_list', name='app_consult_info_list'),
                        url(r'^app_consult_stream/del/$', 'app_consult_info_del', name='app_consult_info_del'),
                        )

urlpatterns += patterns('mz_common.views',
                        url(r'^upload/file/$', 'upload_file', name='upload_file_interface'),
                        )

# urlpatterns += patterns('mz_common.upload_file',
#                         url(r'^upload/file/$', 'upload_file', name='upload_file'),
#                         )
