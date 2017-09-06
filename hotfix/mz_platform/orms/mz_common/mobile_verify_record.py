#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models
from datetime import datetime


class MobileVerifyRecord(models.Model):

    '''
    手机验证码记录表
    '''

    code = models.CharField(max_length=6, verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    type = models.SmallIntegerField(
        default=0, choices=((0, "注册"), (1, "忘记密码"),), verbose_name="验证码类型")
    ip = models.CharField(max_length=20, verbose_name="请求来源IP")
    created = models.DateTimeField(
        auto_now_add=True,
        default=datetime.now(),
        verbose_name="创建时间")
    source = models.IntegerField(
        default=3,
        choices=((1, "pc"), (2, "手机"), (3, "未知")),
        verbose_name="来源")

    class Meta:
        verbose_name = "手机验证记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.code
