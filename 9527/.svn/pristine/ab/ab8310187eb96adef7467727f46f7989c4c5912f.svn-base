#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns("mz_course",

                       # 专业方向
                       url(r'^careerCatagory/list/$', "careerCatagory.careerCatagory_list", name="careerCatagory_list"),
                       url(r'^careerCatagory/edit/$', "careerCatagory.careerCatagory_edit", name="careerCatagory_edit"),
                       url(r'^careerCatagory/save/$', "careerCatagory.careerCatagory_save", name="careerCatagory_save"),

                       # 对象关系
                       url(r'^objTagRelation/list/$', "objTagRelation.obj_tag_relation_list",
                           name="objTagRelation_list"),
                       url(r'^objTagRelation/edit/$', "objTagRelation.obj_tag_relation_edit",
                           name="objTagRelation_edit"),
                       url(r'^objTagRelation/save/$', "objTagRelation.obj_tag_relation_save",
                           name="objTagRelation_save"),

                       # 职业课程介绍
                       url(r'^careerIntroduce/list/$', "careerIntroduce.career_introduce_list",
                           name="careerIntroduce_list"),
                       url(r'^careerIntroduce/edit/$', "careerIntroduce.career_introduce_all_edit",
                           name="careerIntroduce_edit"),  # 查看职业课程相关信息
                       url(r'^careerIntroduce/info/edit/$', "careerIntroduce.career_introduce_edit",
                           name="careerIntroduceInfo_edit"),
                       url(r'^careerIntroduce/info/save/$', "careerIntroduce.career_introduce_info_save",
                           name="careerIntroduceInfo_update"),  # 更新职业课程基本介绍信息
                       url(r'^careerIntroduce/story/save/$', 'careerIntroduce.career_introduce_story_save',
                           name='careerIntroduceStory_update'),  # 更新学员成功故事
                       url(r'^careerIntroduce/discuss/save/$', 'careerIntroduce.career_introduce_discuss_save',
                           name='careerIntroduceDiscuss_update'),  # 更新评论

                       # 职业课程老师介绍
                       url(r'^careerIntroduce/teacher/edit/$', "careerIntroduceTeacher.teacher_edit",
                           name="careerIntroduce_teacher_edit"),
                       url(r'^careerIntroduce/teacher/save/$', "careerIntroduceTeacher.teacher_save",
                           name="careerIntroduce_teacher_save"),
                       url(r'^careerIntroduce/teacher/list/$', "careerIntroduceTeacher.teacher_list",
                           name="careerIntroduce_teacher_list"),
                       # 职业课程学生介绍
                       url(r'^careerIntroduce/student/edit/$', "careerIntroduceStudent.student_edit",
                           name="careerIntroduce_student_edit"),
                       url(r'^careerIntroduce/student/save/$', "careerIntroduceStudent.student_save",
                           name="careerIntroduce_student_save"),
                       url(r'^careerIntroduce/student/list/$', "careerIntroduceStudent.student_list",
                           name="careerIntroduce_student_list"),

                       # 职业课程企业介绍
                       url(r'^careerIntroduce/enterprise/edit/$', "careerIntroduceEnterprise.enterprise_edit",
                           name="careerIntroduce_enterprise_edit"),
                       url(r'^careerIntroduce/enterprise/save/$', "careerIntroduceEnterprise.enterprise_save",
                           name="careerIntroduce_enterprise_save"),
                       url(r'^careerIntroduce/enterprise/list/$', "careerIntroduceEnterprise.enterprise_list",
                           name="careerIntroduce_enterprise_list"),

                       # 职业课程职位介绍
                       url(r'^careerIntroduce/duty/edit/$', "careerIntroduceDuty.duty_edit",
                           name="careerIntroduce_duty_edit"),
                       url(r'^careerIntroduce/duty/save/$', "careerIntroduceDuty.duty_save",
                           name="careerIntroduce_duty_save"),
                       url(r'^careerIntroduce/duty/list/$', "careerIntroduceDuty.duty_list",
                           name="careerIntroduce_duty_list"),

                       # 任务描述
                       url(r'^task/taskDesc/edit/$', "taskDesc.task_desc_edit", name="taskDesc_edit"),
                       url(r'^task/taskDesc/save/$', "taskDesc.task_desc_save", name="taskDesc_save"),
                       url(r'^task/taskDesc/list/$', "taskDesc.task_desc_list", name="taskDesc_list"),

                       # 任务与相关文章
                       url(r'^task/taskArticle/edit/$', "taskArticle.task_article_edit", name="taskArticle_edit"),
                       url(r'^task/taskArticle/save/$', "taskArticle.task_article_save", name="taskArticle_save"),
                       url(r'^task/taskArticle/list/$', "taskArticle.task_article_list", name="taskArticle_list"),

                       # 任务的优秀作品展
                       url(r'^task/taskExcellentWorks/edit/$', "taskExcellentWorks.task_excellent_works_edit",
                           name="taskExcellentWorks_edit"),
                       url(r'^task/taskExcellentWorks/save/$', "taskExcellentWorks.task_excellent_works_save",
                           name="taskExcellentWorks_save"),
                       url(r'^task/taskExcellentWorks/list/$', "taskExcellentWorks.task_excellent_works_list",
                           name="taskExcellentWorks_list"),

                       # 问卷编辑详情
                       url(r'^questionnaire/list/$', "questionnaire_list.questionnaire_item_list",
                           name="questionnaire_list"),
                       url(r'^questionnaire/edit/$', "questionnaire_list.questionnaire_item_add",
                           name="questionnaire_edit"),
                       url(r'^questionnaire/save/$', "questionnaire_list.questionnaire_item_save",
                           name="questionnaire_save"),

                       # 问卷查询
                       url(r'^questionnairequery/list/$', "questionnairequery.questionnairequery_list",
                           name="questionnairequery"),
                       url(r'^questionnairequery/edit/$', "questionnairequery.questionnairequery_edit",
                           name="questionnairedit"),


                       # 小课程seo
                       url(r'^courseinfo/list/$', "course_info.courseinfo_list", name="courselist"),
                       # url(r'^courseinfo/info/$', "course_info.courseinfo_info", name="courseinfo"),
                       url(r'^courseinfo/edit/$', "course_info.courseinfo_edit", name="courseedit"),
                       url(r'^courseinfo/save/$', "course_info.courseinfo_save", name="coursesave"),

                       # 首页课程排序
                       url(r'^homepagecourse/list/$', "mz_homepagecourse.homepagecourse_list",
                           name="homepagecourse_list"),
                       url(r'^homepagecourse/edit/$', "mz_homepagecourse.homepagecourse_edit",
                           name="homepagecourse_edit"),
                       url(r'^homepagecourse/save/$', "mz_homepagecourse.homepagecourse_save",
                           name="homepagecourse_save"),

                       url(r'^record/user_career_list/$', "record_views.user_career_list", name="user_career_list"),

                       # 搜索页职业课程广告
                       # url(r'^careerAd/list/$', "careerAd.career_ad_list", name="careerAd_list"),
                       # url(r'^careerAd/edit/$', "careerAd.career_ad_edit", name="careerAd_edit"),
                       # url(r'^careerAd/save/$', "careerAd.career_ad_save", name="careerAd_save"),
                       # ajax验证课程ID是否存在
                       # url(r'^careerAd/validateUniqueId/ajax/$', "careerAd.validate_unique_id",
                       #     name="validate_unique_career_ad_id"),

                       # 职业课程发布会议日期
                       url(r'^careerPMD/list/$', "careerPublicMeetingDate.career_public_meeting_date_list", name="careerPMD_list"),
                       # 直播班会管理
                       url(r'^livemeeting/list/$', "courseLiveMeeting.liveMeeting_list", name="liveMeeting_list"),
                       url(r'^livemeeting/show/$', "courseLiveMeeting.liveMeeting_show", name="liveMeeting_show"),
                       )

                       
urlpatterns += patterns("mz_course.careerPublicMeeting",
                        # 职业课程公开课
                        url(r'^publicMeeting/list/$', "career_public_meeting_list",
                            name="public_meeting_list"),
                        url(r'^publicMeeting/edit/$', "career_public_meeting_edit",
                            name="public_meeting_edit"),
                        url(r'^publicMeeting/save/$', "career_public_meeting_save",
                            name="public_meeting_save"),
                        )
