# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from mz_lps2 import views, teacher_views

urlpatterns = patterns('',
                       #处理学生个人资料完成任务
                       url(r'learning/plan/stu_profile_handle/$',
                           views.student_profile_handler,
                           name='student_profile_handler'),
                       #处理学生个人协议查看任务
                       url(r'^learning/plan/stu_contract_handle/$',
                           views.student_contract_handler),
                       #处理入学协议用户任务
                       url(r'^learning/plan/check_contract_handler/$',
                           views.check_contract_handler),
                       #处理学生给老师打分的任务
                       url(r'^learning/plan/giveScore_students_handler/(?P<careercourse_id>\d+)/$',
                           views.giveScore_students_handler),

                       url(r'^learning/plan/(?P<careercourse_id>\d+)/$',
                           views.student_class_view,
                           name='lps2_learning_plan'),

                       # 班级数据
                       url(r'^learning/plan_class/(?P<careercourse_id>\d+)/$',
                           views.student_class_data_view,
                           name='lps2_learning_plan_class'),

                       # 班级数据,查看其他周
                       url(r'^learning/plan_class/weekkpi/(?P<class_id>\d+)/$',
                           views.another_week_data_get,
                           name='lps2_learning_plan_weekkpi'),

                        #学生详细信息
                       url(r'learning/detail/(?P<careercourse_id>[\d]+)/$',
                           views.student_detail_view,
                           name='lps2_learning_detail'),

                       url(r'course/stage/(?P<careercourse_id>[\d]+)/(?P<stage_id>[\d]+)/(?P<user_id>[\d]+)/$',
                           views.stage_course_handler,
                           name='lps2_stage_course'),

                       url(r'stage/(?P<careercourse_id>[\d]+)/(?P<stage_id>[\d]+)/(?P<user_id>[\d]+)/$',
                           views.careercourse_stage_handler,
                           name='lps2_stage'),

                       url(r'uncomplete/quiz/by/lesson/(?P<lesson_id>[\d]+)/$',
                           views.get_uncomplete_quiz_by_lesson,
                           name='get_uncomplete_quiz_by_lesson'),

                        #老师
                       url(r'teach/plan/(?P<class_id>[\d]+)/$',
                           teacher_views.teacher_class_view,
                           name='lps2_teach_plan'),

                       #老师
                       url(r'teach/plan/(?P<class_id>[\d]+)/close_display/$',
                           teacher_views.close_display,
                           name='close_display'),

                       #老师已完成的任务
                        url(r'teach/plan/finishtask/(?P<class_id>[\d]+)/$',teacher_views.asyn_get_usertask_finish,
                            name='lps2_teach_plan_finishtask'),
                       # 老师班级数据,查看其他周
                       url(r'^teach/plan/weekkpi/(?P<class_id>\d+)$',
                           teacher_views.teacher_another_week_data_get,
                           name='lps2_teach_plan_weekkpi'),
                        #老师班级学生的任务情况
                        url(r'^teach/plan/studentsusertask/(?P<class_id>\d+)/$',
                           teacher_views.asyn_get_usertask_info),
                       #  #学生打分
                       # url(r'teach/classdata/(?P<class_id>[\d]+)/$',
                       #     teacher_views.student_score_update_view,
                       #     name='lps2_teach_data'),

                       url(r'teach/plan/(?P<class_id>[\d]+)/(?P<user_id>[\d]+)/$',
                           teacher_views.teacher_class_student_view,
                           name='lps2_teach_student_data'),

                       #处理教师须知查看任务
                       url(r'^teach/plan/teach_contract_handle/',
                           teacher_views.teacher_contract_handler),

                       #处理教师个人资料完成任务
                       url(r'^teach/plan/teach_profile_handle/$',
                           teacher_views.teacher_profile_handler,
                           name='teacher_profile_handler'),

                       # 请求学员打分操作
                       url(r'^teach/plan/ask_evaluate_stu_handle/$',
                           teacher_views.student_socre_required_data),

                       # 提交学员打分
                       url(r'^teach/plan/submit_stu_score_handle/$',
                           teacher_views.submit_stu_score_handler),


                       # 关闭直播班会
                       url(r'^teach/plan/finish_classmeeting_handle/$',
                           teacher_views.finish_classmeeting_handler),

                        # 更改直播班会时间
                       url(r'^teach/plan/modifier_class_meeting_time/$',
                           teacher_views.modifier_class_meeting_time),

                       url(r'^teach/plan/get_class_meeting_time/$',
                           teacher_views.get_classmeeting_time),

                       url(r'^teach/plan/create_temp_class_meeting/$',
                           teacher_views.create_temp_class_meeting),

                       # 暂停/恢复学习
                       url(r"user/teacher/pause_restore_planning/(?P<type>\w+)$",
                           teacher_views.pause_restore_planning,
                           name="pause_restore_planning"),
                       url(r'^teach/plan/teacher_suggest/$',
                           teacher_views.teacher_suggest,
                           name="teacher_suggest"),
                       url(r'^teach/plan/teacher_suggest_type/$',
                           teacher_views.teacher_suggest_type,
                           name="teacher_suggest_type"),
                        url(r'^teach/plan/teacher_suggest_complish/$',
                            teacher_views.get_send_context,
                            name="get_send_context"),
                       #播放班会
                       url(r'^teach/plan/player/(?P<ownerid>\w+)/$',
                           views.class_plan_player,name='class_plan_player'),
                       )



