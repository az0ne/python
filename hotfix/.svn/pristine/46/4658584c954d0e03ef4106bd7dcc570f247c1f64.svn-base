#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
实现Model类的中间定义，弃用django的Model之后，可以自定义与表相关的类model对象

目前，自定义的类model对象仅仅从django的model对象获取　表名　这个属性
"""

from mz_platform.orms.mz_db_model import MZDBModel

from mz_platform.orms.course_models.course import Course
from mz_platform.orms.course_models.career_course import CareerCourse
from mz_platform.orms.course_models.lesson import Lesson
from mz_platform.orms.course_models.course_resource import CourseResource
from mz_platform.orms.course_models.course_catagory import CourseCatagory
from mz_platform.orms.course_models.tag import Tag
from mz_platform.orms.course_models.career_catagory import NewCareerCatagory as CareerCatagory

CareerCatagory.__name__ = 'CareerCatagory'

origin_class = [Course, CareerCourse, Lesson, CourseResource, CourseCatagory, Tag, CareerCatagory]

for model in origin_class:
    locals()[model.__name__] = type(model.__name__, (MZDBModel,), dict(db_table=model._meta.db_table))
