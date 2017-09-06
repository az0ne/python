#!/usr/bin/env python
# -*- coding: utf8 -*-

from django.db import models
import career_course.CareerCourse as CareerCourse


# add_by_zhangyunrui 网站改版20160118
class StudentProjectImage(models.Model):
    image_url = models.ImageField(
        u"学生作品图片", upload_to="student_project_image/%Y/%m", max_length=200)
    career_course = models.ForeignKey(CareerCourse, verbose_name=u"职业课程")

    class Meta:
        verbose_name = u"学生作品图片"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)
