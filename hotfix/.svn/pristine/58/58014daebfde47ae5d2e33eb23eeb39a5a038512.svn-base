#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models


# （app）版本管理
class AndroidVersion(models.Model):
    vno = models.CharField(max_length=10, verbose_name="版本号")
    size = models.CharField(
        max_length=10, verbose_name="文件大小", null=True, blank=True)
    desc = models.TextField(null=True, blank=True, verbose_name="功能简介")
    is_force = models.BooleanField(default=False, verbose_name="是否强制更新")
    down_url = models.CharField(max_length=100, verbose_name="下载地址")

    class Meta:
        verbose_name = "版本管理"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return str(self.id)
