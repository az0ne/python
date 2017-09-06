# -*- coding: utf-8 -*-
#from mz_service.views import *
from mz_lps2.calc_view import *
from mz_lps.models import *
import unittest
import json

class TestRequest:
    REQUEST={"courseId":"","studentId":"","UUID":"","userId":""}

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        #self.seq = range(10)
        pass

    def tearDown(self):
        pass

    def test_update_score(self):
        user = UserProfile.objects.get(pk=302)
        course = Course.objects.get(pk = 4)
        update_study_point_score_calc(user, course = course, lesson_id=2, update_type=1)

    def test_getCourseProgress(self):
        class1 = Class.objects.get(pk= 27)
        calc_liveroom_info(class1)


    # def test_getCourseProgress1(self):
    #     request=TestRequest()
    #     #给Request赋值
    #     request.REQUEST["courseId"]=16
    #     request.REQUEST["UUID"]="5bc0d490a55b40c8a6f41a6f81ce793d"
    #     request.REQUEST["studentId"]=7
    #     request.REQUEST["userId"]=3
    #     #传递request给测试目标
    #     res=getCourseProgress(request)
    #     #得到返回值
    #     js=json.loads(res.content)
    #     #判断返回值
    #     self.assertEqual(js["message"],"数据加载成功")
    #     self.assertEqual(js["data"].get("score"),0)
    #     self.assertEqual(len(js["data"].get("list")),5)
