#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.db import models
from django import forms
from mz_course.models import CareerCourse
# Create your models here.
class UserCenterAd(models.Model):
    '''个人中心对应广告'''
    img_url = models.ImageField(u"个人中心广告",upload_to= 'ad/userCenterAd/%Y/%m', max_length=500)
    img_title = models.CharField(u'图片title', max_length=500)
    is_actived = models.BooleanField(u'是否生效', default=True)
    class Meta:
        verbose_name = u'个人中心对应广告'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.img_title

class CareerAd(models.Model):
    '''职业对应广告'''
    '''评论列表'''
    TYPE_CHOICES = (
        ('ARTICLE', '文章'),
        ('COURSE', '课程'),
    )
    career_id = models.IntegerField(u'职业课程ID', db_index=True)
    img_url = models.ImageField(u'对象类型', upload_to= 'ad/careerAd/%Y/%m',max_length=500)
    img_title = models.CharField(u'图片title', max_length=500)
    type = models.CharField(u'对象类型', choices=TYPE_CHOICES, default='COURSE', max_length=20)
    is_actived = models.BooleanField(u'是否生效', default=True)

    class Meta:
        verbose_name = u'职业对应广告'
        verbose_name_plural = verbose_name
    @property
    def career(self):
        return CareerCourse.objects.get(id=self.career_id)


class ObjSEO(models.Model):
    '''对象SEO'''
    TYPE_CHOICES = (
        ('ARTICLE', '文章'),
        ('TEACHER', '老师'),
        ('COURSE', '课程'),
        ('LESSON', '视频'),
    )
    obj_type = models.CharField(u'对象类型', max_length=10, choices=TYPE_CHOICES, default='COURSE')
    obj_id = models.IntegerField(u'对象ID')
    seo_title = models.CharField(u'SEO title', max_length=500)
    seo_keywords = models.CharField(u'SEO keywords', max_length=500)
    seo_description = models.CharField(u'SEO description', max_length=500)

    class Meta:
        verbose_name = u'对象SEO'
        verbose_name_plural = verbose_name


class ArticleType(models.Model):
    '''文章类型'''
    name = models.CharField(u'文章类型', max_length=50)
    is_homepage = models.BooleanField(u'是否首页显示', default=False)

    class Meta:
        verbose_name = u'文章类型'
        verbose_name_plural = verbose_name


class ObjTagRelation(models.Model):
    '''对象标签关系'''
    TYPE_CHOICES = (
        ('ARTICLE', '文章'),
        ('TEACHER', '老师'),
        ('COURSE', '课程'),
    )
    obj_type = models.CharField(u'对象类型', max_length=10, choices=TYPE_CHOICES, default='COURSE')
    obj_id = models.IntegerField(u'对象ID')
    tag_id = models.IntegerField(u'标签ID', db_index=True)
    careercatagory_id = models.IntegerField(u'专业方向ID', db_index=True)

    class Meta:
        verbose_name = u'对象标签关系'
        verbose_name_plural = verbose_name

class NewArticle(models.Model):
    '''文章'''
    title = models.CharField(u'文章标题', max_length=200)
    content = models.TextField(u'内容')
    abstract = models.CharField(u'摘要', max_length=200)
    title_image = models.CharField(u'文章配图', max_length=200)
    user_id = models.IntegerField(u'发表用户ID')
    nick_name = models.CharField(u'昵称', max_length=50)
    user_head = models.CharField(u'用户头像', max_length=200)
    replay_count = models.IntegerField(u'回复数量')
    praise_count = models.IntegerField(u'点赞数量')
    publish_date = models.DateTimeField(u'发布日期')
    article_type_id = models.IntegerField(u'类型', db_index=True)

    class Meta:
        verbose_name = u'文章'
        verbose_name_plural = verbose_name