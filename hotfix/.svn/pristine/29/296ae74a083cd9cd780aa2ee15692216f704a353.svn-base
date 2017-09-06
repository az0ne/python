#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models

# 新手问答与课程页常见问答


class FAQ(models.Model):
    title = models.CharField("标题", max_length=200)
    content = models.TextField("内容", max_length=1000)
    type = models.SmallIntegerField(
        default=0, choices=((0, "新手问答页"), (1, "课程页"),), verbose_name="问答类型")
    index = models.IntegerField("排列顺序(从小到大)", default=999)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title
