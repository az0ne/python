# -*- coding: utf8 -*-

import db.api
from django.conf import settings
from utils.logger import logger as log


def wiki_public_data():
    """
    wiki页面公用数据
    :return: dict: type_list: wiki课程分类;
                   links: wiki页面友情链接
    """

    course_types = db.api.get_wiki_course_types()
    if course_types.is_error():
        course_types = []
        log.error('wiki_public_data error: get course_types failed')
    else:
        course_types = course_types.result()

    links = db.api.get_wiki_links()
    if links.is_error():
        links = []
        log.error('wiki_public_data error: get links failed')
    else:
        links = links.result()

    return dict(
        type_list=course_types,
        links=links
    )


def merge_data_list(first, second, first_attr,
                    second_attr, key_attr, is_clean=True):
    """
    合并两个有重合的数据列表(字典列表)，用来对应表跟它的外键表
    :param first: 一级字典列表
    :param second: 二级字典列表
    :param first_attr: 一级字典用来跟二级字典对比的key
    :param second_attr: 二级字典用来跟一级字典对比的key
    :param key_attr: 用来在一级字典取值的key，用来生成最终数据列表
    :param is_clean: 是否干净的数据列表，抛弃空的数据列表
    :return: 生成的数据字典
    """

    data_list = []

    try:
        for _fst in first:
            l = [c for c in second if c[second_attr] == _fst[first_attr]]

            if not is_clean or l:
                if isinstance(key_attr, (tuple, list)):
                    data_list.append({tuple([_fst[key] for key in key_attr]): l})
                else:
                    data_list.append({_fst[key_attr]: l})
    except KeyError as e:
        log.warn('key error: key "{}" not found'.format(e))

    return data_list


def get_all_first_item_short_name_dict():
    """
    将get_all_course_first_item_short_name获取到的数据，
    按{course_id: first_item_short_name}的格式合并成字典
    :return:
    """

    res = db.api.get_all_course_first_item_short_name()

    if res.is_error():
        log.warn('get_all_course_first_item_short_name failed')
        res = {}
    else:
        res = {r['course_id']: r['first_item_short_name'] for r in res.result()}

    return res


def mark_course_list_first_item_short_name(courses):
    """
    给一个课程列表中的每个课程设它的第一个知识点的short_name,
    未找到知识点的课程将被丢弃
    :param courses: 一个包装课程的可迭代对象(list or tuple or...)
    :return:
    """

    course_item_dic = get_all_first_item_short_name_dict()

    course_list = []
    for course in courses:
        if course['id'] in course_item_dic:
            course['first_item_short_name'] = course_item_dic[course['id']]
            course_list.append(course)

    return course_list


def get_article_by_wiki_course_short_name(short_name):
    """
    根据wiki课程查询相关文章(最多4条)
    :param short_name: course short_name
    :return: article list
    """

    wiki_course = db.api.get_wiki_course_by_short_name(short_name)
    if wiki_course.is_error():
        log.warn('get wiki course by short name failed.'
                 'course short_name: {0}'.format(short_name))
        return []

    articles = db.api.get_article_with_course(wiki_course.result()['course_id'])
    if articles.is_error():
        log.warn('get article with course failed.'
                 'course_id: {0}'.format(wiki_course.result()['course_id']))
        return []

    return articles.result()[:4]
