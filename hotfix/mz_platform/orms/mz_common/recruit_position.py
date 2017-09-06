#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models
from .maizi_department import MaiziDeparment


class RecruitPosition(models.Model):
    department = models.ForeignKey(MaiziDeparment, verbose_name="部门")
    title = models.CharField("职位", max_length=30)
    desc = models.TextField("描述", max_length=1000)
    index = models.IntegerField("排列顺序(从小到大)", default=999)

    class Meta:
        verbose_name = "招聘职位"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title
