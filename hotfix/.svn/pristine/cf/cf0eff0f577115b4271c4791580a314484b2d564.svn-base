#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models
from .career_course import CareerCourse


class StageManager(models.Manager):
    def get_queryset(self):
        # 调用父类的方法，在原来返回的QuerySet的基础上返回新的QuerySet
        return super(StageManager, self).get_queryset().exclude(lps_version='3.0')

    def xall(self):
        return super(StageManager, self).get_queryset()

# 阶段 models


class Stage(models.Model):
    name = models.CharField("阶段名称", max_length=50)
    description = models.TextField("阶段描述")
    price = models.IntegerField("阶段价格")
    index = models.IntegerField("阶段顺序(从小到大)", default=999)
    is_try = models.BooleanField(default=False, verbose_name=u"是否是试学阶段")
    career_course = models.ForeignKey(CareerCourse, verbose_name="职业课程")

    # 首付款有效天数
    valid_days = models.IntegerField(default=30, verbose_name=u"有效时间")
    lps_version = models.CharField(
        u"lps版本", max_length=16, blank=True, null=True)

    objects = StageManager()

    class Meta:
        verbose_name = "课程阶段"
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return '%s: %s' % (self.career_course, self.name)

    # def getCourseSet(self):
    # if self.course_set.count():
    # return self.course_set.all()
    # else:
    #     return Course.objects.filter(stages_m = self)
