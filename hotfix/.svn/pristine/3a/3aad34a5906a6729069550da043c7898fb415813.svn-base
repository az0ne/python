#!/usr/bin/env python
# -*- coding: utf8 -*-


def gene_fake(keys, *val):
    if len(val) > 1:
        return map(lambda v: dict(zip(keys, v)), val)
    return dict(zip(keys, val[0]))


def deb_print(**kwargs):
    print '-' * 30
    print '\n'.join(['{}:{}'.format(k, v) for k, v in kwargs.iteritems()])
    print '-' * 30


def null_func(*args, **kwargs):
    pass


deb_print = null_func


# debug fake data creator
# def deb_get_one_course():
#     k = ("id", "name", "image", "description", "is_active", "date_publish", "need_days","need_days_base",
# "student_count",
# "favorite_count",
# "click_count",
# "is_novice",
# "is_click",
# "index",
# "teacher_id",
# "is_homeshow",
# "course_status",
# "score_ava",
# "need_pay")
#     v = ('1', '嵌入式驱动开发环境搭建初级', 'course/2015/07/1.1嵌入式驱动开发环境搭建初级_btlDIHY.png', '嵌入式系统的开发往往和PC上的开发不一样，那么本套课程将带着大家看看嵌入式开发中一些常用软件环境和服务的搭建情况。', '1', '2015-03-26 16:32:58', '7', '3', '4216', '214', '62669', '1', '1', '1', '4', '1', '1', '4.90107526881378', '0')

#     c = debug_tool.gene_fake(k, v)
#     c = course.Course(c)
#     return deb_get_all_course()[0]


# def deb_get_all_course():
#     k = ("id", "name", "image", "description", "is_active", "date_publish", "need_days","need_days_base",
#                 "student_count",
#                 "favorite_count",
#                 "click_count",
#                 "is_novice",
#                 "is_click",
#                 "index",
#                 "teacher_id",
#                 "is_homeshow",
#                 "course_status",
#                 "score_ava",
#                 "need_pay")
#     v1 = ('1', '嵌入式驱动开发环境搭建初级', 'course/2015/07/1.1嵌入式驱动开发环境搭建初级_btlDIHY.png', '嵌入式系统的开发往往和PC上的开发不一样，那么本套课程将带着大家看看嵌入式开发中一些常用软件环境和服务的搭建情况。', '1', '2015-03-26 16:32:58', '7', '3', '4216', '214', '62669', '1', '1', '1', '4', '1', '1', '4.90107526881378', '0')
#     v2 = ('2', '嵌入式驱动开发环境搭建初级1', 'course/2016/07/1.1嵌入式驱动开发环境搭建初级_btlDIHY.png', '嵌入式系统的开发往往和PC上的开发不一样，那么本套课程将带着大家看看嵌入式开发中一些常用软件环境和服务的搭建情况。', '1', '2015-03-26 16:32:58', '7', '3', '4216', '214', '62669', '1', '1', '1', '4', '1', '1', '4.90107526881378', '0')
#     cs = debug_tool.gene_fake(k, v1, v2)
#     cs = [course.Course(i) for i in cs]
#     return cs


# def deb_get_one_lesson():
#     return deb_get_all_lesson()[0]


# def deb_get_all_lesson():
#     k = ('id', 'name', 'video_url', 'video_length', 'play_count','share_count', 'index', 'is_popup', 'course_id', 'seo_description', 'seo_keyword', 'seo_title', 'have_homework', 'code_exercise_type')
#     v1 = ('1', 'Vmware软件介绍', 'http://ocs.maiziedu.com/embedded_env_1.mp4', '731', '26668', '0', '1', '0', '1', '本章节讲述Vmware使用教程，Vmware下载以及Vmware的初始环境搭建方法。', 'Vmware，Vmware使用教程，Vmware11，Vmware详解，Vmware配置', 'Vmware_Vmware使用教程', '1', '0')
#     v2 = ('2', 'Java是什么', 'http://ocs.maiziedu.com/candy4java_1_1.mp4', '641', '66278', '0', '1', '0', '4', 'Java语言入门基础讲解，本章节从Java教程的基础理解到进阶应用逐一讲解。', 'Java，Java教程，Java视频教程，Java语言入门，Java开发入门', 'Java视频教程_Java语言入门基础', '1', '0')

#     ls = debug_tool.gene_fake(k, v1, v2)
#     ls = [lesson.Lesson(i) for i in ls]
#     return ls


# def deb_get_one_teacher():
#     return deb_get_all_teacher()[0]


# def deb_get_all_teacher():
#     k = ("id","password","last_login","is_superuser","username","first_name","last_name","email","is_staff","is_active","date_joined","nick_name","avatar_url","avatar_middle_thumbnall","avatar_small_thumbnall","qq","mobile","valid_email","valid_mobile","company_name","position","description","city_id","register_way_id","uid","index","uuid","token","avatar_alt","study_goal","study_base","study_base_opt_id","study_goal_opt_id","is_disabled","teach_feature","teacher_photo","teacher_video","invitation_code","address","birthday","degree","gender","real_name","graduate_institution","id_number","in_service","intention_job_city","service_year","industry","to_industry")
#     v1 = ('44137', 'pbkdf2_sha256$12000$2mOvCYmpBdUZ$Yb2TOEPyu50sd5n1sPzO0rLN8ra4zKK55fAhb1ewxXU=', '2015-10-10 14:43:28', '0', 'liwei@maiziedu.com', '', '', 'liwei@maiziedu.com', '0', '1', '2015-08-27 14:31:53', '李伟老师', 'avatar/2015/08/李伟-220.jpg', 'avatar/2015/08/李伟-104.jpg', 'avatar/2015/08/李伟-70.jpg', '718788382', None, '0', '0', '', '高级开发工程师', '8年WEB开发经验，曾就职于智联招聘，高级软件工程师，参与重构和开发了新版校园招聘系统，现在就职于益盟操盘手爱炒股事业部，负责公司项目的开发和重构。', '294', None, '36917', '999', 'fdf5c94ab4174336bb724f1b1845209f', '', '', '', '', None, None, '0', None, None, None, None, None, '1990-01-01', None, None, None, None, None, None, None, None, None, None)
#     v2 = ('44138', 'pbkdf2_sha256$12000$2mOvCYmpBdUZ$Yb2TOEPyu50sd5n1sPzO0rLN8ra4zKK55fAhb1ewxXU=', '2015-10-10 14:43:28', '0', 'liwei2@maiziedu.com', '', '', 'liwei@maiziedu.com', '0', '1', '2015-08-27 14:31:53', '李伟老师', 'avatar/2015/08/李伟-220.jpg', 'avatar/2015/08/李伟-104.jpg', 'avatar/2015/08/李伟-70.jpg', '718788382', None, '0', '0', '', '高级开发工程师', '8年WEB开发经验，曾就职于智联招聘，高级软件工程师，参与重构和开发了新版校园招聘系统，现在就职于益盟操盘手爱炒股事业部，负责公司项目的开发和重构。', '294', None, '36917', '999', 'fdf5c94ab4174336bb724f1b1845209f', '', '', '', '', None, None, '0', None, None, None, None, None, '1990-01-01', None, None, None, None, None, None, None, None, None, None)
#     lt = debug_tool.gene_fake(k, v1, v2)
#     return (user.Teacher(i) for i in lt)