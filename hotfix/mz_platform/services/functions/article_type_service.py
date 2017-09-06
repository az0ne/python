# -*- coding: utf-8 -*-

__author__ = 'changfu'

from mz_platform.services.functions.mz_service import MZService, Orm2Str

from mz_platform.orms.mz_article import ArticleType
from mz_platform.orms.mz_article import Article

class ArticleTypeService(MZService):
    """课程service

    """

    factory_functions = dict(article_type=ArticleType)

    def __init__(self):
        """
        :return:
        """
        super(ArticleTypeService, self).__init__()

    def get_related_articles(self, article_type_id, what='*', conditions=None, limit=None, order_by=None):
        """
        @brief 获取文章类型所相关的文章,

        @param article_type_id: 文章类型的id, 类型为int
        @param what: 需要的字段，类型为列表，如['id', 'name'], 缺省值为'*'
        @param conditions: 额外的条件， 如['id>5', 'name like "%python%"'], 缺省值为None
        @param limit: 切片， 类型为字符串， 如'5, 8', 缺省值为None
        @param order_by: 排序, 类型为字符串, 如'name', 缺省值为None
        @return: 课程信息字典的列表

        @note example1:
              get_related_articles(article_type_id=5, what='id', conditions=['id>10'], limit='9, 14', order_by='-id',)
            　获取id为5的文章类型的全部相关文章的id字段，条件为文章的id大于10.从结果的第9条开始取，取14条，并按id字段降序排列
        """
        more_conditions = [(Article, ('article_type_id', ), (article_type_id, )), ]
        data = Orm2Str.orm2str(what=what,
                               where=Article,
                               join=None,
                               conditions=conditions,
                               more_conditions=more_conditions,
                               limit=limit,
                               order_by=order_by)
        return self.db.select(**data)
