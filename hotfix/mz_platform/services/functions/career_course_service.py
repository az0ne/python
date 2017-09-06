# -*- coding: utf-8 -*-

__author__ = 'changfu'

from mz_platform.services.functions.mz_service import MZService, Orm2Str
from mz_platform.orms.course_models import CareerCourse
from mz_platform.orms.mz_common import CareerObjRelation
from mz_platform.orms.course_models import Course
from mz_platform.orms.mz_user import UserProfile
from mz_platform.orms.mz_article import Article
from mz_platform.orms.mz_common import CareerAd
from mz_platform.orms.course_models import Lesson

class CareerCourseService(MZService):
    """ 职业课程service

    """

    factory_functions = dict(career_course=CareerCourse)

    def __init__(self):
        """
        @brief
        @return:
        """
        super(CareerCourseService, self).__init__()

    def get_related_objects(self, career_course_id, obj_type='COURSE', ad_type='COURSE', is_active=True,
                            what='*', conditions=None, limit=None, order_by=None):
        """
        @brief 获取职业课程所相关的objects, 如课程，文章，老师，视频, 广告

        @param career_course_id: 职业课程的id
        @param obj_type: objects的类型，可选为'COURSE', 'ARTICLE', 'TEACHER', 'LESSON', 'CAREERAD', 默认为'COURSE'
        @param ad_type: 广告的类型，指明广告的位置．当ob_type='CAREERAD'时，该参数有效．可选值为'COURSE', 'ARTICLE', 默认为'COURSE'
        @param is_active: True or False, 如果为True,则返回激活的课程，如果为False, 返回全部课程， 默认为True
        @param what:
        @param conditions:
        @param limit:
        @param order_by:
        @return: 课程信息字典的列表

        @note example1:
              get_related_objects(career_course_id=5, obj_type='COURSE', is_activate=False, order_by='-id',
                                  what='id', conditions=['id>10'], limit='9, 14')
            　获取id为5的职业课程的全部相关小课程(is_active=False)的id字段，条件为小课程的id大于10.从结果的第9条开始取，取14条，并按id字段降序排列

              example2:
              get_related_objects(career_course_id=5, obj_type='CAREERAD', ad_type='ARTICLE', is_activate=False, order_by='-id',
                                  what='id', limit='9, 14')
            　获取id为5的职业课程的文章详情页的广告的(is_active=False)的id字段。从结果的第9条开始取，取14条，并按id字段降序排列
        """
        relation_map = dict(CAREERAD=([(CareerAd, ('career_id', 'type', 'is_actived'), (career_course_id, ad_type, 1 if is_active else 0))],
                                      CareerAd,
                                      None),
                            COURSE=([(CareerObjRelation, ('career_id', 'is_actived', 'obj_type'), (career_course_id, 1 if is_active else 0, 'COURSE'))],
                                    Course,
                                    [('inner', (CareerObjRelation, Course), ('obj_id', 'id'))]),
                            ARTICLE=([(CareerObjRelation, ('career_id', 'is_actived', 'obj_type'), (career_course_id, 1 if is_active else 0, 'ARTICLE'))],
                                     Article,
                                     [('inner', (CareerObjRelation, Article), ('obj_id', 'id'))]),
                            TEACHER=(),
                            LESSON=())
        more_conditions, where, join = relation_map[obj_type.upper()]
        data = Orm2Str.orm2str(what=what,
                               where=where,
                               join=join,
                               conditions=conditions,
                               more_conditions=more_conditions,
                               limit=limit,
                               order_by=order_by)
        return self.db.select(**data)


