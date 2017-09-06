#!/usr/bin/env python
# -*- coding: utf8 -*-
from mz_platform.services.functions.mz_service import MZService, Orm2Str

from mz_platform.orms.course_models import Course
from mz_platform.orms.course_models import CourseResource
from mz_platform.orms.course_models import CourseCatagory
from mz_platform.orms.course_models import CareerCourse
from mz_platform.orms.mz_common import CareerObjRelation
from mz_platform.orms.course_models import Tag
from mz_platform.orms.mz_common import ObjTagRelation
from mz_platform.orms.mz_common import ObjSEO


class CourseService(MZService):
    """课程service

    @note get_course 和 get_all_course 在基类MZService中动态生成, 定义如下：
          get_course(what='*', conditions=None, limit=None, order_by=None)
          get_all_course(what='*', limit=None, order_by=None)
    """

    factory_functions = dict(course=Course,
                             course_resource=CourseResource,
                             course_category=CourseCatagory)

    def __init__(self):
        """
        :return:
        """
        super(CourseService, self).__init__()

    def get_related_career_courses(self, course_id, is_active=True, what='*',
                                   conditions=None, limit=None, order_by=None):
        """
        @brief 获取课程所属的职业课程

        @param course_id: 课程的id
        @param what: 查询的字段
        @param is_active: True or False, 如果为True,则返回激活的职业课程，如果为False, 返回全部职业课程， 默认为True
        @param conditions: 附加条件
        @param limit: 切片
        @param order_by: 排序
        @return: 职业课程信息字典的列表

        @note　该函数同时支持其它的条件，如order_by.　一个典型的调用方式如下：
        　　　　get_related_career_courses(course_id=5, is_activated=False, order_by='-id'
            　 获取id为5的course所相关的全部的职业课程，并按id负向排序
        """
        more_conditions = [(CareerObjRelation, ('obj_id', 'is_actived', 'obj_type'),
                            (course_id, 1 if is_active else 0, 'COURSE'))]
        data = Orm2Str.orm2str(what=what,
                               where=CareerCourse,
                               join=[('inner', (CareerObjRelation, CareerCourse), ('career_id', 'id'))],
                               conditions=conditions,
                               more_conditions=more_conditions,
                               limit=limit,
                               order_by=order_by)
        return self.db.select(**data)

    def get_related_tags(self, course_id, what='*', conditions=None, limit=None, order_by=None):
        """
        @brief 获取课程的相关tag信息

        @param course_id: 课程的id, 类型为int
        @param what: 需要的字段，类型为字符串，如'id, name'
        @param conditions: 额外的条件， 如['id>5', 'name like "%python%"']
        @param limit: 切片， 如'5, 8'
        @param order_by: 分组
        @return: tag信息字典的列表

        @note 该函数同时支持其它的条件，如order_by.　一个典型的调用方式如下：
        　　　 get_related_tags(course_id=5, conditions=['order_by=-id']
            　获取id为5的course所相关的全部的tag，并按id负向排序
        """
        more_conditions = [(ObjTagRelation, ('obj_id', 'obj_type'), (course_id, 'COURSE')), ]
        data = Orm2Str.orm2str(what=what,
                               where=Tag,
                               join=[('inner', (ObjTagRelation, Tag), ('tag_id', 'id'))],
                               conditions=conditions,
                               more_conditions=more_conditions,
                               limit=limit,
                               order_by=order_by)
        return self.db.select(**data)

    def get_course_by_career_tag(self, career_category_id=0, tag_id=0,
                                 what='*', conditions=None, limit=None, order_by=None):
        """
        @brief 以职业方向和标签为条件获取课程

        @param career_category_id: 职业方向的id, int. 值为0时，代表全部职业方向，缺省值为0
        @param tag_id: 标签的id, int. 值为0时，代表全部职业方向， 缺省值为0
        @param what: 需要的字段，类型为列表，如['id', 'name'], 缺省值为'*'
        @param conditions: 额外的条件， 如['id>5', 'name like "%python%"'], 缺省值为None
        @param limit: 切片， 类型为字符串， 如'5, 8', 缺省值为None
        @param order_by: 排序, 类型为字符串, 如'name', 缺省值为None
        @return: 课程信息的字典列表

        @note 调用example:
              get_course_by_career_tag(career_category_id=5, tag_id=8,
                                       what=['id', 'name'], conditions=['student_count>20'], limit='8, 10'
                                       order_by='-click_count')
              获取职业方向为5, 标签为8, 并且student_count>20的课程的id,name字段，从结果的第8条开始取，取10条, 按播放次数排列
        """
        more_conditions = [(ObjTagRelation, ('tag_id', 'careercatagory_id', 'obj_type'),
                            (tag_id, career_category_id, 'COURSE')), ]
        data = Orm2Str.orm2str(what=what,
                               where=Course,
                               join=[('inner', (ObjTagRelation, Course), ('obj_id', 'id'))],
                               conditions=conditions,
                               more_conditions=more_conditions,
                               limit=limit,
                               order_by=order_by)
        return self.db.select(**data)

    def get_course_seo(self, course_id, what='*', conditions=None, limit=None, order_by=None):
        """
        @brief 获取course的seo

        @param course_id:
        @return:
        """
        more_conditions = [(ObjSEO, ('obj_id', 'obj_type'), (course_id, 'COURSE')), ]
        data = Orm2Str.orm2str(what=what,
                               where=ObjSEO,
                               join=None,
                               more_conditions=more_conditions,
                               conditions=conditions,
                               limit=limit,
                               order_by=order_by)
        return self.db.select(**data)

    # def test_transaction(self):
    #     from django.db import transaction
    #     from mz_platform.services.functions.discuss_service import DiscussService
    #     discuss_service = DiscussService()
    #     import datetime
    #     with transaction.atomic():
    #         discuss_service.new_discuss(dict(object_id=2, object_type='LESSON', comment='just for test测试哈哈哈',
    #                                          user_id=8, nick_name='我是QA3', head='temp/temp/2.img',
    #                                          create_date=datetime.datetime.now(), parent_id=8))
    #         discuss_service.new_discuss(dict(object_id=2, object_type='LESSON', comment='just for test测试哈哈哈',
    #                                          user_id=8, nick_name='我是QA2', head='temp/temp/2.img',
    #                                          create_date=datetime.datetime.now(), parent_id=8))
    #     print 'success'



# from user_service import UserService
# course_service = CourseService()
# user = UserService()
# # # for x in course_service.get_all_course():
# # #     for k, v in x.items():
# # #         print k, v
# # # for x in course_service.get_all_lesson(limit='5, 8'):
# # #     for k, v in x.items():
# # #         print k, v
# # # for x in course_service.get_lesson(conditions=['id > 5', ], limit='5, 8', order_by='-id'):
# # #     for k, v in x.items():
# # #         print k, v
# #
# # # if SysCourseService.get_lesson():
# # #     pass
# # course = course_service.get_course(conditions=['id=736'])[0]  # 课程信息
# print len( course_service.get_all_course_category())
# print len(course_service.get_all_lesson())
# print len(course_service.get_all_course())
# print course
# print course['teacher']
# teacher = user.get_user(conditions=['id=%s' % course['teacher']],)[0]  # 教师信息
# print teacher

# print user.get_all_teacher()[:3]
# import career_course_service
# career_course_service = career_course_service.CareerCourseService()
# print career_course_service.get_career_course(conditions=['id=1'])
# print career_course_service.get_all_career_course()[0]
# print len(course_service.get_related_career_courses(course_id=736, is_active=True))
# print len(course_service.get_related_career_courses(course_id=736, is_active=False))
# print course_service.get_related_tags(course_id=736)
# from career_course_service import CareerCourseService
# career_course_service = CareerCourseService()
# print career_course_service.get_related_objects(career_course_id=2, obj_type='COURSE', is_active=False)
# from lps_service import LpsService
# lps_service = LpsService()
# print lps_service.get_registered_career_course(user_id=69736)

# from mz_platform.services.functions.lesson_service import LessonService
# lesson = LessonService()
# print len(lesson.get_related_discuss(lesson_id=5))

# from mz_platform.services.functions.discuss_service import DiscussService
# discuss_service = DiscussService()
# import datetime
# print discuss_service.new_discuss(dict(object_id=2, object_type='LESSON', comment='just for test测试哈哈哈', user_id=8,
#                                  nick_name='我是QA', head='temp/temp/2.img', create_date=datetime.datetime.now(),
#                                  parent_id=8))
# print len(discuss_service.execute_select('select * from mz_course_course'))

# from mz_platform.services.functions.search_service import SearchService
# search_service = SearchService()
# print search_service.search_by_keywords(keywords=['python', 'java'], obj_type='')

# course_service.test_transaction()

# from mz_platform.services.functions.article_type_service import ArticleTypeService
# ats = ArticleTypeService()
# print ats.get_article_type(conditions=['is_homepage=1'])
