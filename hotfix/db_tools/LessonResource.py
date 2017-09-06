# -*- coding: utf-8 -*-
__author__ = 'bobby'

import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"/..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
import django
django.setup()

from mz_course.models import (
                LessonResource,
                CourseResource,
            )

class LessonResourceProcessor():
    """
    处理老数据，将章节资源记录转换为课程资源记录
    """

    @classmethod
    def translate(self):
        lesson_resources = LessonResource.objects.all()
        i = 0
        for lesson_resource in lesson_resources:
            if CourseResource.objects.filter(download_url=lesson_resource.download_url).count() == 0:
                course_resource = CourseResource(name=lesson_resource.name,download_url=lesson_resource.download_url,
                                             download_count=lesson_resource.download_count,course=lesson_resource.lesson.course)
                course_resource.save()

            print i
            i += 1

if __name__ == "__main__":
    LessonResourceProcessor.translate()


