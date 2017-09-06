#!/usr/bin/env python
# -*- coding: utf8 -*-

import base_sys_api
from mz_platform.services.functions.lps_service import LpsService
from mz_platform.utils.decorator_tool import api_except_catcher

"""
Course Business Api Collection


-   所有的导出外部调用的api，必须用装饰器
    @api_except_catcher 装饰保证捕获所有异常和包装成ApiResult对象
-   直接数据对象
-   经过复杂查询得到的对象
"""


class CourseSysApi(base_sys_api.BaseSysApi):
    """
    @brief 课程库系统API接口类

    """
    lps_service = LpsService()

    _api = None

    @staticmethod
    def default_instance():
        """
        @brief 默认api对象
        """
        if not CourseSysApi._api:
            CourseSysApi._api = CourseSysApi()
        return CourseSysApi._api

    @api_except_catcher
    def get_one_course(self, **kwargs):
        """
        @brief 获取课程对象

        @param kwargs : 查询Course对象的条件，多个条件是and的关系
        @retval : 符合条件的Course对象，如果存在多个返回第一个，如果没有
        符合条件的对象，返回None
        """
        c = self.course_service.get_course(conditions=self.s_p(kwargs))
        if not c:
            return None
        return self.n_obj('Course', c[0])

    @api_except_catcher
    def get_all_course(self, **kwargs):
        """
        @brief 获取所有课程对象

        @param kwargs : 查询Course对象的条件，多个条件是and的关系
        @retval : 符合条件的Course对象,如果没有符合条件的对象返回[]
        """
        cs = self.course_service.get_course(conditions=self.s_p(kwargs))
        return self.n_obj('Course', cs)

    @api_except_catcher
    def get_one_lesson(self, **kwargs):
        """
        @brief 获取章节对象

        @param kwargs : 查询Lesson对象的条件，多个条件是and的关系
        @retval : 符合条件的Lesson对象，如果存在多个返回第一个，如果没有
        符合条件的对象，返回None
        """
        l = self.lesson_service.get_lesson(conditions=self.s_p(kwargs))
        if not l:
            return None
        return self.n_obj('Lesson', l[0])

    @api_except_catcher
    def get_all_lesson(self, **kwargs):
        """
        @brief 获取所有章节对象,按照index顺序升序排列

        @param kwargs : 查询Lesson对象的条件，多个条件是and的关系
        @retval : 符合条件的Lesson对象，如果没有符合条件的对象返回[]
        """
        ls = self.lesson_service.get_lesson(conditions=self.s_p(kwargs))
        return self.n_obj('Lesson', ls)

    @api_except_catcher
    def get_careercourse_by_course(self, course_id, exclude=False, is_active=False):
        """
        @brief 获取所有与Course相关的CareerCourse对象

        @param  course_id   course id
        @param  exclude 返回值不包含course_id的对象,默认为False
        @retval : 符合条件的CareerCourse对象，如果没有符合条件的对象返回[]
        """
        cs = self.course_service.get_related_career_courses(
            course_id, is_active=is_active)
        cs = self.n_obj('CareerCourse', cs)
        if exclude:
            cs = filter(lambda x: x.id != course_id, cs)
        return cs

    @api_except_catcher
    def get_active_careercourse_by_course(self, course_id, first=True):
        """
        @brief 获取所有与Course相关的被激活职业课程

        当前只有一个

        @param  course_id   course id
        @param  first    是否只要第一个，默认只取第一个，否则取全部
        @retval 与课程id相关的CareerCourse, first真返回CareerCourse对象或者None失败的时候，
                first为假返回[CareerCourse]如果不存在或者失败返回[]
        """
        c = self.course_service.get_related_career_courses(
            course_id, True)
        if first:
            if not c:
                return None
            return self.n_obj("CareerCourse", c[0])
        else:
            if not c:
                return []
            return self.n_obj("CareerCourse", c)

    @api_except_catcher
    def get_all_article_by_course(self, course_id):
        """
        @brief 获取所有与Course相关的文章

        获取course_id激活的职业课程的文章

        @param career_course_id : course id
        @retval : 与课程id相关的Article, 如果不存在或者失败返回[]
        """
        r = self.get_active_careercourse_by_course(course_id)
        if not r:
            return []
        r = r.obj
        articles = self.career_course_service.get_related_objects(
            r.id, obj_type='ARTICLE', limit='10')
        return self.n_obj("Article", articles)

    @api_except_catcher
    def get_all_courseresource_by_course(self, course_id):
        """
        @brief 获取所有与Course相关的课程课件资源

        @param course_id : course id
        @retval : 与课程id相关的CourseResource, 如果不存在返回[]
        """
        cs = self.course_service.get_course_resource(
            conditions=self.s_p(dict(course_id=course_id)))
        return self.n_obj("CourseResource", cs)

    @api_except_catcher
    def get_ad_by_careercourse(self, careercourse_id):
        """
        @brief      获取职业课程相关的广告
        @param      careercourse_id 职业课程id
        @return     与课程id相关的Ad, 如果不存在返回[]

        @todo 需要service实现
        """
        ads = self.career_course_service.get_related_objects(
            careercourse_id, obj_type='CAREERAD')
        return self.n_obj("Ad", ads)

    @api_except_catcher
    def get_course_by_careercourse(self, careercourse_id, only_active=False,
                                   limit=0):
        """
        @brief 获取职业课程相关的所有课程对象

        @param careercourse_id : 查询Course对象的相关的职业课程ID
        @param only_active : 只获取职业课程ID相关的active课程，默认False
        @param limit : 当limit=0的时候表示获取所有课程，limit大于0表示获取limit条课程
        @retval : 符合条件的Course对象,如果没有符合条件的对象返回[]
        """
        cs = self.career_course_service.get_related_objects(
            career_course_id=careercourse_id,
            is_active=only_active,
            limit=self.s_limit(limit))

        return self.n_obj('Course', cs)

    @api_except_catcher
    def get_discuss_by_lesson(self, lesson_id):
        """
        @brief 获取章节下的所有评论

        @param lesson_id : 章节ID
        @retval : 符合条件的Discuss对象,如果没有符合条件的对象返回[]
        """
        d_list = self.lesson_service.get_related_discuss(lesson_id)
        d_list = self.n_obj('Discuss', d_list)
        pdl = [d for d in d_list if d.parent_id == 0]
        self._compound_discuss(pdl, d_list)
        return pdl

    def _compound_discuss(self, pdl, d_list):
        for pd in pdl:
            cdl = [d for d in d_list if d.parent_id == pd.id]
            if cdl:
                pd['child_list'] = cdl
                self._compound_discuss(cdl, d_list)
            else:
                return

    @api_except_catcher
    def get_hot_career_course(self, is_hot=True, limit=0):
        """
        @brief 获取热门职业课程

        @param is_hot : 是否是热门
        @param limit : 当limit=0的时候表示获取所有职业课程，
        limit大于0表示获取limit条职业课程
        @retval : 符合条件的Discuss对象,如果没有符合条件的对象返回[]
        """
        assert limit >= 0, 'limit must >= 0'
        if limit == 0:
            limit = None

        hots = self.career_course_service.get_career_course(
            conditions=self.s_p(dict(is_hot=is_hot)), limit=limit)
        return self.n_obj('CareerCourse', hots)

    @api_except_catcher
    def get_all_career_category(self):
        """
        @brief 获取所有职业课程分类

        @retval : 返回所有职业课程分类
        """

        r = self.career_category_service.get_all_career_category()
        return self.n_obj('CareerCategory', r)

    def is_registered_career_course(self, user_id, career_course_id):
        """
        判断用户是否报名一个职业课程,
        @param user_id:
        @param career_course_id: 可以为职业课程id的列表或者一个职业课程id
        @return:
        """
        if not user_id:
            return False
        rccs = self.lps_service.get_registered_career_course(user_id)
        id_list = [rcc['id'] for rcc in rccs]
        if isinstance(career_course_id, (int, long)):
            return True if career_course_id in id_list else False
        elif isinstance(career_course_id, list):
            tmp = list(item for item in id_list if item in career_course_id)
            return True if tmp else False
