#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models
from datetime import datetime, timedelta


class Coupon(models.Model):
    # endtime = datetime.now() + timedelta(days=90)
    surplus = models.IntegerField(verbose_name=u"剩余张数")
    coupon_price = models.CharField(max_length=20, verbose_name=u"优惠金额")
    createtime = models.DateTimeField(
        default=datetime.now(), auto_now_add=True, verbose_name=u"创建时间")
    endtime = models.DateTimeField(auto_now_add=True, verbose_name=u"结束时间")

    class Meta:
        verbose_name = u"优惠码"
        verbose_name_plural = verbose_name
