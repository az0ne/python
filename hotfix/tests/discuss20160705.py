# -*- coding: utf-8 -*-
"""
@version: 2016/7/6 0006
@author: lewis
@contact: lewis@maiziedu.com
@file: discuss20160705.py
@time: 2016/7/6 0006 9:47
@note:  ??
"""

from django.db import models


class NewDiscuss(models.Model):
    '''评论列表'''
    TYPE_CHOICES = (
        ('ARTICLE', '文章'),
        ('LESSON', '视频'),
        ('PROJECT', '项目制作'),
        ('TEST', '限时答题')
    )
    object_content = models.CharField(u'对象的内容', blank=True, null=True, max_length=20)
    object_name = models.CharField(u'对象的名称', blank=True, null=True, max_length=50)
    object_location = models.CharField(u'对象位置', blank=True, null=True, max_length=50)
    # {"course":[316,3085]}    {"lps":[316,3085,445]}

    group_name = models.CharField(u'用户组的名称', blank=True, null=True, max_length=20)
    problem_id = models.IntegerField(u'当前回复所属提问ID', default=0, db_index=True)
    weight = models.SmallIntegerField(u'权重', default=0, db_index=True) #学生默认为0;老师为1
    last_answer_datetime = models.DateTimeField(u'最后回复时间',  blank=True, null=True)
    last_answer_id = models.IntegerField(u'最后回复ID', blank=True, null=True, db_index=True)

    answer_user_id = models.IntegerField(u'回复对象的用户ID', blank=True, null=True)
    answer_nick_name = models.CharField(u'回复对象名称', blank=True, null=True, max_length=50)
    discuss_count = models.IntegerField(u'评论数量', default=0)
    user_praise_count = models.IntegerField(u'用户点赞数量', default=0)

class UserNewDiscussStatus(models.Model):
    """用户评论列表的状态"""
    STATUS = (
        (1, '未读'),
        (2, '已读/未回复'),
        (3, '已回复')
    )

    status = models.SmallIntegerField(u'评论状态', choices=STATUS, default=1)
    user_id = models.IntegerField(u'用户ID', db_index=True)
    new_discuss = models.ForeignKey(NewDiscuss, verbose_name=u"评论列表")
    group_name = models.CharField(u'用户组的名称', blank=True, null=True, max_length=20)

    class Meta:
        verbose_name = u"用户评论列表的状态"
        verbose_name_plural = verbose_name
        unique_together = (("user_id", "new_discuss"),)


class NewDiscussUserPraise(models.Model):
    """用户积赞记录"""
    user_id = models.IntegerField(u'用户ID', db_index=True)
    new_discuss = models.ForeignKey(NewDiscuss, verbose_name=u"评论列表")

    class Meta:
        verbose_name = u"用户积赞记录"
        verbose_name_plural = verbose_name
        unique_together = (("user_id", "new_discuss"),)


class NewDiscussMaterial(models.Model):
    """评论素材"""
    new_discuss = models.ForeignKey(NewDiscuss, verbose_name=u'评论列表')
    name = models.CharField(u"评论素材名称", blank=True, null=True, max_length=50)
    material = models.FileField(u'素材', upload_to="NewDiscuss/Material/%Y/%m")
    small_material = models.FileField(u'素材缩略图', upload_to="NewDiscuss/Material/%Y/%m")

    class Meta:
        verbose_name = u"评论素材"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)
