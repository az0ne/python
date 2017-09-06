# -*- coding: utf-8 -*-
import unittest
from mz_lps2.calc_view import *
from mz_lps2.models import *
from mz_user.forms import UserProfile
from mz_lps.models import *
from datetime import datetime
import random

def clear_course_user_task(user, user_class):
    try:
        CourseUserTask.objects.filter(user=user, user_class=user_class).delete()
    except:
        assert False

def update_course_user_task(user, user_class, total_study_time):
    try:
        course_user_task_set = CourseUserTask.objects.filter(user=user, user_class=user_class)\
                                            .order_by('-id')[:1]
        course_user_task_set[0].total_study_time=total_study_time
        course_user_task_set[0].save()
    except:
        assert False

class TestPlanForNextweek(unittest.TestCase):
    def setUp(self):
        # 测试条件
        user_id = 71
        class_id = 11
        self.times = 2
        try:
            self.user_class = Class.objects.get(id=class_id)
            self.user = UserProfile.objects.get(id=user_id)
        except:
            assert False

        # 先清空测试表
        clear_course_user_task(user=self.user, user_class=self.user_class)

    def tearDown(self):
        assert True

    def test_plan_for_nextweek(self):
        for i in xrange(self.times):
            learning_plans, learning_hours = plan_for_nextweek(self.user, self.user_class)
            total_study_time = random.randint(0, 20)
            update_course_user_task(self.user, self.user_class, total_study_time)
            print "本周学习计划：", learning_plans
            print "本周计划学时：", learning_hours
