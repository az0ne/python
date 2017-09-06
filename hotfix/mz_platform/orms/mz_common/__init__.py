#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
实现Model类的中间定义，弃用django的Model之后，可以自定义与表相关的类model对象

目前，自定义的类model对象仅仅从django的model对象获取　表名　这个属性
"""

from mz_platform.orms.mz_db_model import MZDBModel

from mz_platform.orms.mz_common.obj_tag_relation import ObjTagRelation
from mz_platform.orms.mz_common.career_obj_relation import CareerObjRelation
from mz_platform.orms.mz_common.career_ad import CareerAd
from mz_platform.orms.mz_common.user_center_ad import UserCenterAd
from mz_platform.orms.mz_common.new_discuss import NewDiscuss as Discuss
from mz_platform.orms.mz_common.banner import Banner
from mz_platform.orms.mz_common.obj_seo import ObjSEO

# TODO: here will be replaced by actual ORM object
from mz_common.models import NewAd as NewAd


origin_class = [ObjTagRelation, CareerObjRelation, CareerAd, UserCenterAd, Discuss, Banner, NewAd, ObjSEO]

Discuss.__name__ = 'Discuss'

for model in origin_class:
    locals()[model.__name__] = type(model.__name__, (MZDBModel,), dict(db_table=model._meta.db_table))

