#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models
from django.conf import settings

from ..mz_common import mz_lps
import lesson.Lesson as Lesson


Class = mz_lps.Class
# 章节讨论 models


class Discuss(models.Model):
    content = models.TextField("讨论内容")
    parent_id = models.IntegerField("父讨论ID", blank=True, null=True)
    date_publish = models.DateTimeField("发布时间", auto_now_add=True)

    lesson = models.ForeignKey(Lesson, verbose_name="章节")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="用户")
    user_class = models.ForeignKey(
        Class, verbose_name="班级", null=True, blank=True)

    class Meta:
        verbose_name = "课程讨论"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)
