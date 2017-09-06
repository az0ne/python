#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models


class RecommendKeywords(models.Model):
    name = models.CharField(u'推荐搜索关键词', max_length=50)

    class Meta:
        verbose_name = u'推荐搜索关键词'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name
