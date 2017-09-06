# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from fps_interface.models import Article, CourseAsk, Discuss
from mz_lps.models import ClassStudents, CourseScore, ProjectRecord
from mz_lps2.models import CourseUserTask
from mz_user.models import ClassStudentDynamic, UserProfile
import logging

logger = logging.getLogger('mz_user.signal_view')


def _create_dynamic(**kwargs):
    try:
        __create_dynamic(**kwargs)
        __create_course_score_dynamic(**kwargs)
    except Exception, e:
        print e
        logger.error(e)


def __create_dynamic(**kwargs):
    '''创建动态'''
    # kwargs: "instance", "raw", "created", "using", "update_fields"
    sender = kwargs.get('sender')
    ins = kwargs.get('instance')
    created = kwargs.get('created')
    if sender == ClassStudents and created:
        params = dict(user=ins.user, type=1,
                      obj_id=ins.student_class.id)
        ClassStudentDynamic.objects.get_or_create(**params)

    # elif sender == CourseUserTask:
    #     if ins.plan_study_time <= ins.real_study_time:
    #         params = dict(user=ins.user, type=2, obj_id=ins.week.id)
    #         ClassStudentDynamic.objects.get_or_create(**params)
    #
    # elif sender == CourseScore:
    #     if ins.project_score:
    #         params = dict(user=ins.user, type=3, obj_id=ins.course.id)
    #         ClassStudentDynamic.objects.get_or_create(**params)

    elif sender == ProjectRecord and created:
        params = dict(user=ins.student, type=5, obj_id=ins.project.relation_id)
        ClassStudentDynamic.objects.create(**params)


def __create_user_task_dynamic(**kwargs):
    '''创建动态'''
    # kwargs: "instance", "raw", "created", "using", "update_fields"
    sender = kwargs.get('sender')
    ins = kwargs.get('instance')
    created = kwargs.get('created')
    if sender == CourseUserTask:
        if ins.plan_study_time <= ins.real_study_time:
            params = dict(user=ins.user, type=2, obj_id=ins.week.id)
            ClassStudentDynamic.objects.get_or_create(**params)

def __create_course_score_dynamic(**kwargs):
    '''创建动态'''
    # kwargs: "instance", "raw", "created", "using", "update_fields"
    sender = kwargs.get('sender')
    ins = kwargs.get('instance')
    created = kwargs.get('created')
    if sender == CourseScore:
        if ins.project_score:
            params = dict(user=ins.user, type=3, obj_id=ins.course.id)
            ClassStudentDynamic.objects.get_or_create(**params)
    # elif sender == Discuss and created:
    #     if ins.type == 1:
    #         dis_user = UserProfile.objects.get(id=ins.user)
    #         article = Article.objects.get(id=ins.relate_id)
    #         articke_user = UserProfile.objects.get(id=article.user)
    #         class_students = ClassStudents.objects.filter(user=articke_user)
    #         if class_students:
    #             for clazz in class_students:
    #                 if clazz.filter(user=dis_user).exists():
    #                     params = dict(user=articke_user, type=4, obj_id=ins.relate_id)
    #                     ClassStudentDynamic.objects.create(**params)
    #
    #     if ins.type == 3:
    #         dis_user = UserProfile.objects.get(id=ins.user)
    #         ask = CourseAsk.objects.get(id=ins.relate_id)
    #         articke_user = UserProfile.objects.get(id=ask.user)
    #         class_students = ClassStudents.objects.filter(user=articke_user)
    #         if class_students:
    #             for clazz in class_students:
    #                 if clazz.filter(user=dis_user).exists():
    #                     params = dict(user=articke_user, type=6, obj_id=ins.lesson_id)
    #                     ClassStudentDynamic.objects.create(**params)

    # elif sender == Article and created:
    #     user = UserProfile.objects.get(id=ins.user)
    #     params = dict(user=user, type=7, obj_id=ins.id)
    #     ClassStudentDynamic.objects.get_or_create(**params)

# LPS
# 1.xxx加入了xxxx职业课程（还需展示班级号）：职业课程点击跳转到对应的课程页
post_save.connect(_create_dynamic, sender=ClassStudents)
# 2.xxx本周学习任务已经完成了100%啦！：所有本周学习任务大于等于100%的学员，都这样显示
# post_save.connect(__create_user_task_dynamic, sender=CourseUserTask)
# 3.xxx的课程作业《xxxx》被老师批改啦！：课程点击跳转到对应的课程播放页
# post_save.connect(__create_course_score_dynamic, sender=CourseScore)
# 5.xxx提交了课程：《xxxx》的项目实战作业！：课程点击跳转到对应的课程播放页
# post_save.connect(_create_dynamic, sender=ProjectRecord)

# FPS
# 4.xxx发表的文章：xxxx被同班同学回复啦！：文章点击跳转到对应文章详情页
# 6.xxx在课程《xxxx》下的提问被同班同学回复啦！：课程点击跳转到对应的课程播放页
# post_save.connect(_create_dynamic, sender=Discuss)
# 7.xxx发表了文章《xxxx》：文章点击跳转到对应文章详情页
# post_save.connect(_create_dynamic, sender=Article)
