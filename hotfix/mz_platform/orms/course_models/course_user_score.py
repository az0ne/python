#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models
from course import Course

class CourseUserScore(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u"用户")
    score  = models.FloatField(u"课程评分", default=0.0)

    class Meta:
        verbose_name = u"课程用户评分"
        verbose_name_plural = verbose_name
        unique_together = (("course", "user"),)

    def __unicode__(self):
        return self.score

# 前向兼容
Course_User_Score = CourseUserScore