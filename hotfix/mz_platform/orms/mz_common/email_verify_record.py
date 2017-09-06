#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models
from datetime import datetime


class EmailVerifyRecord(models.Model):

    '''
    邮箱验证记录表（包括注册和忘记密码使用到的验证链接）
    '''

    code = models.CharField(max_length=10, verbose_name="验证码")
    email = models.CharField(max_length=50, verbose_name="邮箱")
    type = models.SmallIntegerField(
        default=0, choices=((0, "注册"), (1, "忘记密码"),), verbose_name="验证码类型")
    ip = models.CharField(max_length=20, verbose_name="请求来源IP")
    created = models.DateTimeField(
        auto_now_add=True,
        default=datetime.now(),
        verbose_name="创建时间")

    class Meta:
        verbose_name = "邮箱验证记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.code
