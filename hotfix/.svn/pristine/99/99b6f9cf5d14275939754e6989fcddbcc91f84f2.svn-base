#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models


# （app）留言反馈model
class Feedback(models.Model):
    content = models.TextField(u'反馈内容')
    date_publish = models.DateTimeField(u"发布时间", auto_now_add=True)

    class Meta:
        verbose_name = "留言反馈"
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __unicode__(self):
        return str(self.id)
