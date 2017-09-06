#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models


class AppAd(models.Model):
    ad_types = (
        ('0', '课程'),
        ('1', '企业直通班'),
        ('2', '问答'),
        ('3', '文章'),
        ('4', '活动'),
        ('5', '外链'),
    )

    class Meta:
        verbose_name = u'App广告'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']
    title = models.CharField(u'广告标题', max_length=50)
    description = models.CharField(
        u'广告描述', max_length=200, blank=True, null=True)
    image_url = models.ImageField(u'图片路径', upload_to='ad/%Y/%m')
    ad_type = models.CharField(u'广告类型', choices=ad_types, max_length=1)
    target_id = models.IntegerField(u'跳转目标ID')
    index = models.IntegerField("排列顺序(从小到大)", default=999)
    callback_url = models.URLField(u'回调url', null=True, blank=True)

    def __unicode__(self):
        return self.title
