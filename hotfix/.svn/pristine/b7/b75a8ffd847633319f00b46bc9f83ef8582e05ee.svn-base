# -*- coding: utf-8 -*-

__author__ = 'changfu'

from mz_platform.services.functions.mz_service import MZService, Orm2Str

from mz_platform.orms.mz_article import Article
from mz_platform.orms.mz_article import UserPraise
from mz_platform.orms.mz_common import ObjTagRelation
from mz_platform.orms.mz_common import CareerObjRelation
from mz_platform.orms.mz_common import Discuss
from mz_platform.orms.course_models import Tag
from mz_platform.orms.course_models import CareerCourse
from mz_platform.orms.mz_common import NewAd

class ArticleService(MZService):
    """Article 服务

    @note 方法get_article, get_all_article由基类支持
    """

    factory_functions = dict(article=Article)

    def __init__(self):
        """
        :return:
        """
        super(ArticleService, self).__init__()

    def get_related_objects(self, article_id, obj_type='TAG', otr_type='COURSE', is_active=True,
                            what='*', conditions=None, limit=None, order_by=None):
        """
        @brief 获取文章相关的objects

        @param article_id:  文章id
        @param obj_type:  相关对象类型, 可选为'TAG', 'CAREER', 'SEO', 'AD', 'DISCUSS',
                          分别为：相关Tag, 相关职业, 相关SEO, 相关广告, 相关讨论
        @param is_active:  是否激活
        @param what:  查询的字段
        @param conditions:  条件
        @param limit:  切片
        @param order_by: 排序
        @return:

        @note example:
              get_related_objects(article_id=5, obj_type='CAREER', is_activate=False, order_by='-id',
                                  what='id', conditions=['id>10'], limit='9, 14')
            　获取id为5的文章的全部相关职业(is_active=False)的id字段，条件为职业的id大于10.从结果的第9条开始取，取14条，并按id字段降序排列
        """
        relation_map = dict(TAG=([(ObjTagRelation, ('obj_id', 'obj_type'), (article_id, 'ARTICLE')), ],
                                 Tag,
                                 [('inner', (ObjTagRelation, Tag), ('tag_id', 'id'))]),
                            CAREER=([(CareerObjRelation, ('obj_id', 'is_actived', 'obj_type'), (article_id, 1 if is_active else 0, otr_type))],
                                    CareerCourse,
                                    [('inner', (CareerObjRelation, CareerCourse), ('career_id', 'id'))]),
                            DISCUSS=([(Discuss, ('object_id', 'object_type'), (article_id, 'ARTICLE')), ],
                                     Discuss,
                                     None),
                            AD=([(NewAd, ('type', 'is_actived'), ('ARTICLE', 1)), ], NewAd, None),
                            )
        more_conditions, where, join = relation_map[obj_type.upper()]
        data = Orm2Str.orm2str(what=what,
                               where=where,
                               join=join,
                               conditions=conditions,
                               more_conditions=more_conditions,
                               limit=limit,
                               order_by=order_by)
        return self.db.select(**data)

    def get_praised_users(self, article_id, what=('id',), conditions=None, limit=None, order_by=None):
        """
        @brief 获取文章的点赞用户的信息

        @param article_id: 文章id, 类型为int
        @param what: 需要的字段，类型为列表，如['id', 'name'], 缺省值为'id'
        @param conditions: 额外的条件， 如['id>5', 'name like "%python%"'], 缺省值为None
        @param limit: 切片， 类型为字符串， 如'5, 8', 缺省值为None
        @param order_by: 排序, 类型为字符串, 如'name', 缺省值为None
        @return: 课程信息的字典列表

        @todo UserPraise表升级之后, 升级这个接口
        """
        more_conditions = [(UserPraise, ('article_id', ), (article_id, )), ]
        data = Orm2Str.orm2str(what=what,
                               where=UserPraise,
                               join=None,
                               conditions=conditions,
                               more_conditions=more_conditions,
                               limit=limit,
                               order_by=order_by)
        return self.db.select(**data)

    def new_user_praise(self, article_id, user_id):
        """
        @brief 添加新的文章点赞

        @param args:
        @param kwargs:
        @return:

        @note: 一个典型的用法如下：
               new_user_praise(dict(article_id=2, user_id=5))

        @todo　UserPraise表升级之后，需要为不同的点赞对象实现这个接口
            　 support update 语句
        """
        # 插入userpriase记录
        sql = '''
            insert into mz_common_userpraise (article_id, user_id) values (%s, %s)
            '''
        new_id = self.execute_insert(sql, (article_id, user_id))
        # data = Orm2Str.orm2str(op_type='insert', where=UserPraise, values=dict(article_id=article_id, user_id=user_id))
        # new_id = self.db.insert(**data)
        if new_id > 0:  # 插入成功,增加article的praise_count记录,此处未使用事务
            sql = '''
                update mz_common_newarticle set praise_count = praise_count + 1 where id = %s
                ''' % article_id
            self.execute_update(sql)
        return new_id