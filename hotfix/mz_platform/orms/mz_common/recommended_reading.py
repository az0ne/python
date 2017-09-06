#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models


class RecommendedReading(models.Model):
    ACTIVITY = 'AV'
    NEWS = 'NW'
    DISCUSS = 'DC'

    READING_TYPES = (
        (ACTIVITY, '官方活动'),
        (NEWS, '开发者资讯'),
        (DISCUSS, '技术交流'),
    )

    reading_type = models.CharField(max_length=2,
                                    choices=READING_TYPES,
                                    default=ACTIVITY
                                    )

    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200)

    class Meta:
        verbose_name = "首页推荐文章"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.title
