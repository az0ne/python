#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models


class MyMessage(models.Model):
    action_types = (
        ('1', '系统消息'),
        ('2', '课程讨论回复'),
        ('3', '论坛讨论回复'),
        ('4', '教师督促学生'),
        ('5', '粉丝'),
        ('6', '赞'),
        ('7', '@我'),
        ('8', '系统推送消息'),
        ('9', '开始新课程学习'),
        ('10', '班级排名变化'),
        ('11', '项目制作成绩'),
        ('12', '班会开始'),
        ('13', '班会缺勤'),
    )

    class Meta:
        verbose_name = u'我的消息'
        verbose_name_plural = verbose_name
    userA = models.IntegerField(u"用户A")  # 发送方，为0表示系统用户
    userB = models.IntegerField(u"用户B")  # 接收方，为0就给所有用户发送消息
    action_type = models.CharField(u'类型', choices=action_types, max_length=2)
    action_id = models.IntegerField(u'动作id', blank=True, null=True)
    action_content = models.TextField(u'消息内容', blank=True, null=True)
    date_action = models.DateTimeField(u"添加日期", auto_now_add=True)
    is_new = models.BooleanField(u'是否为最新', default=True)

    def __unicode__(self):
        return str(self.id)
