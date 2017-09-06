#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import Signal

from course import Course as Course

# 章节 models


class Lesson(models.Model):
    name = models.CharField("章节名称", max_length=50)
    video_url = models.CharField("视频资源URL", max_length=1000)
    video_length = models.IntegerField("视频长度（秒）")
    play_count = models.IntegerField("播放次数", default=0)
    share_count = models.IntegerField("分享次数", default=0)
    index = models.IntegerField("章节顺序(从小到大)", default=999)
    is_popup = models.BooleanField("是否弹出提示框（支付、登录）", default=False)
    course = models.ForeignKey(Course, verbose_name="课程")
    seo_title = models.CharField(
        "SEO标题", max_length=200, null=True, blank=True)
    seo_keyword = models.CharField(
        "SEO关键词", max_length=200, null=True, blank=True)
    seo_description = models.TextField("SEO描述", null=True, blank=True)
    # add by yuxin
    have_homework = models.BooleanField(
        "是否有作业", null=False, blank=False, default=True)
    code_exercise_type = models.SmallIntegerField(
        "在线编码类型",
        choices=((0, "无在线编码"), (1, "python"), (2, "php"),),
        default=0)

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']
        db_table = 'mz_course_lesson'

    def __unicode__(self):
        return self.name


def Post_Save_Handle(**kwargs):
    """
    @TODO: 替换signal处理方式，或者规范signal处理方式
    """
    obj = kwargs['sender']
    created = False

    # if kwargs.has_key('created'):
    if 'created' in kwargs:
        created = kwargs['created']

    # 如果是添加新的课程章节，更新章节对应课程Course对象的最新发布时间
    if created and (obj is Lesson):
        inst = kwargs['instance']
        inst.course.date_publish = datetime.now()
        inst.course.save()

Signal.connect(post_save, Post_Save_Handle)
