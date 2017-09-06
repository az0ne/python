#!/usr/bin/env python
# -*- coding: utf8 -*-

from mz_platform.objects.sql_result_wrapper import SqlResultWrapper


class Seo(SqlResultWrapper):
    """
    @brief Seo对象

    '''对象SEO'''
    TYPE_CHOICES = (
        ('ARTICLE', '文章'),
        ('TEACHER', '老师'),
        ('COURSE', '课程'),
        ('LESSON', '视频'),
    )
    obj_type = models.CharField(u'对象类型', max_length=10, choices=TYPE_CHOICES, default='COURSE')
    obj_id = models.IntegerField(u'对象ID')
    seo_title = models.CharField(u'SEO title', max_length=500)
    seo_keywords = models.CharField(u'SEO keywords', max_length=500)
    seo_description = models.CharField(u'SEO description', max_length=500)

    """

    pass
