#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models


class Log(models.Model):
    log_types = (
        ('1', '班级管理'),
    )

    class Meta:
        verbose_name = u'日志'
        verbose_name_plural = verbose_name
    userA = models.IntegerField(u"用户A")
    userB = models.IntegerField(u"用户B", blank=True, null=True)
    log_type = models.CharField(u'类型', choices=log_types, max_length=1)
    log_id = models.IntegerField(u'动作id', blank=True, null=True)
    log_content = models.TextField(u'消息内容', blank=True, null=True)
    date_action = models.DateTimeField(u'添加日期', auto_now_add=True)

    def __unicode__(self):
        return str(self.id)
