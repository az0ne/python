# -*- coding: utf-8 -*-

"""
@version: 2016/6/14
@author: Jackie
@contact: jackie@maiziedu.com
@file: interface.py
@time: 2016/6/14 10:46
@note:  ??
"""
import os
import urllib

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
import django

django.setup()
import datetime

from mz_lps3.models import ClassMeeting, LiveRoom, ClassMeetingVideo, UserTaskRecord
from django.utils.functional import cached_property
from django.core.urlresolvers import reverse
# 面费488试学的职业课程和老师的对应关系

FREE488_TEACHER = {'qrs': 4, 'android': 684, 'php': 48129, 'ios': 4130,
                   'web': 59669, 'python': 3472, 'iot': 12470, 'npm': 124580,
                   'ui': 104125, 'gd': 140355, 'op': 5}


def get_free_class_weekday(weekday_int):
    week_dict = {0: u'周一',
                 1: u'周二',
                 2: u'周三',
                 3: u'周四',
                 4: u'周五',
                 5: u'周六',
                 6: u'周天', }

    return week_dict.get(weekday_int, '')


class Free488ClassInterface:
    """
    免费488班级相关接口
    """
    CLASS_MEETING_NOT_STARTED = 0
    CLASS_MEETING_ONGOING = 2
    CLASS_MEETING_FINISHED = 1

    def __init__(self, class_id, student_name=u''):
        self.class_id = class_id
        self.student_name = student_name
        self._init()

    def _init(self):
        pass

    @cached_property
    def first_meeting(self):
        """首次班会"""
        try:
            class_meeting = ClassMeeting.objects.filter(classmeetingrelation__class_id=self.class_id)[0]
        except Exception, e:
            # print
            return {}
        return self._format_meeting(class_meeting)
        # return {'time': '20:00', 'date': '05.26', 'week': '周三',
        #         'status': self.CLASS_MEETING_ONGOING, 'countdown': 3600,
        #         'student_url': 'http://www.baidu.com/', 'student_token': 'xx887ws'}

    @cached_property
    def student_first_meeting_url(self):
        return self.first_meeting['living_student_url'] + '?' + urllib.urlencode(
            {'token': self.first_meeting['living_student_token'], 'nickname': self.student_name}
        )

    @cached_property
    def last_meeting(self):
        """后一次班会"""
        try:
            class_meeting = ClassMeeting.objects.filter(classmeetingrelation__class_id=self.class_id)[1]
        except Exception, e:
            # print
            return {}
        return self._format_meeting(class_meeting)
        # return {'time': '20:00', 'date': '05.29', 'week': '周六',
        #         'status': self.CLASS_MEETING_NOT_STARTED, 'countdown': 3600,
        #         'student_url': '', 'student_token': 'xx99ss'
        #         }

    @cached_property
    def student_last_meeting_url(self):
        return self.last_meeting['living_student_url'] + '?' + urllib.urlencode(
            {'token': self.last_meeting['living_student_token'], 'nickname': self.student_name}
        )

    @cached_property
    def latest_meeting(self):
        """当前最近的班会"""
        if self.is_not_started():
            return self.first_meeting
        elif self.is_ongoing():
            if self.first_meeting['status'] == self.CLASS_MEETING_ONGOING:
                return self.first_meeting
            else:
                return self.last_meeting
        else:
            return None

    @cached_property
    def class_time_range(self):
        """班级时间时长"""
        return 3

    @cached_property
    def class_time_range_text(self):
        return "%s-%s" % (self.first_meeting['date'], self.last_meeting['date'])

    def is_not_started(self):
        """还未开始"""
        return self.first_meeting['status'] == self.CLASS_MEETING_NOT_STARTED

    def is_ongoing(self):
        """进行中"""
        return self.first_meeting['status'] != self.CLASS_MEETING_NOT_STARTED \
               and self.last_meeting['status'] != self.CLASS_MEETING_FINISHED

    def is_finished(self):
        """已结束"""
        return self.last_meeting['status'] == self.CLASS_MEETING_FINISHED

    def get_stage(self):
        """
        获取当前阶段   项目破冰 项目进阶 项目答疑 课程推荐
        :return:1,2,3,4
        """
        if self.is_not_started():
            return 1
        if self.first_meeting['status'] != self.CLASS_MEETING_NOT_STARTED \
                and self.last_meeting['status'] == self.CLASS_MEETING_NOT_STARTED:
            return 2
        if self.last_meeting['status'] == self.CLASS_MEETING_ONGOING:
            return 3
        else:
            return 4

    def _format_meeting(self, class_meeting):
        """
        根据班会对象，格式化所以数据
        :param class_meeting:
        :return:
        """
        try:
            live_room = LiveRoom.objects.get(class_meeting=class_meeting)
            # 大班课学生端以助教身份进入
            student_url = live_room.teacher_join_url
            student_token = live_room.assistant_token
        except LiveRoom.DoesNotExist:
            student_url, student_token = ''
        try:
            play_id = ClassMeetingVideo.objects.get(class_id=self.class_id, live_id=live_room.live_id).play_id
            video_url = reverse('lps3:class_meeting_player', kwargs=dict(class_id=self.class_id, play_id=play_id))
        except Exception, e:
            # print e
            video_url = ''
        delta = class_meeting.startline - datetime.datetime.now()
        return dict(
            week=get_free_class_weekday(class_meeting.startline.weekday()),
            date=class_meeting.startline.strftime("%m.%d"),
            time=class_meeting.startline.strftime("%H:%M"),
            startline=class_meeting.startline,
            status=class_meeting.status,
            living_student_url=student_url,
            living_student_token=student_token,
            video_url=video_url,  # 录播视频地址
            countdown=delta.seconds + delta.days * 24 * 3600
        )


def unlock_free_task(student_id, class_id, stagetask_id):
    if not UserTaskRecord.objects.filter(class_id=class_id, student_id=student_id, stage_task_id=stagetask_id).exists():
        usertask = UserTaskRecord()
        usertask.class_id = class_id
        usertask.stage_task_id = stagetask_id
        usertask.student_id = student_id
        usertask.save()
        return True
    return False


if __name__ == '__main__':
    Free488ClassInterface(223).first_meeting
