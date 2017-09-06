# -*- coding: utf-8 -*-
# lewis
from django.db import models

# Create your models here.
from django.db import models

class NameMode(models.Model):
    url = models.CharField(u'URL地址', max_length=100, db_index=True)
    index = models.IntegerField(u'排列顺序(从小到大)', default=999)
    created = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['index', 'id']


class RecommendKeywords(models.Model):
    name = models.CharField(u'搜索关键词', max_length = 20, db_index=True)
    index = models.IntegerField(u'排列顺序(从小到大)', default=999)
    created = models.DateTimeField(u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name = u'搜索关键词'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

class Ad(NameMode):
    image = models.ImageField(u'图片(1160*300)', upload_to=u"homepage/%Y/%m", db_index=True)
    title = models.CharField(u'标题', max_length=20, db_index=True)
    back_image = models.ImageField(u"图片背景虚化图(1920*300)", upload_to=u"homepage/%Y/%m", db_index=True)

    class Meta:
        verbose_name = u'首页Banner图'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.title)

class RecommendPoint(NameMode):
    image = models.ImageField(u'图片(232*110)', upload_to=u"homepage/%Y/%m", db_index=True)
    title = models.CharField(u'标题', max_length=20, db_index=True)

    class Meta:
        verbose_name = u'重点推荐'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.title)

class News(NameMode):
    NEWS_TYPE_LATEST = 'latest'
    NEWS_TYPE_COURSE = 'course'
    NEWS_TYPE = {NEWS_TYPE_LATEST: u'最新资讯', NEWS_TYPE_COURSE: u'课程相关资讯'}
    title = models.CharField(u'标题', max_length=50, db_index=True)
    type = models.CharField(u'资讯类型', max_length=20, choices=NEWS_TYPE.items(), default=NEWS_TYPE_LATEST)

    class Meta:
        verbose_name = u'资讯'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.title)

class LiveStudy(NameMode):
    image = models.ImageField(u'图片(275*174)', upload_to=u"homepage/%Y/%m", db_index=True)
    title = models.CharField(u'标题', max_length=50, db_index=True)
    original_price = models.IntegerField(u'原价', db_index=True, default=0)
    current_price = models.IntegerField(u'现价', db_index=True, default=0)
    lecturer = models.CharField(u'讲师', max_length=20, db_index=True)
    limit_count = models.IntegerField(u'限制人数', db_index=True, default=0)
    real_count = models.IntegerField(u'剩余人数', db_index=True, default=0)
    live_startdate = models.DateTimeField(u'直播开始时间', db_index=True)
    live_enddate = models.DateTimeField(u'直播结束时间', db_index=True)

    class Meta:
        verbose_name = u'直播试学'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.title)

class CourseInfo(NameMode):
    COURSE_TYPE_HOT = 'hot'
    COURSE_TYPE_LATEST = 'latest'
    COURSE_TYPE_PROJECT = 'project'
    COURSE_TYPE_TEACHER = 'teacher'
    COURSE_TYPE = {COURSE_TYPE_HOT: u'热门推荐', COURSE_TYPE_LATEST: u'最新课程', COURSE_TYPE_PROJECT: u'项目实战',
                   COURSE_TYPE_TEACHER: u'名师独家'}
    image = models.ImageField(u'图片(275*174)', upload_to=u"homepage/%Y/%m", db_index=True)
    title = models.CharField(u'标题', max_length=50, db_index=True)
    type = models.CharField(u'课程信息类型', max_length=20, choices=COURSE_TYPE.items(), default=COURSE_TYPE_HOT)
    description = models.CharField(u'描述', max_length=200, db_index=True)
    studying_count = models.IntegerField(u'学习人数', default=0)
    lesson_count = models.IntegerField(u'章节数', default=0)
    lecturer = models.CharField(u'讲师', max_length=20, db_index=True)

    class Meta:
        verbose_name = u'课程信息(热门推荐,最新课程,项目实战,名师独家)'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.title)


class CareerPath(NameMode):
    image = models.ImageField(u'图片(84*84)', upload_to=u"homepage/%Y/%m", db_index=True)
    name = models.CharField(u'课程名称', max_length=50, db_index=True)
    monthly_salary = models.CharField(u'月薪', max_length=20, db_index=True)
    description = models.CharField(u'描述', max_length=100, db_index=True)

    class Meta:
        verbose_name = u'职业路线'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.name)

class GoldLecturer(NameMode):
    image = models.ImageField(u'图片(140*140)', upload_to=u"homepage/%Y/%m", db_index=True)
    name = models.CharField(u'讲师名称', max_length=50, db_index=True)
    description = models.CharField(u'描述', max_length=200, db_index=True)

    class Meta:
        verbose_name = u'金牌讲师'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.name)

class Cooperation(NameMode):
    COOPERATION_TYPE_MEDIA = 'media'
    COOPERATION_TYPE_ENTERPRISE = 'enterprise'
    COOPERATION_TYPE_ACADEMY = 'academy'
    COOPERATION_TYPE = {COOPERATION_TYPE_MEDIA: u'媒体报道', COOPERATION_TYPE_ENTERPRISE: u'合作企业',
                        COOPERATION_TYPE_ACADEMY: u'合作院校'}
    image = models.ImageField(u'图片(合作院校265*90;其他170*70)', upload_to=u"homepage/%Y/%m", db_index=True)
    name = models.CharField(u'合作对象名称', max_length=50, db_index=True)
    type = models.CharField(u'合作类型', max_length=20, choices=COOPERATION_TYPE.items(), default=COOPERATION_TYPE_MEDIA)

    class Meta:
        verbose_name = u'合作推广'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.name)

class AdImage(models.Model):
    ADIMAGE_TYPE_COURSE = 0
    ADIMAGE_TYPE_SUSPENSION = 1
    ADIMAGE_TYPE = {ADIMAGE_TYPE_COURSE: u'课程广告', ADIMAGE_TYPE_SUSPENSION: u'悬浮广告'}
    image = models.ImageField(u'图片（课程图片275*174,悬浮广告120*200）', upload_to=u"homepage/%Y/%m", db_index=True)
    url = models.CharField(u'URL地址', max_length=100, db_index=True)
    created = models.DateTimeField(u'创建时间', auto_now_add=True)
    title = models.CharField(u'标题', max_length=20, db_index=True)
    type = models.IntegerField(u'广告位置', choices=ADIMAGE_TYPE.items(), default=ADIMAGE_TYPE_COURSE)

    class Meta:
        verbose_name = u'广告图片'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.title)