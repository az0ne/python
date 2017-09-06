# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include

urlpatterns = patterns(
    '',
    # 班级动态消息
    url(r'student/class/(?P<class_id>\d+)/dynmsg/$',
        "mz_lps3.views_student.student_class_dynmsg", name='student_class_dynmsg'),
    # 学生班级任务列表
    url(r'student/class/(?P<class_id>\d+)/$',
        "mz_lps3.views_student.student_class", name='student_class'),
    # 新任务
    url(r'student/task/(?P<class_id>\d+)_(?P<stagetask_id>\d+)/unlock/$',
        "mz_lps3.views_student.unlock_new_task", name='student_unlock_new_task'),
    # 新任务
    url(r'student/task/(?P<class_id>\d+)_(?P<stagetask_id>\d+)/unlock_guide/$',
        "mz_lps3.views_student.unlock_new_task_guide", name='student_unlock_new_task_guide'),
    # 重修
    url(r'student/task/(?P<class_id>\d+)_(?P<stagetask_id>\d+)/rebuild/$',
        "mz_lps3.views_student.rebuild_task", name='student_rebuild_task'),
    # 学生阶段任务任务详情
    url(r'student/task/(?P<class_id>\d+)_(?P<stagetask_id>\d+)/$',
        "mz_lps3.views_student.student_stagetask", name='student_stagetask'),
    # 学生的知识点item
    url(r'student/item/(?P<class_id>\d+)_(?P<stagetask_id>\d+)_(?P<item_id>\d+)/$',
        "mz_lps3.views_student.student_knowledgeitem", name='student_knowledgeitem'),
    # 学生看视频
    url(r'student/item_lesson/(?P<class_id>\d+)_(?P<stagetask_id>\d+)_(?P<item_id>\d+)/$',
        'mz_lps3.views_student.student_item_lesson', name='student_item_lesson'),
    # 学生更新用户观看视频进度
    url(r'student/ajax/item_lesson/update/(?P<user_knowledge_item_id>\d+)/$',
        'mz_lps3.views_ajax.update_learning_lesson', name='item_lesson_update_process'),

    # 学生补全资料
    # url(r'student/student_info_submit/$',
    #     "mz_lps3.views_student.student_info_submit", name='student_info_submit'),
    # 学生提交协议
    url(r'student/contract_submit/$',
        "mz_lps3.views_student.contract_submit", name='contract_submit'),

    # 学生关闭QQ加群提醒
    url(r'student/qq_hints_close/$',
        "mz_lps3.views_student.qq_hints_close", name='qq_hints_close'),

    # 学生选择是否需要就业
    url(r'student/employment_contract_submit/$',
        "mz_lps3.views_student.employment_contract_submit", name='employment_contract_submit'),

    # 老师班级面板
    url(r'teacher/class/(?P<class_id>\d+)/$',
        "mz_lps3.views_teacher.teacher_class", name='teacher_class'),
    # 开启班级
    url(r'teacher/class/(?P<class_id>\d+)/start/$',
        "mz_lps3.views_teacher.start_class", name='teacher_class_start'),

    # 老师查看教学大纲
    url(r'teacher/class/(?P<class_id>\d+)/syllabus/$',
        "mz_lps3.views_teacher.course_syllabus", name='teacher_course_syllabus'),

    # 查看学生完整学籍信息
    url(r'teacher/class/(?P<class_id>\d+)/student_info/(?P<student_id>\d+)/$',
        "mz_lps3.views_teacher.student_info", name='t_student_info'),
    # 导出学生完成学习信息
    url(r'teacher/class/(?P<class_id>\d+)/export_student_info/(?P<student_id>\d+)/$',
        "mz_lps3.views_teacher.export_student_info", name='t_export_student_info'),

    # 20160331老师端优化去掉休学入口
    # # 老师端,暂停/恢复 学生学习
    # url(r'teacher/class/(?P<class_id>\d+)/student_status/(?P<student_id>\d+)_(?P<to_status>(pause|resume))/$',
    #     "mz_lps3.views_teacher.pause_student_studying", name="t_pause_student_studying"),

    # 老师端,查看学生阶段信息
    url(r'teacher/class/(?P<class_id>\d+)/student_stage/(?P<student_id>\d+)_(?P<stage_id>\d+)/$',
        "mz_lps3.views_teacher.student_stage_div", name="t_student_stage_div"),

    # 学习历程
    url(r'student/class/(?P<class_id>\d+)/study_history/$',
        "mz_lps3.views_student.student_study_history", name='student_study_history'),
    # 学生直播班会历史列表
    url(r'student/class/(?P<class_id>\d+)/classmeeting/$',
        "mz_lps3.views_student.student_classmeeting", name='student_classmeeting'),
    # 播放班会
    url(r'^class_meeting/player/(?P<class_id>\w+)/(?P<play_id>\w+)/$',
        "mz_lps3.views_student.class_meeting_player", name='class_meeting_player'),

    # 老师
    # 老师直播班会历史列表
    url(r'^teacher/class/(?P<class_id>\d+)/classmeeting/$',
        "mz_lps3.views_teacher.teacher_classmeeting", name='teacher_classmeeting'),
    # 老师直播班会考勤
    url(r'^teacher/attendance/(?P<class_id>\d+)/(?P<classmeeting_id>\d+)/$',
        "mz_lps3.views_teacher.teacher_attendance", name='teacher_attendance'),
    # 创建临时班会
    url(r'^teacher/class/crate_classmeeting/$',
        "mz_lps3.views_teacher.create_classmeeting", name='create_classmeeting'),
    # 根据班会ID获取信息
    url(r'^teacher/class/classmeeting/(?P<classmeeting_id>\d+)/$',
        "mz_lps3.views_teacher.get_classmeeting", name='get_classmeeting'),
    # 修改临时班会
    url(r'^teacher/class/alter_classmeeting/(?P<classmeeting_id>\d+)/$',
        "mz_lps3.views_teacher.alter_classmeeting", name='alter_classmeeting'),

    # 任务面板全局消息
    url(r'student/ajax/global_message/$', 'mz_lps3.views_ajax.global_message', name='global_message'),
    # 任务面板任务成绩消息
    url(r'student/ajax/task_score_message/$', 'mz_lps3.views_ajax.task_score_message', name='task_score_message'),
    # 任务面板班会消息
    url(r'student/ajax/class_meeting_schedule/$', 'mz_lps3.views_ajax.class_meeting_schedule',
        name='class_meeting_schedule'),
    # 任务面板用户FPS信息
    url(r'student/ajax/head_user_info/(?P<user_id>\d+)/$', 'mz_lps3.views_ajax.head_user_info',
        name='head_user_info'),
    # 任务面板班会开始信息
    url(r'student/ajax/class_meeting_open/$', 'mz_lps3.views_ajax.class_meeting_open_message',
        name='class_meeting_open'),
    # 任务面板班会结束缺席信息
    url(r'student/ajax/class_meeting_absence/$',
        'mz_lps3.views_ajax.class_meeting_absence_message',
        name='class_meeting_absence'),

    # 项目制作
    url(r'^student/task_project/(?P<class_id>\d+)_(?P<stage_task_id>\d+)/$',
        'mz_lps3.views_student_project.get_project_task', name='student_project_task'),
    url(r'^student/item_project/(?P<class_id>\d+)_(?P<stage_task_id>\d+)_(?P<item_id>\d+)/$',
        'mz_lps3.views_student_project.get_project_item', name='student_project_item'),
    url(r'^student/project_score/(?P<class_id>\d+)/(?P<task_id>\d+)/$',
        'mz_lps3.views_student_project.task_project_score',
        name='student_project_score'),
    url(r'^student/project_detail/(?P<class_id>\d+)/(?P<stage_task_id>\d+)/(?P<item_id>\d+)/$',
        'mz_lps3.views_student_project.item_project_detail', name='item_project_detail'),
    url(r'^student/project/upload_task/(?P<class_id>\d+)/(?P<stage_task_id>\d+)/(?P<task_id>\d+)/$',
        'mz_lps3.views_student_project.project_upload_task',
        name='project_upload_task'),
    url(r'^student/project/upload_item/(?P<class_id>\d+)/(?P<stage_task_id>\d+)/(?P<item_id>\d+)/$',
        'mz_lps3.views_student_project.project_upload_item',
        name='project_upload_item'),
    url(r'^teacher/project_marking/(?P<class_id>\d+)/(?P<student_id>\d+)/(?P<stage_task_id>\d+)/$',
        'mz_lps3.views_teacher_qx.set_course_project_score', name='teacher_project_marking'),
    url(r'^teacher/task_project/(?P<class_id>\d+)_(?P<student_id>\d+)_(?P<stage_task_id>\d+)/$',
        'mz_lps3.views_teacher_qx.student_task_div', name='teacher_student_project_task'),
    url(r'^teacher/item_project/(?P<class_id>\d+)_(?P<student_id>\d+)_(?P<stage_task_id>\d+)_(?P<item_id>\d+)/$',
        'mz_lps3.views_teacher_qx.student_item_project_div', name='teacher_project_item'),
    # 限时答题
    # 做题与查看错题
    url(r'student/item_test/(?P<class_id>\d+)_(?P<stage_task_id>\d+)_(?P<knowledgeitem_id>\d+)/$',
        "mz_lps3.views_student.timed_test", name='timed_test'),
    # 交卷
    url(r'student/item_test/(?P<class_id>\d+)_(?P<stage_task_id>\d+)_(?P<knowledgeitem_id>\d+)/submit/$',
        "mz_lps3.views_student.submit_paper", name='submit_paper'),
    # 老师端查看学生错题
    url(r'teacher/item_test/(?P<class_id>\d+)_(?P<student_id>\d+)_(?P<stage_task_id>\d+)_(?P<knowledgeitem_id>\d+)/$',
        "mz_lps3.views_teacher_zyr.student_item_exam_div", name='teacher_test_item'),
    # 学生获取班级排名接口
    url(r'^student/get_ranking/$', "mz_lps3.views_student.student_rank_list"),

    # 教务
    url(r'^ea/', include('mz_eduadmin.urls', namespace='eduadmin')),
    # 学生查看入学须知
    url(r'^student/admission_infor/$', "mz_lps3.views_student.student_admission_infor", name='student_admission_infor'),
    # 学生查看不就业的服务
    url(r'^student/not_employment_agreement/$', "mz_lps3.views_student.student_not_employment_agreement", name='student_not_employment_agreement'),
    # 学生查看就业协议
    url(r'^student/employment_agreement/(?P<class_id>\d+)/$', "mz_lps3.views_student.student_employment_agreement", name='student_employment_agreement'),

    # 日历详情
    url(r'^student/class/(?P<class_id>\d+)/calender/$', "mz_lps3.views_student_yf.calender_detail", name='calender_detail'),

    # 每天班级排名
    url('^student/class_rank/(?P<class_id>\d+)/(?P<student_id>\d+)/$', 'mz_lps3.views_student.class_rank',
        name='class_rank'),
    # 学生已完成任务记录
    url('^student/finished_task_record/(?P<class_id>\d+)/(?P<student_id>\d+)/$', 'mz_lps3.views_ajax.finished_task_record',
        name='finished_task_record'),
    # 班级动态
    url('^student/class_dynamic_message/$', 'mz_lps3.views_ajax.class_dynamic_message',
        name='class_dynamic_message'),

)
