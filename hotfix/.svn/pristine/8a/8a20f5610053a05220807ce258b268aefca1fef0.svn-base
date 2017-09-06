# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # lps---------------------------------------------------------------
    # 任务详情
    url(r'^(?P<class_id>\d+)_(?P<stagetask_id>\d+)/$', "mz_lps4.views_lps.lps4_stage_task", name='lps4_stage_task'),
    # 解锁任务
    url(r'^unlock/(?P<class_id>\d+)_(?P<stagetask_id>\d+)/$', "mz_lps4.views_lps.lps4_unlock_task", name='lps4_unlock_task'),
    # 更新用户的is_already_guided状态
    url(r'^update_is_already_guided/$', "mz_lps4.views_lps.update_is_already_guided", name='update_is_already_guided'),
    # lps---------------------------------------------------------------

    # 1v1直播---------------------------------------------------------------
    url(r'^mobile/sendsms/$', "mz_lps4.views.send_mobile_captcha_from_onevone_meeting",
        name='send_mobile_captcha_from_onevone_meeting'),
    url(r'^order_onevone_meeting/$', "mz_lps4.views.order_onevone_meeting", name='order_onevone_meeting'),
    url(r'^old_onevone_meeting_list/(?P<career_id>\d+)/$', "mz_lps4.views.old_onevone_meeting_list",
        name='old_onevone_meeting_list'),
    url(r'^onevone/avatar/upload/$', "mz_lps4.views.img_upload_onevone_meeting",
        name='img_upload_onevone_meeting'),
    url(r'^update_onevone_meeting/(?P<meeting_id>\d+)/$', "mz_lps4.views.update_onevone_meeting",
        name='update_onevone_meeting'),
    url(r'^onevone_meeting_success/(?P<meeting_id>\d+)/$', "mz_lps4.views.onevone_meeting_success",
        name='onevone_meeting_success'),
    url(r'^onevone_meeting_join_info/(?P<meeting_id>\d+)/$', "mz_lps4.views.onevone_meeting_join_info",
        name='onevone_meeting_join_info'),
    url(r'^ajax_onevone_list/(?P<career_id>\d+)/$', "mz_lps4.views.ajax_onevone_add_list_student",
        name='ajax_onevone_add_list_student'),
    url(r'^ajax_onevone_datelist/(?P<career_id>\d+)/$', "mz_lps4.views.ajax_onevone_datelist",
        name='ajax_onevone_datelist'),
    url(r'^ajax_date_onovone_meeting/(?P<meeting_id>\d+)/$', "mz_lps4.views.ajax_date_onovone_meeting",
        name='ajax_date_onovone_meeting'),
    url(r'^student_service/(?P<career_id>\d+)/$', "mz_lps4.views.student_onevone_meeting_list",
        name='student_service'),
    # 学生为班会打分
    url(r'^student_score_meeting/$',
        'mz_lps4.views.score_meeting', name='student_score_meeting'),
    # 1v1直播结束------------------------------------------------------------

    # 问答 -------------------------------------------------------------
    url(r'^discuss/(?P<career_id>\d+)/$', "mz_lps4.views_discuss.view_my_discuss", name='my_discuss'),
    url(r'^ajax_my_problem/$', "mz_lps4.views_discuss.ajax_get_my_problem", name='ajax_get_my_problem'),  # 异步获取我的问题
    url(r'^ajax_my_answer/$', "mz_lps4.views_discuss.ajax_get_my_answer", name='ajax_get_my_answer'),  # 异步获取我的回答
    url('^ajax_get_answer_by_problem_id/(?P<problem_id>\d+)/$', 'mz_lps4.views_discuss.ajax_get_answer_by_problem_id',
        name='ajax_get_answer_by_problem_id'),  # 异步获取回复

    # 问答结束 ----------------------------------------------------------
    # 1v1 运营----------------------------------------------------------
    url(r'^ajax_ops_verify/$', "mz_lps4.views.verify_mobile_and_insert_ops",
        name='verify_mobile_and_insert_ops'),
    url(r'^ajax_ops_is_exist/$', "mz_lps4.views.is_exist_onevone_ops", name='is_exist_onevone_ops'),
    # 1v1 运营结束------------------------------------------------------
    # 辅导-------------------------------------------------------------
    # 老师端 学生辅导列表
    url(r'^teacher_coach/(?P<career_id>\d+)/(?P<student_id>\d+)/$',
        'mz_lps4.views_coach.teacher_coach_list', name='teacher_coach_list'),
    # 老师新建学习辅导
    url(r'^teacher_create_coach/(?P<career_id>\d+)/(?P<student_id>\d+)/$',
        'mz_lps4.views_coach.teacher_create_coach', name='teacher_create_coach'),

    # 老师学生 辅导详情
    url(r'^coach/(?P<coach_id>\d+)/$',
        'mz_lps4.views_coach.coach_detail', name='coach_detail'),
    # 学生 项目辅导详情
    url(r'^student_coach_project/(?P<class_id>\d+)_(?P<stage_task_id>\d+)_(?P<item_id>\d+)/$',
        'mz_lps4.views_coach.student_coach_project', name='student_coach_project'),
    # 老师 项目辅导详情
    url(r'^teacher_coach_project/(?P<coach_id>\d+)/$',
        'mz_lps4.views_coach.teacher_coach_project', name='teacher_coach_project'),
    # 项目辅导上传文件
    url(r'^coach_project_upload/$',
        'mz_lps4.views_coach.coach_project_upload', name='coach_project_upload'),
    # 项目辅导老师打分
    url(r'^grade_coach_project/$',
        'mz_lps4.views_coach.grade_coach_project', name='grade_coach_project'),
    # 学生端辅导列表
    url(r'^student_coach/(?P<career_id>\d+)/$',
        'mz_lps4.views_coach.student_coach_list', name='student_coach_list'),

    # 学生为学习建议打分 弃用
    url(r'^student_score_service/$',
        'mz_lps4.views_service.score_service', name='student_score_service'),
    # 辅导 结束------------------------------------------------------------------

    # 任务面板任务成绩消息
    url(r'student/ajax/task_score_message/$', 'mz_lps4.views_lps.task_score_message', name='task_score_message'),

    # 学生查看入学须知
    url(r'^admission_infor/$',
        "mz_lps4.views.student_admission_infor", name='student_admission_infor'),
    # 学生查看不就业的服务
    url(r'^not_employment_agreement/$',
        "mz_lps4.views.student_not_employment_agreement", name='student_not_employment_agreement'),
    # 学生查看就业协议
    url(r'^employment_agreement/(?P<class_id>\d+)/$',
        "mz_lps4.views.student_employment_agreement", name='student_employment_agreement'),
)
