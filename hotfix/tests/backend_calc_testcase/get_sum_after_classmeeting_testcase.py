# -*- coding: utf-8 -*-
import unittest
from mz_lps2.models import *
from mz_lps2.calc_view import *
from mz_lps.models import *
import random

def clear_class_meeting_task(user_class):
    try:
        ClassMeetingTask.objects.filter(user_class=user_class).delete()
    except:
        assert False


class TestCalcInClass(unittest.TestCase):
    def setUp(self):
        # 测试条件
        class_id = 11
        try:
            self.user_class = Class.objects.get(id=class_id)
        except:
            assert False

        # 先清空测试表
        clear_class_meeting_task(user_class=self.user_class)

    def tearDown(self):
        pass

    def test_get_risk_in_week(self):
        get_sum_after_classmeeting([self.user_class])
