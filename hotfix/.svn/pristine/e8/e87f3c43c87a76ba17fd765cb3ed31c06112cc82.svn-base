# -*- coding: utf-8 -*-
import unittest
from mz_lps2.models import *
from mz_lps2.calc_view import *
from mz_lps.models import *
from mz_user.forms import UserProfile
import random

# 创建测试表
def create_course_user_task(user, user_class, real_study_time, real_study_time_ext, total_study_time):
    try:
        course_user_task = CourseUserTask.objects.create(user=user, user_class=user_class,\
                                                          real_study_time=real_study_time,\
                                                          real_study_time_ext=real_study_time_ext,\
                                                          total_study_time=total_study_time)
    except:
        assert False
    return course_user_task

# 清空测试表
def clear_course_user_task(user, user_class):
    try:
        CourseUserTask.objects.filter(user=user, user_class=user_class).delete()
    except:
        assert False

class TestCalcInClass(unittest.TestCase):
    def setUp(self):
        # 测试条件
        user_id = 71
        class_id = 11
        try:
            self.user_class = Class.objects.get(id=class_id)
            self.user = UserProfile.objects.get(id=user_id)
        except:
            assert False

        # 先清空测试表
        clear_course_user_task(user=self.user, user_class=self.user_class)
        # 生成随机测试数据
        for i in xrange(2):
            real_study_time = random.randint(5, 15)
            real_study_time_ext = random.randint(0, 10)
            total_study_time = real_study_time + real_study_time_ext
            create_course_user_task(user=self.user, user_class=self.user_class, \
                        real_study_time=real_study_time, real_study_time_ext=real_study_time_ext,\
                        total_study_time=total_study_time)

    def tearDown(self):
        pass

    def test_calc_plan_graduate_time(self):
        remaining_days = calc_plan_graduate_time(self.user, self.user_class)
        print "user id:", self.user.id, "离毕业还有", remaining_days, "天"
