#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models


class PageSeoSet(models.Model):
    page_name_types = (
        ('1', '首页'),
        ('2', '移动app'),
        ('3', '职业课程'),
        ('4', '课程列表页'),
        ('5', '教师列表页'),
    )
    page_name = models.CharField(
        "单页名称", choices=page_name_types, max_length=3, null=True, blank=True)
    seo_title = models.CharField(
        "SEO标题", max_length=200, null=True, blank=True)
    seo_keyword = models.CharField(
        "SEO关键词", max_length=200, null=True, blank=True)
    seo_description = models.TextField("SEO描述", null=True, blank=True)

    class Meta:
        verbose_name = u'单页SEO设置'
        verbose_name_plural = verbose_name
        unique_together = (("page_name",),)
        # db_table = "mz_common_pageseoset"
        db_table = 'mz_course_careercourse'

    def __unicode__(self):
        return self.page_name
