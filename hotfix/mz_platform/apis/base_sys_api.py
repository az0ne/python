#!/usr/bin/env python
# -*- coding: utf8 -*-
import collections
import re

from mz_platform.services.functions.course_service import CourseService
from mz_platform.services.functions.discuss_service import DiscussService
from mz_platform.services.functions.lesson_service import LessonService
from mz_platform.services.functions.tag_service import TagService
from mz_platform.services.functions.user_service import UserService
from mz_platform.services.functions.career_course_service import \
    CareerCourseService
from mz_platform.services.functions.article_service import ArticleService
from mz_platform.services.functions.article_type_service import \
    ArticleTypeService
from mz_platform.services.functions.banner_service import BannerService
from mz_platform.services.functions.career_category_service import CareerCategoryService

from mz_platform.utils.debug_tool import deb_print


"""
导出Api

-   所有的导出外部调用的api，必须用装饰器
    @api_except_catcher 装饰保证捕获所有异常和包装成ApiResult对象
-   直接数据对象
-   经过复杂查询得到的对象
"""


class BaseSysApi(object):
    """
    类设计：
    业务系统API类，聚合多处出现的业务逻辑，这是一个持续迭代的过程
    集合业务层代码，可以集合多个业务service类,
    捕获services抛出的异常，返回ApiResult对象
    收集业务逻辑log，易于测试
    """

    course_service = CourseService()
    user_service = UserService()
    career_course_service = CareerCourseService()
    lesson_service = LessonService()
    article_type_service = ArticleTypeService()
    article_service = ArticleService()
    tag_service = TagService()
    discuss_service = DiscussService()
    banner_service = BannerService()
    career_category_service = CareerCategoryService()

    def s_p(self, dict_param):
        """
        @brief 转化dict类型参数为service需要的参数类型

        自动转换关键字pk（lowcase）到id
        """
        if 'pk' in dict_param:
            v = dict_param['pk']
            dict_param['id'] = v
            del dict_param['pk']
        return ["{}={}".format(
            i, self.p_safe(dict_param[i])) for i in dict_param]

    def s_limit(self, limit, offset=0):
        """
        @brief     转化limit, offset类型参数为service需要的参数类型

        @param  limit   >=0 0 all
        @param  offset   >=
        @return     string "offset,limit" "limit" if offset == 0
                    "" if limit == 0
        """
        assert limit >= 0
        assert offset >= 0

        if limit == 0:
            limit = ''
        else:
            limit = str(limit)

        if offset == 0:
            offset = ''
        else:
            offset = str(offset) + ','

        return "%(offset)s%(limit)s" % dict(offset=offset, limit=limit)

    def n_obj(self, clz, sql_result):
        """
        @brief 转换db结果到本地对象
        """

        if isinstance(clz, str):
            clz = self.get_clz(clz)

        if isinstance(sql_result, dict):
            return clz(sql_result)
        elif isinstance(sql_result, collections.Iterable):
            return [clz(i) for i in sql_result]
        return None

    @staticmethod
    def p_safe(p):
        """
        @brief 过滤参数中的特殊字符，防止sql注入

        @param p: 参数
        @retval : 过滤后的安全的参数
        """
        if isinstance(p, (str, unicode)):
            result = re.search(r'["\\/*\'=\-#;<>\+%]', p)
            assert not result, 'It may be sql injection, param: {}'.format(p)
        return p

    def get_clz(self, clz_name):
        """
        @brief      通过name找到对应的object对象

        @param      name class名字

        @return     返回对应的class对象，如果失败抛出异常ImportError,AttributeError
        """
        ns = re.findall('[A-Z][a-z0-9]*', clz_name)
        name = '_'.join([i.lower() for i in ns if i])
        name = "mz_platform.objects.%s" % (name,)
        mod = __import__(name, globals(), locals(), [clz_name], -1)
        return getattr(mod, clz_name)

    def _query(self, host, related, first=False, order_by=None, **cond):
        """
        @brief query host obj with related obj

        @todo need implement it

        根据conditions查询related对应的CareerCourse对象, 默认返回全部
        如果first=True，返回第一个，默认是顺序为sql表顺序

        比如：
        查询的全部CareerCourse
        get_careercourse(None)
        查询的全部CareerCourse 以id降序
        get_careercourse(None, order_by="-id")
        查询的全部CareerCourse 以id升序
        get_careercourse(None, order_by="id")
        查询某个course_id对应的全部CareerCourse
        get_careercourse('Course', dict(course_id=1))
        查询某个course_id对应的第一个CareerCourse
        get_careercourse(Course, first=True, dict(course_id=1))

        @param  related     相对关系，字符串类型或者objects下对象类型，如果None查询careercourse
        @param  first       默认False返回所有数据，True返回第一个
        @param  order_by    默认None顺序为sql表顺序,
        """

        pass

    def _deb_print(self, **kwargs):
        deb_print(**kwargs)
