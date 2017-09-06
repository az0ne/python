# -*- coding: utf-8 -*-
"""
暂时不上!!!!
"""
__author__ = 'Jackie'

from django.db import models


class OptLog(models.Model):
    OPT_TYPE_STUDENT_QUIT = 1  # 退班
    OPT_TYPE_STUDENT_PAUSE = 2  # 休学
    OPT_TYPE_STUDENT_RESUME = 3  # 复学
    OPT_TYPE_STUDENT_CHANGE_CLASS = 4  # 转班

    EXT_OBJ_TYPE_CLASS = 1  # 班级

    opt_type = models.IntegerField(u'操作类型', db_index=True)

    class_id = models.IntegerField(u'班级ID', null=True, blank=True, db_index=True)
    student_id = models.IntegerField(u'学生ID', null=True, blank=True, db_index=True)

    ext_obj_type = models.IntegerField(u'扩展对象类型', null=True, blank=True, db_index=True)
    ext_obj_id = models.IntegerField(u'扩展对象ID', null=True, blank=True, db_index=True)

    operator_id = models.IntegerField(u'操作人员ID', db_index=True)
    create_time = models.DateTimeField(u'日志时间', auto_now_add=True)
    remark = models.CharField(u'备注', max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = u'教务操作日志'
        verbose_name_plural = verbose_name
