# -*- coding: utf-8 -*-
import unittest
from mz_lps2.models import *
from mz_lps2.calc_view import *
from mz_lps.models import *
from mz_user.forms import UserProfile
import random

# 创建测试表
def create_course_user_task(user, user_class, study_point, ava_score):
    try:
        course_user_task = CourseUserTask.objects.create(user=user, user_class=user_class,\
                                                study_point=study_point, ava_score=ava_score)
    except:
        assert False
    return course_user_task

# 清空测试表
def clear_course_user_task(user_class):
    try:
        CourseUserTask.objects.filter(user_class=user_class).delete()
    except:
        assert False

# 计算综合分数，用于测试比较
def calc_score(user, user_class):
    try:
        course_user_task = CourseUserTask.objects.select_related()\
            .get(user=user, user_class=user_class)
    except:
        assert False
    com_score = course_user_task.study_point*0.1 + course_user_task.ava_score*0.9
    return com_score

class TestCalcInClass(unittest.TestCase):
    def setUp(self):
        # 测试条件
        class_id = 11
        try:
            self.user_class = Class.objects.get(id=class_id)
            self.class_stu_set = ClassStudents.objects.select_related()\
                .filter(student_class=self.user_class)
        except:
            assert False

        # 先清空测试表
        clear_course_user_task(user_class=self.user_class)
        # 生成随机测试数据
        for each in self.class_stu_set:
            study_point = random.randint(50, 100)
            ava_score = random.randint(50, 100)
            create_course_user_task(user=each.user, user_class=each.student_class, \
                        study_point=study_point, ava_score=ava_score)

    def tearDown(self):
        pass

    def test_rank_in_class(self):
        ranking_list = calc_rank_in_class([self.user_class])
        print "按学员综合分数进行班级排名："
        for stu, ranking in ranking_list[str(self.user_class.id)].iteritems():
            print "排名：", ranking, "user id：", stu.id, "综合分数：",\
                calc_score(stu, self.user_class)
