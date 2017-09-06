# -*- coding: utf8 -*-

import db.api
from django.http.response import Http404
from django.shortcuts import render
from utils.logger import logger as log
from mz_wiki.functions import wiki_public_data, merge_data_list, \
    mark_course_list_first_item_short_name, \
    get_article_by_wiki_course_short_name


# wiki首页
def wiki_index(request):

    data = wiki_public_data()

    courses = db.api.get_all_wiki_course(is_homepage=True)
    if courses.is_error():
        course_list = []
        log.warn('wiki_index error: get courses failed')
    else:
        course_list = mark_course_list_first_item_short_name(courses.result())

    course_data_list = merge_data_list(
        data['type_list'], course_list, 'id', 'type_id', 'name')

    data.update(course_data_list=course_data_list)

    return render(request, 'mz_wap/wiki.html', data)


# wiki课程详情页
def wiki_course_detail(request, short_name):
    """
    wiki课程详情页
    :param request:
    :param short_name: wiki_course的short_name
    :return:
    """

    # data = wiki_public_data()
    data = dict()

    course = db.api.get_wiki_course_by_short_name(short_name)
    if course.is_error():
        log.warn('get_wiki_course_by_short_name is failed. '
                 'course_short_name: {0}'.format(short_name))
        raise Http404
    else:
        course = course.result()
    course['seo_name'] = course['name'].replace(u'学习', '')

    chapter_list = db.api.get_wiki_chapters_by_course_short_name(
        short_name)
    if chapter_list.is_error():
        chapter_list = []
        log.warn('wiki_item_detail error: get chapter list failed. '
                 'course_short_name: {0}'.format(short_name))
    else:
        chapter_list = chapter_list.result()

    item_list = db.api.get_wiki_items_by_course_short_name(short_name)
    if item_list.is_error():
        item_list = []
        log.warn('get wiki items by course short name failed.'
                 'course_short_name: {0}'.format(short_name))
    else:
        item_list = item_list.result()

    item_data_list = merge_data_list(
        chapter_list, item_list, 'id', 'chapter_id', 'name', is_clean=False)

    data.update(course=course, course_short_name=short_name,
                item_data_list=item_data_list)

    return render(request, 'mz_wap/wiki_list.html', data)


# wiki知识点 详情页
def wiki_item_detail(request, course_short_name, item_short_name):
    data = wiki_public_data()

    course = db.api.get_wiki_course_by_short_name(course_short_name)
    if course.is_error():
        log.warn('get_wiki_course_by_short_name is failed. '
                 'course_short_name: {0}'.format(course_short_name))
        raise Http404
    else:
        course = course.result()

    course_list = db.api.get_all_wiki_course()
    if course_list.is_error():
        log.warn('get all wiki course failed. ')
        course_list = []
    else:
        course_list = mark_course_list_first_item_short_name(
            course_list.result())

    type_course_data_list = merge_data_list(
        data['type_list'], course_list, 'id', 'type_id',
        ['name', 'short_name', 'img_url', 'img_title'], is_clean=False)

    chapter_list = db.api.get_wiki_chapters_by_course_short_name(
        course_short_name)
    if chapter_list.is_error():
        chapter_list = []
        log.warn('wiki_item_detail error: get chapter list failed. '
                 'course_short_name: {0}'.format(course_short_name))
    else:
        chapter_list = chapter_list.result()

    item_list = db.api.get_wiki_items_by_course_short_name(course_short_name)
    if item_list.is_error():
        item_list = []
        log.warn('get wiki items by course short name failed.'
                 'course_short_name: {0}'.format(course_short_name))
    else:
        item_list = item_list.result()

    item_data_list = merge_data_list(
        chapter_list, item_list, 'id', 'chapter_id', 'name', is_clean=False)

    item = db.api.get_wiki_item_by_short_name(
        course_short_name, item_short_name)
    if item.is_error():
        log.info('get wiki item by short name failed.'
                 'course_short_name: {0}. item_short_name: {1}.'
                 .format(course_short_name, item_short_name))
        raise Http404()
    else:
        item = item.result()

    try:
        item_i = [_item['id'] for _item in item_list].index(item['id'])
        prev_item = item_list[item_i-1] if item_i > 0 else None
        next_item = item_list[item_i+1] if item_i < len(item_list)-1 else None
    except ValueError as e:
        log.warn('wiki_item_detail exception: item not in item_list, check it.'
                 'details: {0}. course_short_name: {1}. item_short_name: {2}'
                 .format(e, course_short_name, item_short_name))
        raise Http404()

    wiki_chapter = db.api.get_wiki_chapter_by_item_id(item['id'])
    if wiki_chapter.is_error():
        log.warn('get wiki chapter by item_id failed.'
                 'item_id: {0}.'.format(item['id']))
        wiki_chapter = {}
    else:
        wiki_chapter = wiki_chapter.result()

    wiki_ad = {}
    # wiki_ad = db.api.get_wiki_ad_by_course_short_name(course_short_name)
    # if wiki_ad.is_error():
    #     log.warn('get wiki ad by course_short_name failed.'
    #              'course_short_name: {0}'.format(course_short_name))
    #     wiki_ad = {}
    # else:
    #     wiki_ad = wiki_ad.result()

    relation_course = db.api.get_lps_course_by_wiki_course_short_name(
        course_short_name)
    if relation_course.is_error():
        log.info('get lps course by wiki course short name failed.'
                 'course_short_name: {0}'.format(course_short_name))
    relation_course = relation_course.result()

    recommend_courses = db.api.get_recommend_course_by_wiki_course_short_name(
        course_short_name)
    if recommend_courses.is_error():
        log.info('get recommend course by wiki course short name failed.'
                 'course_short_name: {0}'.format(course_short_name))
        recommend_courses = []
    else:
        recommend_courses = recommend_courses.result()

    relation_articles = get_article_by_wiki_course_short_name(course_short_name)
    relation_articles = relation_articles[:4-len(recommend_courses)]

    data.update(item_data_list=item_data_list, item=item,
                prev_item=prev_item, next_item=next_item,
                course_short_name=course_short_name,
                wiki_chapter=wiki_chapter, wiki_ad=wiki_ad,
                relation_course=relation_course, course=course,
                relation_articles=relation_articles,
                recommend_courses=recommend_courses,
                type_course_data_list=type_course_data_list)

    return render(request, 'mz_wap/wiki_article.html', data)
