# -*- coding: utf-8 -*-

"""
实现Model类的中间定义，弃用django的Model之后，可以自定义与表相关的类model对象

目前，自定义的类model对象仅仅从django的model对象获取　表名　这个属性
"""

__author__ = 'changfu'

from mz_platform.orms.mz_db_model import MZDBModel

from mz_platform.orms.mz_article.article import NewArticle as Article  # 用Article的名字而不是NewArticle
from mz_platform.orms.mz_article.article_type import ArticleType
from mz_platform.orms.mz_article.user_praise import UserPraise

Article.__name__ = 'Article'

origin_class = [Article, ArticleType, UserPraise]

for model in origin_class:
    locals()[model.__name__] = type(model.__name__, (MZDBModel,), dict(db_table=model._meta.db_table))