# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime

__author__ = 'bobby'

class Entity(models.Model):
    content = models.TextField("内容", blank=False, null=False, max_length=1000)
    title = models.TextField("标题", blank=False, null=False, max_length=40)
    date_publish = models.DateTimeField("发布时间", auto_now_add=True)
    relate_id = models.IntegerField("相关ID", blank=True, null=True)
    user = models.IntegerField("用户", blank=False, null=False)
    # nick_name = models.IntegerField("用户昵称", blank=False, null=False)
    nickname = models.CharField("用户昵称", blank=True, null=True, max_length=50)
    review_count = models.IntegerField("浏览次数", blank=False, null=False, default=0)
    reply_count = models.IntegerField("回复次数", blank=False, null=False, default=0)
    collect_count = models.IntegerField("收藏次数", blank=False, null=False, default=0)
    praise_count = models.IntegerField("赞次数", blank=False, null=False, default=0)
    forward_count = models.IntegerField("转发次数", blank=False, null=False, default=0)
    is_head = models.BooleanField("已置顶", blank=False, null=False, default=False)

    class Meta:
        verbose_name = "社交内容"
        verbose_name_plural = verbose_name
        db_table = 'mz_forum_entity'

class Ask(Entity):
    is_solved = models.BooleanField("已解决", blank=False, null=False, default=False)
    is_great = models.BooleanField("已加精", blank=False, null=False, default=False)
    # invited_users = models.CommaSeparatedIntegerField("受邀用户",null=True,max_length=200)需要用到@功能时解除注释
    class Meta:
        verbose_name = "问答"
        verbose_name_plural = verbose_name
        db_table = 'mz_forum_ask'

    def __unicode__(self):
        return str(self.id)

class UserSocialProfile(models.Model):
    user = models.IntegerField("用户", blank=False, null=False)
    ticket = models.IntegerField("积分", blank=False, null=False, default=0)
    study_days = models.IntegerField("学习天数", blank=False, null=False, default=0)
    no_more_guide_prompt = models.BooleanField("不再提示", blank=False, default=False)
    phone_number = models.CharField("手机号", blank=True, null=False, max_length=11)

    class Meta:
        db_table = 'mz_forum_usersocialprofile'


class Activity(Entity):
    datetime_start = models.DateTimeField("开始时间", null=False, blank=False)
    datetime_end = models.DateTimeField("结束时间", null=False, blank=False)
    location = models.CharField("地点", null=True, blank=True, max_length=50)
    register_count = models.IntegerField("报名人数", default=0)
    image = models.ImageField("活动图标", upload_to="Activity/%Y/%m")
    status = models.SmallIntegerField(choices=((1, u"进行中"), (0, u"未开始"), (2, u"已结束"), (3, u"已关闭"),), default=0,
                                      verbose_name=u"课程状态")
    price = models.CharField("费用", null=False, blank=False, default="0", max_length=50)
    activity_user = models.ManyToManyField(UserSocialProfile, null=True, blank=True, through="ActivityUser",
                                           verbose_name=u"参加的用户")

    class Meta:
        verbose_name = "活动"
        verbose_name_plural = verbose_name
        db_table = 'mz_forum_activity'

    def __unicode__(self):
        return str(self.id)


class ActivityUser(models.Model):
    activity = models.ForeignKey(Activity, null=False, blank=False, verbose_name="活动")
    user = models.ForeignKey(UserSocialProfile, null=False, blank=False, verbose_name="用户")  # 没有使用外键，因为要跨表连接

    class Meta:
        verbose_name = u"参加用户"
        verbose_name_plural = verbose_name
        unique_together = (('activity', 'user'),)
        db_table = 'mz_forum_activityuser'

    def __unicode__(self):
        # return self.name # has no attriute of name. we may need another field to store the student'name
        return str(self.student)

class Article(Entity):
    is_great = models.BooleanField("已加精", blank=False, null=False, default=False)
    privilege = models.SmallIntegerField(choices=((0, u"本班可见"), (1, u"好友可见"), (2, u"我的粉丝可见"), (3, u"全部可见")),
                                         default=3, verbose_name=u"文章权限")
    image = models.ImageField("文章题图", upload_to="Article/%Y/%m", null=False, blank=False, max_length=300)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        db_table = 'mz_forum_article'

    def __unicode__(self):
        return str(self.id)

class Comment(models.Model):
    content = models.TextField("讨论内容", max_length=400)
    parent_id = models.IntegerField("父讨论ID", blank=True, null=True)
    child_id = models.IntegerField("子讨论ID", blank=True, null=True)
    date_publish = models.DateTimeField("发布时间", default =datetime.now())
    relate_id = models.IntegerField("相关ID", blank=True, null=True)
    type = models.SmallIntegerField("讨论类型", choices=((0, u"问答"), (1, u"文章"), (2, u"活动"), (3, u"课程"), (4, u"班级")),
                                    blank=True, null=True)
    lesson_id = models.IntegerField("课程章节ID", blank=True,
                                    null=True)  # this cloumn is not in usage any way.
    user = models.IntegerField("用户", blank=False, null=False)
    reply_count = models.IntegerField("回复次数", blank=False, null=False, default=0)
    praise_count = models.IntegerField("赞次数", blank=False, null=False, default=0)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        db_table = 'mz_forum_discuss'

    def __unicode__(self):
        return str(self.id)


class CourseAsk(Entity):
    class Meta:
        verbose_name = "课程问答"
        verbose_name_plural = verbose_name
        db_table = 'mz_forum_courseask'

    def __unicode__(self):
        return str(self.id)


class Discuss(models.Model):
    content = models.TextField("讨论内容", max_length=400)
    parent_id = models.IntegerField("父讨论ID", blank=True, null=True)
    child_id = models.IntegerField("子讨论ID", blank=True, null=True)
    date_publish = models.DateTimeField("发布时间", default=datetime.now)
    relate_id = models.IntegerField("相关ID", blank=True, null=True)
    type = models.SmallIntegerField("讨论类型", choices=((0, u"问答"), (1, u"文章"), (2, u"活动"), (3, u"课程"),
                                    (4, u"班级"), (5, u"公开课讨论")), blank=True, null=True)
    lesson_id = models.IntegerField("课程章节ID", blank=True,
                                    null=True)  # this cloumn is not in usage any way.
    user = models.IntegerField("用户", blank=False, null=False)
    reply_count = models.IntegerField("回复次数", blank=False, null=False, default=0)
    praise_count = models.IntegerField("赞次数", blank=False, null=False, default=0)
    # collected_praised_by = models.ManyToManyField(UserSocialProfile, null=True, blank=True, verbose_name="被谁收藏",
                                                  # through="DiscussCollectionPraise")

    class Meta:
        verbose_name = "讨论"
        verbose_name_plural = verbose_name
        db_table = 'mz_forum_discuss'


class UserNetwork(models.Model):
    userA = models.IntegerField(u"用户A", null=False, blank=False)  # 发送方，为0表示系统用户
    userB = models.IntegerField(u"用户B", null=False, blank=False)   # 接收方，为0就给所有用户发送消息
    join_datatime = models.DateTimeField("建立时间", null=False, blank=False, auto_now_add = True)

    class Meta:
        verbose_name = u"用户网络"
        verbose_name_plural = verbose_name
        unique_together = (("userA", "userB"),)
        db_table = 'mz_common_usernetwork'

    def __unicode__(self):
        return str(self.id)


# Create your models here.
class DynamicMsg(models.Model):
    action_types = (
        ('1', '系统消息'),
        ('2', '课程讨论回复'),
        ('24', '课程被回复'),
        ('3', '论坛讨论回复'),
        ('4', '教师督促学生'),
        ('5', '问答回复被点赞'),  # 记录点赞，不单独建表
        ('19', '问答被回复'),
        ('20', '问答被点赞'),
        ('21', '问答被加精'),
        ('22', '问答被置顶'),
        ('23', '问答回复被回复'),
        ('14', '@自己的提问'),
        ('6', '文章中的回复'),
        ('7', '文章被加精'),  # 记录加精，不单独建表
        ('8', '文章被置顶'),
        ('9', '文章被点赞'),  # 记录点赞，不单独建表
        ('10', '文章评论被点赞'),
        ('18', '文章评论被回复'),  # 是否需要定位冒点？
        ('11', '活动评论的回复'),
        ('25', '活动被回复'),
        ('12', '活动回复被点赞'),
        ('13', '活动报名成功'),
        ('15', '新建文章'),
        ('16', '新建问答'),
        ('17', '新建活动'),
        ('26', '关注了你'),
        ('27', '成了好友')
    )

    userA = models.IntegerField(u"用户A")  # 发送方，为0表示系统用户
    userB = models.IntegerField(u"用户B")  # 接收方，为0就给所有用户发送消息
    relate_id = models.IntegerField("相关ID", blank=True, null=True)
    action_type = models.CharField(u'类型', choices=action_types, max_length=2)
    action_id = models.IntegerField(u'动作id', blank=True, null=True)
    action_content = models.TextField(u'消息内容', blank=True, null=True)
    date_action = models.DateTimeField(u"添加日期", auto_now_add=True)
    is_new = models.BooleanField(u'是否为最新', default=True)

    class Meta:
        verbose_name = u'我的动态'
        verbose_name_plural = verbose_name
        db_table = 'mz_common_dynamicmsg'

    def __unicode__(self):
        return str(self.id)
