#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models


# 消息推送Model
class MsgBox(models.Model):
    sendtarget = models.SmallIntegerField(
        u"发送对象",
        default="-1",
        null=True,
        blank=True,
        choices=((-1, u"全部"), (0, u"学生"), (1, u"老师"),))
    content = models.TextField(u'消息内容')
    date_send = models.DateTimeField(u"发送时间", auto_now_add=True)
    is_sendmsg = models.BooleanField(u"是否发送站内信", default=False)
    is_sendemail = models.BooleanField(u"是否发送邮件", default=False)
    is_sendappmsg = models.BooleanField(u"是否推送App消息", default=False)

    class Meta:
        verbose_name = "消息推送记录"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)
