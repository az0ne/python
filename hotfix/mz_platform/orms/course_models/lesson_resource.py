#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models
from .lesson import Lesson

# 章节资源 models
class LessonResource(models.Model):
    name = models.CharField("章节资源名称", max_length=50)
    download_url = models.FileField("下载地址", upload_to="lesson/%Y/%m")
    download_count = models.IntegerField("下载次数", default=0)
    lesson = models.ForeignKey(Lesson, verbose_name="章节")

    class Meta:
        verbose_name = "章节资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
