#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models


class Links(models.Model):
    title = models.CharField(u'标题', max_length=50)
    description = models.CharField(u'友情链接描述', max_length=200)
    image_url = models.ImageField(
        u'图片路径', upload_to='links/%Y/%m', null=True, blank=True)
    callback_url = models.URLField(u'回调url')
    is_pic = models.BooleanField(u'是否为图片', default=False)

    class Meta:
        verbose_name = u'友情链接'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title
