# -*- coding: utf-8 -*-
import unittest
from mz_lps2.models import *
from mz_lps2.calc_view import *
from mz_lps.models import *
from mz_user.forms import UserProfile
import random

# 创建测试表
def create_class_meeting_task(user_class):
    try:
        class_meeting_task = ClassMeetingTask.objects.create(user_class=user_class,\
                                                             status=1)
    except:
        assert False
    return class_meeting_task

def create_userquality_modelitems(user, week, quality_type,  subject_score=-1, score=-1):
    try:
        userquality_modelitems = UserQualityModelItems.objects.create(user=user,\
                                                quality_type=quality_type, week=week,\
                                                subject_score=subject_score,
                                                score=score)
    except:
        assert False
    return userquality_modelitems

def create_course_user_task(user, user_class, real_study_time, real_study_time_ext, \
                        total_study_time, comment_count, liveroom_comment_count, week):
    try:
        course_user_task = CourseUserTask.objects.create(user=user, user_class=user_class,\
                                                          real_study_time=real_study_time,\
                                                          real_study_time_ext=real_study_time_ext,\
                                                          total_study_time=total_study_time,\
                                                          comment_count=comment_count, \
                                                          liveroom_comment_count=liveroom_comment_count,\
                                                          week=week)
    except:
        assert False
    return course_user_task

# 清空测试表
def clear_course_user_task(user, user_class):
    try:
        CourseUserTask.objects.filter(user=user, user_class=user_class).delete()
    except:
        assert False

def clear_userquality_modelitems(user):
    try:
        UserQualityModelItems.objects.filter(user=user).delete()
    except:
        assert False

def clear_class_meeting_task(user_class):
    try:
        ClassMeetingTask.objects.filter(user_class=user_class).delete()
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
        clear_userquality_modelitems(user=self.user)
        clear_class_meeting_task(user_class=self.user_class)

        # 生成随机测试数据
        pre_class_meeting_task = create_class_meeting_task(self.user_class)
        cur_class_meeting_task = create_class_meeting_task(self.user_class)
        # 沟通能力
        subject_score = random.randint(50, 100)
        create_userquality_modelitems(user=self.user, week=pre_class_meeting_task,\
                                    subject_score=subject_score, score=subject_score, quality_type=2)
        create_userquality_modelitems(user=self.user, week=cur_class_meeting_task,\
                                    subject_score=random.randint(50, 100), quality_type=2)
        # 执行力
        create_userquality_modelitems(user=self.user, week=pre_class_meeting_task,\
                                    score=random.randint(50, 100), quality_type=1)
        # 主动性
        create_userquality_modelitems(user=self.user, week=pre_class_meeting_task,\
                                    score=random.randint(50, 100), quality_type=3)

        real_study_time = random.randint(5, 15)
        real_study_time_ext = random.randint(0, 10)
        total_study_time = real_study_time + real_study_time_ext
        comment_count = random.randint(0, 10)
        liveroom_comment_count = random.randint(0, 10)
        create_course_user_task(user=self.user, user_class=self.user_class,\
                                    real_study_time=real_study_time,\
                                    real_study_time_ext=real_study_time_ext,\
                                    total_study_time=total_study_time,\
                                    comment_count=comment_count,\
                                    liveroom_comment_count=liveroom_comment_count,\
                                    week=pre_class_meeting_task)
        # 模拟建立下周任务，关联本周班会
        create_course_user_task(user=self.user, user_class=self.user_class,\
                                    real_study_time=real_study_time,\
                                    real_study_time_ext=real_study_time_ext,\
                                    total_study_time=total_study_time,\
                                    comment_count=comment_count,\
                                    liveroom_comment_count=liveroom_comment_count,\
                                    week=cur_class_meeting_task)

    def tearDown(self):
        pass

    def test_calc_student_quality(self):
        calc_single_student_quality(self.user, self.user_class)
