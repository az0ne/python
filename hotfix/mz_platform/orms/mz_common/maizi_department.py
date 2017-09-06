#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models


class MaiziDeparment(models.Model):
    name = models.CharField("部门", max_length=30)
    index = models.IntegerField("排列顺序(从小到大)", default=999)

    class Meta:
        verbose_name = "麦子学院部门"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
