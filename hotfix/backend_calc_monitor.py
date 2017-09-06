# -*- coding: utf-8 -*-
__author__ = 'hugo'

import json
import os
import django.core.handlers.wsgi
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
django.setup()

from mz_user.models import *
from mz_lps.models import *
from mz_lps2.models import *
from mz_lps2.calc_view import check_lesson_done

def check_missing_study_time(user_id, class_id):
    import pdb;pdb.set_trace()
    try:
        user = UserProfile.objects.get(id=user_id)
        user_class = Class.objects.get(id=class_id)
        async_method_set = AsyncMethod(calc_type=1)
        course_user_task_set = CourseUserTask.objects.filter(user=user, user_class=user_class)
    except Exception, e:
        print e
        return -1

    lesson_list = []
    proj_list = []
    for each_course_user_task in course_user_task_set:
        calc_log = each_course_user_task.calc_log
        if calc_log:
            lesson_log, proj_log = calc_log.split(';')
            lesson_list.extend(lesson_log.split(','))
            proj_list.extend(proj_log.split(','))

    for each_async_method in async_method_set:
        try:
            amdict = json.loads(each_async_method.methods)
        except Exception, e:
            print e
            return -1
        if amdict['student'] == user_id:
            if amdict['update_type'] == 3: # 项目制作
                if not str(amdict['examine']) in proj_list:
                    print "info----> missing proj id: %s, is_calc: %s"%(amdict['examine'], each_async_method.is_calc)
            elif amdict['update_type'] == 1: # 视频
                try:
                    lesson = Lesson.objects.get(id=amdict['lesson_id'])
                except Exception, e:
                    print e
                    continue
                if check_lesson_done(user, lesson, existing_ele='video'):
                    if not str(amdict['lesson_id']) in lesson_list:
                        print "info----> missing lesson id: %s, is_calc: %s"%(amdict['lesson_id'], each_async_method.is_calc)
            elif amdict['update_type'] == 2: # 课后作业
                try:
                    homework = Homework.objects.get(id=['examine'])
                    lesson = Lesson.objects.get(id=homework.relation_id)
                except Exception, e:
                    print e
                    continue
                if check_lesson_done(user=user, lesson=lesson, existing_ele='homework'): # 判断是否完成该章节
                    if not str(homework.relation_id) in lesson_list:
                        print "info----> missing lesson id: %s, is_calc: %s"%(homework.relation_id, each_async_method.is_calc)
            else:
                pass


if __name__ == '__main__':
    try:
        check_missing_study_time(user_id=657, class_id=21)
    except Exception, e:
        print e
