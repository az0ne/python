#!/usr/bin/env python
#coding=utf-8
__author__ = 'revol'
from utils.log2mongo import L2M
from django.conf import settings

L2M.basicConfig(settings.MZ_LOG_TO_MONGODB)

class UserOpType(object):
    WATCH_VIDEO = 1
    SUBMIT_HOMEWORK = 2
    SUBMIT_PROJECT = 3
    SUBMIT_CLASS_TEST = 4
    SUBMIT_COURSE_FINAL_TEST = 5
    SUBMIT_PROJECT_TEST = 6

class UserCalcType(object):
    STUDY_TIME=1
    STUDY_POINT_AVERAGE_SCORE=2
    NEXT_WEEK_TASK=3
    REMAINING_DAYS=4
    QUALITY=5

class ClassOpType(object):
    MEETING_CREATED=1
    MEETING_OPENED=2
    MEETING_CLOSED=3

class ClassCalcType(object):
    PROGRESS_RISK=1
    STUDENT_RANKING=2

class LPS3_ClassOpType(object):
    MEETING_CREATED=1 #创建班会
    MEETING_OPENED=2  #开启帮会
    MEETING_CLOSED=3  #关闭班会
    LIVEROOM_CREATED=4  #创建直播室
    LIVEROOM_CREATED_LOG=5  #创建直播室失败

class MzL2M(L2M):
    def user_video_watched(self,class_id,student_id,course_id,lesson_id):
        self.cache(dict(task_type='3s',
                        user_op_type=UserOpType.WATCH_VIDEO,
                        class_id=class_id,
                        student_id=student_id,
                        course_id=course_id,
                        lesson_id=lesson_id))

    def user_submit_homework(self,):
        pass