# -*- coding:utf-8 -*-
from django.db import models

# Create your models here.
class Admin(models.Model):
    name = models.CharField(u'姓名', max_length=100)
    pwd = models.CharField(u'密码',max_length=100)
    class Meta:
        verbose_name = u'后台用户表'
        verbose_name_plural = verbose_name


class AdminRole(models.Model):
    user_id = models.IntegerField(u'用户id')
    role_id = models.IntegerField(u'角色id')
    class Meta:
        verbose_name = u'后台用户角色表'
        verbose_name_plural = verbose_name


class Role(models.Model):
    name = models.CharField(u'用户角色',max_length=100)
    class Meta:
        verbose_name = u'角色表'
        verbose_name_plural = verbose_name

class RoleMenu(models.Model):
    role_id = models.IntegerField(u'角色id')
    menu_id = models.IntegerField(u'菜单id')
    class Meta:
        verbose_name = u'角色权限表'
        verbose_name_plural = verbose_name


class Menu(models.Model):
    name =models.CharField(u'菜单名字',max_length=100)
    url = models.URLField(u'菜单url', null=True, blank=True)
    class Meta:
        verbose_name = u'权限表'
        verbose_name_plural = verbose_name