#!/usr/bin/env python
# -*- coding: utf8 -*-

from mz_platform.objects.sql_result_wrapper import SqlResultWrapper


class CareerAd(SqlResultWrapper):
    """
    @brief      CareerAd对象

    '''职业对应广告'''
    '''评论列表'''
    TYPE_CHOICES = (
        ('ARTICLE', '文章'),
        ('COURSE', '课程'),
    )
    career_id = models.IntegerField(u'职业课程ID', db_index=True)
    img_url = models.CharField(u'对象类型', max_length=500)
    img_title = models.CharField(u'图片title', max_length=500)
    type = models.CharField(u'对象类型', choices=TYPE_CHOICES, default='COURSE', max_length=20)
    is_actived = models.BooleanField(u'是否生效', default=True)

    class Meta:
        verbose_name = u'职业对应广告'
        verbose_name_plural = verbose_name
    """

    pass
