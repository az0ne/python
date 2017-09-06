#!/usr/bin/env python
# -*- coding: utf8 -*-
from django.db import models


class Ad(models.Model):
    class Meta:
        verbose_name = u'网站广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']
    title = models.CharField(u'广告标题', max_length=50)
    description = models.CharField(u'广告描述', max_length=200)
    image_url = models.ImageField(
        u'图片路径(课程列表页与老师列表页广告图片上传大小为500*40）)', upload_to='ad/%Y/%m')
    back_image = models.CharField(
        "图片背景虚化图", null=True, blank=True, max_length=100)
    callback_url = models.URLField(u'回调url', null=True, blank=True)
    index = models.IntegerField("排列顺序(从小到大)", default=999)
    type = models.SmallIntegerField(default=0, choices=(
        (0, "首页"), (1, "课程列表页"), (2, "老师列表页"),), verbose_name="广告类型")

    def __unicode__(self):
        return self.title
