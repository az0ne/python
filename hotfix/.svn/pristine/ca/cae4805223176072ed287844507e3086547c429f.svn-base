# -*- coding: utf-8 -*-

__author__ = 'changfu'

from mz_platform.services.functions.mz_service import MZService, Orm2Str

from mz_platform.orms.course_models import CareerCatagory
from mz_platform.orms.course_models import Course
from mz_platform.orms.mz_user import UserProfile
from mz_platform.orms.mz_article import Article
from mz_platform.orms.mz_common import ObjTagRelation

class CareerCategoryService(MZService):
    """ 职业课程service

    """

    factory_functions = dict(career_category=CareerCatagory)

    def __init__(self):
        """
        @brief
        @return:
        """
        super(CareerCategoryService, self).__init__()

    def get_related_objects(self, career_id, obj_type='COURSE',
                            what='*', conditions=None, limit=None, order_by=None):
        """
        @brief 获取职业课程所相关的objects, 如课程，文章，老师，视频

        @param career_id: 职业的id
        @param obj_type: objects的类型，可选为'COURSE', 'ARTICLE', 'TEACHER', 默认为'COURSE'
        @param what: 需要的字段，类型为列表，如['id', 'name'], 缺省值为'*'
        @param conditions: 额外的条件， 如['id>5', 'name like "%python%"'], 缺省值为None
        @param limit: 切片， 类型为字符串， 如'5, 8', 缺省值为None
        @param order_by: 排序, 类型为字符串, 如'name', 缺省值为None
        @return: 课程信息字典的列表

        @note example1:
              get_related_objects(career_id=5, obj_type='COURSE',
                                  what='id', conditions=['id>10'], limit='9, 14', order_by='-id',)
            　获取id为5的职业的全部相关小课程的id字段，条件为小课程的id大于10.从结果的第9条开始取，取14条，并按id字段降序排列

              example2:
              get_related_objects(career_id=5, obj_type='ARTICLE',
                                  what='id', conditions=['article_type_id=2'], limit='9, 14', order_by='-id')
            　获取id为5的职业的全部文章的id字段。并且文章的类型为article_type_id=2(如，干货分享).从结果的第9条开始取，取14条，并按id字段降序排列
        """
        relation_map = dict(COURSE=([(ObjTagRelation, ('careercatagory_id', 'obj_type'), (career_id, 'COURSE'))],
                                    Course,
                                    [('inner', (ObjTagRelation, Course), ('obj_id', 'id'))]),
                            ARTICLE=([(ObjTagRelation, ('careercatagory_id', obj_type), (career_id, 'ARTICLE'))],
                                     Article,
                                     [('inner', (ObjTagRelation, Article), ('obj_id', 'id'))]),
                            TEACHER=())
        more_conditions, where, join = relation_map[obj_type.upper()]
        data = Orm2Str.orm2str(what=what,
                               where=Course,
                               join=join,
                               conditions=conditions,
                               more_conditions=more_conditions,
                               limit=limit,
                               order_by=order_by)
        return self.db.select(**data)

    def get_distinct_related_course(self, careercatagory_id, limit):
        """
        @brief 获取职业课程所相关的课程（去重后的）

        @param careercatagory_id: 职业的id
        @param limit: 去前几个， 类型为int
        @return: 课程信息字典的列表

        """
        assert isinstance(limit, int)
        temp_sql = """select distinct mz_course_course.* from mz_course_course
            inner join mz_common_objtagrelation on mz_common_objtagrelation.obj_id = mz_course_course.id
            where mz_common_objtagrelation.careercatagory_id={cc_id}
            and mz_common_objtagrelation.obj_type="COURSE"
            order by -mz_course_course.id limit {limit}"""
        return self.db.select(
            sql=temp_sql.format(cc_id=careercatagory_id, limit=limit))
