#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models

# 手机活动页面咨询统计信息


class AppConsultInfo(models.Model):
    market_types = (
        ('sem', 'SEM'),
        ('10086', '中国移动'),
        ('operate', '运营'),
        ('trad', '传统培训'),
    )

    name = models.CharField("姓名", max_length=30, null=True, blank=True)
    phone = models.CharField("电话", max_length=30, null=True, blank=True)
    qq = models.CharField("QQ", max_length=30, null=True, blank=True)
    interest = models.CharField("兴趣方向", max_length=50, null=True, blank=True)
    source = models.CharField("来源", max_length=50, null=True, blank=True)
    date_publish = models.DateTimeField("发布时间", auto_now_add=True)

    market_from = models.CharField(
        "市场推广来源", default='sem', max_length=20, null=True, blank=True, choices=market_types)

    class Meta:
        verbose_name = "手机活动页咨询统计"
        verbose_name_plural = verbose_name
        ordering = ['-id']
        unique_together = (("name", "phone", "qq", "interest"),)

    def __unicode__(self):
        return self.name
