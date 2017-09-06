#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models
import career_course.CareerCourse as CareerCourse


class ShowStage(models.Model):
    name = models.CharField(u"阶段名称", max_length=50)
    description = models.TextField(u"阶段描述")
    task_knowledge_test = models.CharField(
        u"任务数、知识点数、测试项数", max_length=50, default="8,32,64")
    task_list = models.CharField(
        u"任务列表", max_length=200, default="任务一,任务二,任务三,任务四,任务五,任务六,任务七,任务八")
    image_url = models.ImageField(
        u"阶段图片", upload_to="show_stage/%Y/%m", max_length=200)
    career_course = models.ForeignKey(CareerCourse, verbose_name=u"职业课程")

    class Meta:
        verbose_name = u"展示阶段"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.name)
