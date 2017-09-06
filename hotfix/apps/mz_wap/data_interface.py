# -*- coding: utf-8 -*-

"""
wap数据接口
执行复杂数据操作, 可做数据级别缓存

请优先考虑利用已有的数据接口
"""
import logging
from collections import OrderedDict

from django.db.models.aggregates import Sum, Count

from mz_common.models import PageSeoSet, Ad, RecommendKeywords
from mz_course.models import CareerCourse, Course, CourseCatagory

__author__ = 'changfu'

logger = logging.getLogger('mz_wap.data_interface')


def get_hot_recommend_keywords(num):
    """ author: feng
    获取热门搜索关键字
    先取热门的，再按学习人数取
    :param num: 获取数量
    :return: 热门搜索关键字
    """
    num = abs(int(num))
    return RecommendKeywords.objects.all()[:num]\
        .values_list('name', flat=True)


def get_hot_career_courses(num=-1):
    """ author: feng
    获取热门职业课程
    先取热门的，再按学习人数取
    :param num: 获取数量(-1表示所有)
    :return: 职业课程列表
    """
    career_courses = CareerCourse.objects\
        .order_by('-is_hot', '-student_count')
    if num == -1:
        return career_courses
    num = abs(int(num))
    if career_courses.count() > num:
        return career_courses[:num]
    return career_courses


def get_hot_career_courses_details(num=-1):
    """ author: feng
    获取热门职业课程详情
    对每门课程增加课程总数(courses_total)、学习需要多少天(need_days)
    :param num: 获取数量(-1表示所有)
    :return: 职业课程详情列表
    """
    career_courses = get_hot_career_courses(num)
    for cc in career_courses:
        stags = cc.stage_set.order_by('index')

        cc.courses_total, cc.need_days = Course.objects.filter(
            stages_m__in=stags, is_active=True)\
            .aggregate(Count('id'), Sum('need_days')).values()

    return career_courses


def get_course_category_list(career, career_category_list=None):
    """ author: feng
    获取课程分类列表
    :param career: 课程方向
    :param career_category_list: 课程方向分类列表
    :return: 课程分类列表
    """
    if career != 'all':
        if isinstance(career, CareerCourse):
            career = career.name
        return CourseCatagory.objects.filter(
            career_catagory__name=career)\
            .values_list('name', flat=True)
    else:
        assert (career_category_list,
                'career_category_list is None')
        return CourseCatagory.objects.filter(
            career_catagory__in=career_category_list)\
            .values_list('name', flat=True)


def get_category_dict(career_category_list):
    """ author: feng
    获取分类字典 课程方向对应课程分类
    :param career_category_list: 课程方向分类列表
    :return: 分类字典
    """
    dic = OrderedDict()
    for career in career_category_list:
        dic[career.name] = list(get_course_category_list(career))
    return dic


def get_seo(page_name):
    """ author: feng
    获取seo数据
    :param page_name: 页标记
    :return: 一个PageSeoSet对象
    """
    assert isinstance(page_name, str), 'page_name must be str'
    try:
        seo = PageSeoSet.objects.get(page_name=page_name)
    except Exception, e:
        seo = PageSeoSet()
        logger.error(e)
    return seo


def get_index_seo():
    """ author: feng
    获取首页seo数据
    :param :
    :return: 一个PageSeoSet对象
    """
    return get_seo(page_name='1')


def get_course_seo():
    """ author: feng
    获取课程库页seo数据
    :param :
    :return: 一个PageSeoSet对象
    """
    return get_seo(page_name='4')


def get_ad(ad_type):
    """ author: feng
    获取seo数据
    :param ad_type: 广告类型 (0, "首页"),(1, "课程列表页"),(2, "老师列表页")
    :return: 一个PageSeoSet对象
    """
    assert isinstance(ad_type, int), 'ad_type must be int'
    try:
        ad = Ad.objects.filter(type=ad_type)[0]
    except IndexError:
        ad = []
    return ad
