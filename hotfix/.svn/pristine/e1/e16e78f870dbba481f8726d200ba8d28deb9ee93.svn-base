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
def clear_course_user_task(user_class):
    try:
        CourseUserTask.objects.filter(user=user_class).delete()
    except:
        assert False

def clear_stustatus_user_task(teacher):
    try:
        StuStatusUserTask.objects.filter(user=teacher).delete()
    except:
        assert False

def calc_kpi(user_id, user_class):
    try:
        user = UserProfile.objects.get(id=user_id)
        course_user_task = CourseUserTask.objects.filter(user=user,\
                                    user_class=user_class).order_by('-id')[:1]
    except:
        assert False
    if course_user_task:
        kpi = course_user_task[0].real_study_time < course_user_task[0].plan_study_time\
                    and (1.0*course_user_task[0].real_study_time/course_user_task[0].plan_study_time)\
                    or (1.0*course_user_task[0].total_study_time/course_user_task[0].plan_study_time)
    else:
        kpi = 0
    return kpi

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
        clear_stustatus_user_task(teacher=self.user_class.teacher)
        # 生成随机测试数据
        for each in self.class_stu_set:
            real_study_time = random.randint(0, 15)
            real_study_time_ext = random.randint(0, 10)
            total_study_time = real_study_time + real_study_time_ext
            create_course_user_task(user=each.user, user_class=each.student_class, \
                                real_study_time=real_study_time,\
                                real_study_time_ext=real_study_time_ext,\
                                total_study_time=total_study_time)
    def tearDown(self):
        pass

    def test_get_risk_in_week(self):
        risk_list = get_risk_in_week([self.user_class])
        print "进度落后学员名单："
        for uid in risk_list[str(self.user_class.id)]:
            print "user id:", uid, "kpi:", calc_kpi(uid, self.user_class)
