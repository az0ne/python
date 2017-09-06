# -*- coding: utf-8 -*-

"""
wap 业务逻辑函数

请有限考虑使用已有的业务逻辑函数;
请充分考虑复用
"""
import re

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.core.urlresolvers import reverse_lazy
from django.http.response import Http404

from mz_course.models import Course

from utils.logger import logger as log

__author__ = 'changfu'


DISPLAY_AMOUNT = getattr(settings, 'SEARCH_PAGESIZE', 10)


def paginator(query, page_num=1, display_amount=DISPLAY_AMOUNT):
    """ author: feng
    分页器
    :param query: django orm 查询对象
    :param page_num: 第几页
    :param display_amount: 每页多少条数据
    :return: 一个PageSeoSet对象
    """
    # assert isinstance(page_num, int), 'page_num must be int'
    try:
        page_num = int(page_num)
    except ValueError:
        page_num = 1
    page_num = page_num if page_num > 0 else 1
    p = Paginator(query, display_amount)    # 每页display_amount条数据的分页器
    try:
        page = p.page(page_num)
    except (InvalidPage, EmptyPage):   # 如果当前页不存在，获取最后一页
        page = p.page(p.num_pages)
    page_data = {'page_data': page.object_list,
                 'page_count': p.count,     # 数据总条数
                 'has_next': page.has_next(),
                 'has_perv': page.has_previous(),
                 'page': page_num}          # 当前页数
    return page_data


def json_paginator(query, page_num=1, display_amount=DISPLAY_AMOUNT, param=None):
    assert isinstance(param, (list, set, tuple)), 'param must be tuple, list, set'
    if isinstance(param, list):
        param = tuple(set(param))   # 去重
    data = paginator(query, page_num, display_amount)
    data['page_data'] = list(data['page_data'].values(*param))
    return data


# CALLBACK_URL_TEMPLATE = "/wap/course/{career}/{course_id}-{lesson_id}"
def reverse_lesson_url(course_id, lesson_id):
    """ author: feng
    设置课程前端访问url
    :param career: 课程方向(short name)
    :param course_id: 课程id
    :param lesson_id: 章节id
    :return: 构造好的lesson_detail url
    """
    return reverse_lazy(
        'lesson_detail',
        args=[course_id, lesson_id])


def set_callback_url(courses):
    """ author: feng
    设置课程前端访问url
    :param courses: 课程方向
    :return:
    """
    for item in courses:
        try:
            career = item.stages_m.all()[0].career_course.short_name.lower()
        except:
            career = 'others'
        lessons = item.lesson_set.all().order_by('id')
        item.callback_url = reverse_lesson_url(item.id, lessons[0].id) if lessons else ""


def set_callback_url_by_course_id(course_id):
    """ author: feng
    通过课程id生成课程前端访问url
    :param course_id: 课程id
    :return: callback_url
    """
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return ''
    try:
        career = course.stages_m.all()[0].career_course.short_name.lower()
    except:
        career = 'others'
    lessons = course.lesson_set.all().order_by('index')
    callback_url = reverse_lesson_url(
        career, course.id, lessons[0].id) if lessons else ""
    return callback_url


def set_callback_url_by_dic(data):
    """ author: feng
    通过课程id生成课程前端访问url
    :param data: 课程信息字典list
    :return:
    """
    for d in data:
        d['callback_url'] = set_callback_url_by_course_id(d['id'])


def set_lesson_list_callback_url(lessons, career, course_id):
    """ author: feng
    设置每个章节前端访问url
    需要支付的课程只给看前两章
    :param lessons: 章节列表
    :param career: 课程方向
    :param course_id: 课程id
    :return:
    """
    need_pay = None
    for index, item in enumerate(lessons):
        if need_pay is None:
            need_pay = item.course.need_pay
        if need_pay or index >= 2:
            item.callback_url = '#'
        else:
            item.callback_url = reverse_lesson_url(
                career, course_id, item.id) if lessons else ""


def record_lesson_click_count(lesson):
    """ author: feng
    记录章节及章节的课程的播放次数和点击次数
    :param lesson: 章节
    :return:
    """
    lesson.play_count += 1
    lesson.course.click_count += 1
    lesson.course.save()
    lesson.save()


# 判断空
def judge_none(**kwargs):
    for v in kwargs.values():
        if not v:
            return False
    return True


def list_judge_none(list, *args):
    for item in args:
        if judge_none(**item):
            list.append(item)

def calc_course_video_length(lessons):
    """
    @brief 基于新架构的计算章节学习时长函数
    :param lessons:
    :return:
    """
    if lessons:
        vl = reduce(lambda x, y: x + y, [l.get('video_length', 0) for l in lessons])
    else:
        return 0
    h = vl / 3600
    if vl % 3600 != 0:
        return h+1
    return h

def safe_api_result(api_result, log_object, warn_log, if_raise=True, exc_class=Http404):
    """
    @brief api_result的结果检查
    :param api_result:　数据库API返回的函数, 如db.api.course.course.xx_function
    :param log_object: 日志的instance, 用以记录日志
    :param warn_log: 错误发生时的日志
    :param if_raise: 是否抛出错误，如果该参数被设置为真，则抛出Http404异常, 否则默认被设置
    :param exc_class: 抛出异常的类型，默认为Http404
    :return:　返回取值之后的APIResult. 若出错且未抛异常，则返回None

    ＠note: 最好的实现方式为APIResult增加一个方法来处理，该函数为临时的处理方案
    """
    if api_result.is_error():
        log_object.warn(warn_log)
        if if_raise:
            raise exc_class
        else:
            return None
    return api_result.result()


def get_current_url(url, regex_url):
    # 获取当前url的前缀用于分页，页数链接url地址拼接
    try:
        url_prefix = re.match(regex_url, url.rstrip("/")).groups()[0]
    except Exception as e:
        log.info('invalid url: %s, details: %s' % (url, e))
        url_prefix = ''

    return url_prefix
