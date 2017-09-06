#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
实现Model类的中间定义，弃用django的Model之后，可以自定义与表相关的类model对象

目前，自定义的类model对象仅仅从django的model对象获取　表名　这个属性
"""

from mz_platform.orms.mz_db_model import MZDBModel

from mz_platform.orms.mz_lps.class_students import ClassStudents
from mz_platform.orms.mz_lps.lps_class import Class

origin_class = [ClassStudents, Class]

for model in origin_class:
    locals()[model.__name__] = type(model.__name__, (MZDBModel,), dict(db_table=model._meta.db_table))