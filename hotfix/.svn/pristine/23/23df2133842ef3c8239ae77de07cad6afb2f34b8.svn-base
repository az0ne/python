# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns('',
                       # 登陆
                       url(r'^login/', 'website.api.user.views.app_user_login', name="login"),
                       # 登出
                       url(r'^logout/', 'website.api.user.views.app_user_logout', name="logout"),
                       # 发送短信
                       url(r'^checkPhone/', 'website.api.user.views.app_mobile_register_sms',
                           name="checkPhone"),
                       # 注册
                       url(r'^register/', 'website.api.user.views.app_mobile_register',
                           name="register"),
                       # 第三方校验
                       url(r'^thirdCheck/', 'website.api.user.views.third_check',
                           name="third_check"),
                       # 找回密码
                       url(r'^findPassword/', 'website.api.user.views.app_find_password',
                           name="findPassword"),
                       # 获取用户资料基本选项
                       url(r'^infoChoices/', 'website.api.user.views.app_user_info_choices',
                           name="info_choices"),
                       # 提交用户信息
                       url(r'^submitUserInfo/', 'website.api.user.views.app_submit_user_info',
                           name="submitUserInfo"),
                       # 上传头像
                       url(r'^updateAvatar/', 'website.api.user.views.app_upload_avatar',
                           name="updateAvatar"),
                       # 是否关注
                       # url(r'^getFollowRelationship/', 'website.api.user.views.app_is_follow',
                       #     name="FollowRelation"),
                       # 关注
                       # url(r'^follow/', 'website.api.user.views.app_follow', name="follow"),
                       # 获取用户信息
                       url(r'^getUserInfo/', 'website.api.user.views.app_get_user_info',
                           name="getUserInfo"),
                       # 获取反馈类型
                       url(r'^getFeedbackCategory/', 'website.api.user.views.app_feedback_types',
                           name="FeedbackType"),
                       # 提交意见反馈
                       url(r'^submitFeedback/', 'website.api.user.views.app_submit_feedback',
                           name="submitFeedback"),
                       # 联系人列表
                       # url(r'^getContact/', 'website.api.user.views.app_get_contact',
                       #     name="getContact"),
                       # 我的收藏
                       url(r'^getMyCollection/', 'website.api.user.views.app_my_collection',
                           name="getMyCollection"),
                       # 删除收藏
                       url(r'^delCollection/', 'website.api.user.views.app_del_collection',
                           name="delCollection"),
                       # 检查更新
                       url(r'^checkUpdate/', 'website.api.user.views.check_update',
                           name="check_update"),
                       # 更新设备token
                       url(r'^updatePushToken/', 'website.api.user.views.app_update_push_token',
                           name="updatePushToken"),
                       # 消息数量和系统消息
                       url(r'^getMsgCount/', 'website.api.user.views.app_message_count',
                           name="message_count"),
                       # 消息详情
                       url(r'^getMsgList/', 'website.api.user.views.app_message_detail',
                           name="message_detail"),
                       # 密码校验
                       url(r'^checkPassword/', 'website.api.user.views.app_check_password',
                           name="app_check_password"),
                       # 修改密码
                       url(r'^modifyPassword/', 'website.api.user.views.app_change_password',
                           name="app_change_password"),
                       # 绑定手机校验
                       url(r'^checkMobile/', 'website.api.user.views.app_check_mobile',
                           name="app_check_mobile"),
                       # 绑定手机
                       url(r'^bindMobile/', 'website.api.user.views.app_bind_mobile',
                           name="app_bind_mobile"),
                       # APP domain
                       url(r'^launchMainURL/$', "website.api.user.views.app_domain", name='app_app_domain'),
                       )

# course
urlpatterns += patterns('',
                        # # 获取方向
                        url(r'^getDirectionList/',
                            'website.api.course.views.app_get_direction_list', name="direction"),
                        url(r'^getDirectionCourse/',
                            'website.api.course.views.app_get_direction_list_new', name="direction_course"),
                        # # 获取方向职业课程
                        url(r'^getClassList/', 'website.api.course.views.app_direction',
                            name="direction_career"),
                        # 收藏课程
                        url(r'^collectLesson/', 'website.api.course.views.app_collect_course',
                            name="collectLesson"),
                        # 为课程打分
                        url(r'^gradeLesson/', 'website.api.course.views.app_grade_course',
                            name="gradeLesson"),
                        # 获取课程视频列表
                        url(r'^getLessonList/', 'website.api.course.views.app_lesson_list',
                            name="getLessonList"),
                        # 视频播放
                        url(r'^getVideoDetail/', 'website.api.course.views.app_course_video',
                            name="course_video"),
                        # 课程库
                        url(r'^courseStore/', 'website.api.course.views.app_course_list',
                            name="getLessonList"),
                        # 更多课程
                        url(r'^getMoreCourseList/', 'website.api.course.views.app_get_more_course_list',
                            name="getMoreCourseList"),
                        # 直通班课程
                        url(r'^courseList/', 'website.api.course.views.app_courses',
                            name="courseList"),
                        # 课程搜索
                        url(r'^search/', 'website.api.course.views.app_course_search',
                            name="search"),
                        # 搜索热门关键字
                        url(r'^getHotSearch/', 'website.api.course.views.app_hot_search',
                            name="getHotSearch"),
                        # 课程评论
                        url(r'^getLessonComments/', 'website.api.course.views.app_get_comment_list',
                            name="comments"),
                        # 提交课程评论
                        url(r'^submitComment/', 'website.api.course.views.app_submit_comment',
                            name="submitComment"),
                        # 老师课程
                        url(r'^getHisCourse/', 'website.api.course.views.app_teacher_course',
                            name="getHisCourse"),
                        # 他的课程
                        url(r'^getHisClass/', 'website.api.course.views.app_user_course',
                            name="getHisClass"),
                        # 推荐课程
                        url(r'^getExcellentRecom/', 'website.api.course.views.app_recommend_course',
                            name="getExcellentRecom"),
                        # 职业课程详情
                        url(r'^getCareerDetail/', 'website.api.course.views.app_career_detail',
                            name="getCareerDetail"),
                        # 支付界面
                        url(r'^getPaymentInfo/', 'website.api.course.views.app_pay',
                            name="app_pay"),
                        # 提交支付
                        url(r'^submitPayment/', 'website.api.course.views.app_submit_pay',
                            name="submit_pay"),
                        # 提交跳转到项目页的申请(for 手机端)
                        url(r'^snap_project_upload/', 'website.api.course.views.app_snap_project_upload',
                            name="snap_project_upload"),
                        
                        )

# class
urlpatterns += patterns('',
                        # 我的班级
                        url(r'^getMyClass/', 'website.api.class.views.app_my_class',
                            name="getMyClass"),
                        # 班会
                        url(r'^getClassMeetingList/', 'website.api.class.views.app_meeting',
                            name="ClassMeetingList"),
                        )

# learning
urlpatterns += patterns('',
                        # 获取任务地图
                        url(r'^getTaskMap/', 'website.api.learning.views.get_task_map',
                            name="getTaskMap"),
                        # 领取任务
                        url(r'^fetchTask/', 'website.api.learning.views.fetch_task',
                            name="fetchTask"),
                        # 获取任务详细信息
                        url(r'^getTaskInfo/', 'website.api.learning.views.get_task_info',
                            name="getTaskInfo"),
                        # 解锁任务(分享成功后)
                        # url(r'^unlockTask/', 'website.api.learning.views.unlock_task',
                        #     name="unlockTask"),
                        # 获取知识点项详情
                        url(r'^getItemDetail/', 'website.api.learning.views.get_item_detail',
                            name="getItemDetail"),
                        # 获取知识点项详情
                        url(r'^getTaskProject/', 'website.api.learning.views.get_task_project',
                            name="getTaskProject"),
                        # 提交测验答案
                        url(r'^submitExamAnswer/', 'website.api.learning.views.submit_exam_answer',
                            name="submitExamAnswer"),
                        # 他的任务记录(学员)
                        url(r'^getHisTask/', 'website.api.learning.views.get_his_task',
                            name="getHisTask"),
                        # 他的任务记录(学员)
                        url(r'^updateLesson/', 'website.api.learning.views.update_lesson',
                            name="UpdateLesson"),
                        )

# one to one
urlpatterns += patterns('',
                        # 学习建议列表
                        url(r'^createQuestionService/', 'website.api.onevone.views.app_create_coach_info',
                            name="createQuestionService"),
                        # 学习建议列表
                        url(r'^getOneVOneList/', 'website.api.onevone.views.app_get_coach_list',
                            name="getOneVOneList"),
                        # 学习建议详情
                        url(r'^getOneVOneDetail/', 'website.api.onevone.views.coach_detail',
                            name="getOneVOneDetail"),
                        # 学习建议回复
                        url(r'^replyOneVOneService/', 'website.api.onevone.views.app_reply_coach_info',
                            name="replyOneVOneService"),
                        # 学习建议回复上传图片
                        url(r'^uploadImages/', 'website.api.onevone.views.app_student_service_upload',
                            name="uploadImages"),
                        # 预约发送短信
                        url(r'^sendVerifyCode/', 'website.api.onevone.views.app_student_meeting_send_sms',
                            name="sendVerifyCode"),
                        # 项目辅导详情
                        url(r'^getTaskProjectDetail/', 'website.api.onevone.views.app_student_project_coach',
                            name="getTaskProjectDetail"),
                        # 项目辅导回复
                        url(r'^replyProjectService/', 'website.api.onevone.views.app_reply_student_project_coach',
                            name="replyProjectService"),
                        )

# 学生端约课
urlpatterns += patterns('',
                        # 班会打分
                        url(r'^evaluateMeeting/', 'apps.mz_lps4.views.score_meeting', name="evaluateMeeting"),
                        # 学生创建直播
                        url(r'^submitOneVOneMeeting/', 'website.api.onevone.views.app_student_meeting_submit',
                            name="submitOneVOneMeeting"),
                        # 获取可预约时间列表
                        url(r'^getAvailableDateList/', 'website.api.onevone.views.get_available_date_list',
                            name="getAvailableDateList"),
                        # 约课详情
                        url(r'^detailForMeeting/', 'website.api.onevone.views.student_onevone_meeting_detail',
                            name="detailForMeeting"),
                        # 取消班会
                        url(r'^cancelMeeting/', 'website.api.onevone.views.cancel_meeting', name="cancelMeeting"),
                        )

# course
urlpatterns += patterns('',
    url(r'^append_study_info/', 'website.api.business_info.views.views_append_study_info',
        name="appendStudyInfo"),
)

# wechat
urlpatterns += patterns('',
    url(r'^wechat_message_reply/', 'website.api.business_info.views.wechat_message_reply',
        name="wechat_message"),
    url(r'^wechat_click_reply/', 'website.api.business_info.views.wechat_click_reply',
        name="wechat_menu"),
)

# 教师端
urlpatterns += patterns('',
                        # 学习建议列表
                        url(r'^oneOnOneService/$', 'website.api.warning_teacher.views.one_to_one_service',
                            name="oneOnOneService"),
                        # 老师学习建议详情
                        url(r'^detailForStudyAdvice/', 'website.api.onevone.views.app_student_service_detail',
                            name="detailForStudyAdvice"),
                        # 回复学习建议
                        url(r'^replyAdvice/', 'website.api.onevone.views.app_student_submit_service_comment',
                            name="replyAdvice"),
                        # 问题详情
                        url(r'^detailForQuestion/', 'website.api.warning_teacher.views.get_question_detail',
                            name="detailForQuestion"),
                        # 回复问题
                        url(r'^replyQuestion/', 'website.api.warning_teacher.views.answer_question',
                            name="replyQuestion"),
                        # 老师查看项目
                        url(r'^detailForProject/', 'website.api.warning_teacher.views.get_project_detail',
                            name="detailForProject"),
                        # 老师登陆
                        url(r'^teacherLogin/$', 'website.api.warning_teacher.views.app_teacher_login',
                            name="teacherLogin"),
                        # 我的学生
                        url(r'^fetchAllStudents/$', 'website.api.warning_teacher.views.fetch_all_students',
                            name="fetchAllStudents"),
                        # 检查更新
                        url(r'^teacherCheckUpdate/$', 'website.api.warning_teacher.views.teacher_check_update',
                            name="teacherCheckUpdate"),
                        # 更新设备Token
                        url(r'^updateToken/$', 'website.api.warning_teacher.views.app_update_push_token',
                            name="updateToken"),
                        #  1.1 新接口--------------------------------------------------------
                        # 创建辅导信息
                        url(r'^createStudyService/$', 'website.api.warning_teacher.views.app_create_coach_info',
                            name="createStudyService"),
                        # 回复辅导
                        url(r'^replyTeacherService/$', 'website.api.warning_teacher.views.app_reply_coach_info',
                            name="replyTeacherService"),
                        # 辅导详情(非项目)
                        url(r'^detailForService/$', 'website.api.warning_teacher.views.app_get_coach_detail',
                            name="detailForService"),
                        # 辅导详情（项目）
                        url(r'^detailForProjectService/$', 'website.api.warning_teacher.views.app_teacher_project_coach',
                            name="detailForProjectService"),
                        # 辅导打分
                        url(r'^markProjectScore/$', 'website.api.warning_teacher.views.app_teacher_score_project',
                            name="markProjectScore"),
                        # 辅导列表
                        url(r'^getTeacherServiceList/$', 'website.api.warning_teacher.views.app_get_coach_list',
                            name="getTeacherServiceList"),

                        # 历史记录
                        url(r'^getServiceHistory/$', 'website.api.warning_teacher.views.service_history',
                            name="getServiceHistory"),
                        # 历史记录详情(非项目)
                        url(r'^getTeacherHistoryDetail/$', 'website.api.warning_teacher.views.app_get_history_detail',
                            name="getTeacherHistoryDetail"),
                        # 历史记录详情
                        url(r'^getProjectHistoryDetail/$', 'website.api.warning_teacher.views.app_get_history_detail',
                            name="getTeacherHistoryDetail"),
                        # 约课列表
                        url(r'^bookLiveMeeting/', 'website.api.warning_teacher.views.get_meeting_list',
                            name="bookLiveMeeting"),
                        # 约课详情
                        url(r'^detailForLiveMeeting/', 'website.api.warning_teacher.views.get_meeting_detail',
                            name="detailForLiveMeeting"),
                        # 插入老师考勤
                        url(r'^insertAttendance/$', 'mz_usercenter.teacher.views.ajax_insert_onevone_attendance',
                            name='insertAttendance'),
                        )


