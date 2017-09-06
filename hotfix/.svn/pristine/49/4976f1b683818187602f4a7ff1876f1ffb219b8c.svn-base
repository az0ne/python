# -*- coding: utf-8 -*-
__author__ = 'zhangyunrui'
from django.db import models


class LogRecords(models.Model):
    file_name = models.CharField(u'文件名', max_length=20)
    time = models.CharField(u'时间', max_length=50)
    internal_server_error = models.CharField(u'路径', max_length=200)
    traceback = models.TextField(u'回溯')
    # exception = models.CharField(u'错误信息', max_length=100)

    class Meta:
        verbose_name = u'日志'
        verbose_name_plural = verbose_name
