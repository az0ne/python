# -*- coding: utf-8 -*-
import unittest
from mz_lps2.models import *
from mz_lps2.calc_view import *
from mz_lps.models import *
from mz_user.forms import UserProfile
import random

# 创建测试表
def create_course_user_task(user, user_class):
    try:
        course_user_task = CourseUserTask.objects.create(user=user, user_class=user_class)
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
        create_course_user_task(user=self.user, user_class=self.user_class)

    def tearDown(self):
        pass

    def test_update_stu_study_point_score(self):
        study_point, ava_score = update_single_stu_study_point_score(user=self.user,\
                                                        user_class=self.user_class)
        print "user id:", self.user.id
        print "累计学力值:", study_point
        print "平均评测分:", ava_score
