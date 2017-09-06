# -*- coding: UTF-8 -*-
from django.test import TestCase
import datetime

from maiziserver.db.api.activity.activity import *
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziserver.settings")


class DbapiActivityTestCase(TestCase):
    def setUp(self):
        pass

    def test_assert_equal(self):
        self.assertEqual(1, 1, 'pass the test')

    def test_update_student_activity_video_num(self):
        """
        failed test...
        :return:
        """
        t = datetime.date(2017, 7, 6)
        student_account = '18782038849'
        update_student_activity_video_num(student_account, t, 8)
        self.assertEqual(1, 1)

    def test_insert_watched_videos(self):
        """
        failed test
        :return:
        """
        t = datetime.date(2017, 7, 6)
        _insert_watched_videos(t)

    def test_list_finish_exercises(self):
        """
        failed test
        :return:
        """
        t = datetime.date(2017, 7, 6)
        list_finish_exercises(t)

    def test_update_student_activity_exceicse_num(self):
        """
        passed test
        :return:
        """
        t = datetime.date(2017, 7, 6)
        student_account = '18081152062'
        update_student_activity_exceicse_num(student_account, t, 8)

    def test_insert_finished_test(self):
        """
        failed test
        :return:
        """
        t = datetime.date(2017, 7, 6)
        _insert_finished_test(t)

    def test_list_finish_task(self):
        """
        failed test
        :return:
        """
        t = datetime.date(2017, 7, 6)
        list_finish_task(t)

    def test_insert_finish_task_ball(self):
        """

        :return:
        """
        t = datetime.date(2017, 7, 6)
        insert_finish_task_ball(t)

    def test_insert_booking_cources(self):
        t = datetime.date(2017, 7, 6)
        insert_booking_cources(t)

    def test_insert_ask_question_num(self):
        t = datetime.date(2017, 7, 6)
        insert_ask_question_num(t)

    def test_list_active_student(self):
        """
        测试查询数据
        :return:
        """
        t = datetime.datetime(2017, 7, 6)
        a = list_active_monitor(t)

        print a.result()['result']
        self.assertEqual(False, a.is_error())

    def test_update_student_active_monitor_total_score_data(self):
        """
        更新总成绩
        :return:
        """
        a = update_student_active_monitor_total_score_data(1, 8.8)

        self.assertEqual(False, a.is_error())

    def test_insert_total_point_daily(self):
        """

        :return:
        """
        t = datetime.datetime(2017, 7, 6)
        result = insert_total_point_daily(t)

        self.assertEqual(True, result)

    def test_daily_sms_notify(self):
        """
        测试短信的发送
        :return:
        """
        t = datetime.datetime(2017, 7, 6)

        # daily_sms_notify()

        self.assertEqual(1, 1)

    def test_get_total_active_point_by_student_id(self):
        """
        测试学生的总分
        :return:
        """

        result = get_total_active_point_by_student_id(4)

        if result.is_error():
            print 'sql errror'

        else:
            print result.result()['result']



    def test_get_active_point_by_month(self):
        """
        测试每月学分的获取
        :return:
        """

        result = get_active_point_by_month(4, 2017, 7)
        print result


