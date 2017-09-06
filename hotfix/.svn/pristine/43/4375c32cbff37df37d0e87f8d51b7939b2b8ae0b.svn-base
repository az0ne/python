#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models


class Institute(models.Model):
    """
    **描述** :
        - 对应表mz_course_institute

    **字段** :
        - **name** : 学院名称
        - **order** : 排序
    """
    name = models.CharField("学院名称", max_length=50)
    order = models.IntegerField("排序", max_length=50, default=0)

    class Meta:
        verbose_name = "学院分类"
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __unicode__(self):
        return self.name
