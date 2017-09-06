#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models


# 组织结构基类
class Org(models.Model):
    name = models.CharField("名称", unique=True, max_length=30)
    index = models.IntegerField("顺序(从小到大)", default=999)
    image = models.ImageField(
        "小图标", upload_to="org/%Y/%m", null=True, blank=True)
    big_image = models.ImageField(
        "大图标", upload_to="org/%Y/%m", null=True, blank=True)
    app_image = models.ImageField(
        "app端小图标", upload_to="org/%Y/%m", null=True, blank=True)
    description = models.TextField("介绍", null=True, blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, verbose_name="父级机构")
    level = models.IntegerField("级别", default=1)

    class Meta:
        verbose_name = "组织机构"
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']

    def __unicode__(self):
        return self.name
