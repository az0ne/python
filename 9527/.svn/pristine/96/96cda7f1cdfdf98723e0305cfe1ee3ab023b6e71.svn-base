#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('mz_lps4.mz_course',
                       # lps4任务管理
                       url(r'^task/edit/$', 'task.task_edit', name='lps4_task_edit'),
                       url(r'^task/list/$', 'task.task_list', name='lps4_task_list'),
                       url(r'^task/save/$', 'task.task_save', name='lps4_task_save'),
                       url(r'^task/delete/$', 'task.task_delete', name='lps4_task_delete'),
                       )

urlpatterns += patterns("mz_lps4.career.lps4_career",
                        url(r'^career/list/$', "career_list", name="career_list"),
                        url(r'^career/edit/$', "revise_career", name="revise_career"),
                        url(r'^career/save/$', "save_career", name="save_career"),
                        url(r'^career/sn_check/$', "check_short_name", name="check_career_short_name"),
                        )

urlpatterns += patterns("mz_lps4.tree",
                        url(r'^tree/list/$', "lps4_tree_list", name="tree_list"),
                        url(r'^tree/edit/$', "lps4_tree_edit", name="tree_edit"),
                        url(r'^tree/get_stage/$', "get_stage_by_career_id", name="tree_get_stage"),
                        url(r'^tree/save/$', "lps4_tree_save", name="tree_save"),
                        url(r'^tree/delete/$', "delete_lps4_by_id", name="tree_delete"),
                        )

urlpatterns += patterns("mz_lps4.teacher_evaluation.warningTime",
                        url(r'^warningTime/list/$', "warning_time_list", name="warningTimeList"),
                        url(r'^warningTime/edit/$', "warning_time_edit", name="warningTimeEdit"),
                        url(r'^warningTime/save/$', "warning_time_save", name="warningTimeUpdate"),
                        url(r'^warningTime/delete/$', "warning_time_delete", name="warningTimeDelete"),
                        )

urlpatterns += patterns("mz_lps4.teacher_evaluation.teacher_backlog",
                        url(r'^backlog/list/$', "teacher_back_list", name="teacherBacklogList"),
                        url(r'^backlog/show/$', "teacher_back_show", name="teacherBacklogShow"),
                        url(r'^backlog/export/$', "teacher_back_excel_export_by_month", name="teacherBacklogExport"),
                        url(r'^backlog/add_opt/$', "teacher_backlog_add_opt_log", name="teacher_backlog_add_opt_log"),
                        url(r'^backlog/list_opt/$', "teacher_backlog_opt_log_list", name="teacher_backlog_opt_log_list"),
                        )

urlpatterns += patterns("mz_lps4.coach.task_lib_view",
                        url(r'^task_lib/list/$', "task_lib_list", name="tasklibList"),
                        url(r'^task_lib/edit/$', "task_lib_edit", name="tasklibEdit"),
                        url(r'^task_lib/save/$', "task_lib_save", name="tasklibSave"),
                        url(r'^task_lib/delete/$', "task_lib_delete", name="tasklibDelete"),
                        url(r'^task_lib/get_tasks/$', "get_task_by_career", name="getTaskByCarrer"),
                        url(r'^task_lib/check_is_have/$', "check_is_have_content_by_task", name="check_task_is_have"),
                        )

urlpatterns += patterns("mz_lps4.coach.coach",
                        url(r'^coach/list/$', "coach_info_list", name="coachList"),
                        url(r'^coach/edit/$', "coach_info_edit", name="coachEdit"),
                        url(r'^coach/export_all/$', "export_all_coach", name="coachExportAll"),
                        )

urlpatterns += patterns("mz_lps4.student_health",
                        url(r'^health/list/$', "student_health_list", name="student_health_list"),
                        )
