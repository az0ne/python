#!/usr/bin/env python
# -*- coding: utf8 -*-
from django.http import Http404

import db.api.micro.wechat_course.wechat_course
import db.api.course.careerCourse
from utils.logger import logger as log
from django.shortcuts import render


def insert_wechat_career_course(name, index):
    APIResult = db.api.micro.wechat_course.wechat_course.insert_wechat_career_course(name=name, index=index)
    if APIResult.is_error():
        message = u"insert_wechat_career_course failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def insert_wechat_course(dict_course):
    APIResult = db.api.micro.wechat_course.wechat_course.insert_wechat_course(dict_info=dict_course)
    if APIResult.is_error():
        message = u"insert_wechat_course failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def insert_wechat_lesson(dict_lesson):
    APIResult = db.api.micro.wechat_course.wechat_course.insert_wechat_lesson(dict_info=dict_lesson)
    if APIResult.is_error():
        message = u"insert_wechat_lesson failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def get_wechat_career_by_id(career_id):
    APIResult = db.api.micro.wechat_course.wechat_course.get_wechat_career_by_id(career_id=career_id)
    if APIResult.is_error():
        message = u"get wechat career course by id failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def get_wechat_course_by_id(course_id):
    APIResult = db.api.micro.wechat_course.wechat_course.get_wechat_course_by_id(course_id=course_id)
    if APIResult.is_error():
        message = u"get wechat course by id failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def get_wechat_lesson_by_id(lesson_id):
    APIResult = db.api.micro.wechat_course.wechat_course.get_wechat_lesson_by_id(lesson_id=lesson_id)
    if APIResult.is_error():
        message = u"get_wechat_lesson_by_id failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def list_all_wechat_career_course():
    APIResult = db.api.micro.wechat_course.wechat_course.list_all_wechat_career_coures()
    if APIResult.is_error():
        message = u"list_all_wechat_career_course failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def list_all_wechat_course(page_index, page_size):
    APIResult = db.api.micro.wechat_course.wechat_course.list_wechat_all_course(page_index=page_index,
                                                                                page_size=page_size)
    if APIResult.is_error():
        message = u"list_wechat_all_course failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def list_all_wechat_course_by_search(page_index, page_size, career_course_id):
    APIResult = db.api.micro.wechat_course.wechat_course.list_wechat_all_course_by_search(page_index=page_index,
                                                                                          page_size=page_size,
                                                                                          career_course_id=career_course_id)
    if APIResult.is_error():
        message = u"list_wechat_all_course by search failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def list_all_wechat_lesson(page_index, page_size, course_id):
    APIResult = db.api.micro.wechat_course.wechat_course.list_wechat_all_lesson(page_index=page_index,
                                                                                page_size=page_size,
                                                                                course_id=course_id)
    if APIResult.is_error():
        message = u"list_all_wechat_lesson failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def list_all_career_course():
    APIResult = db.api.course.careerCourse.list_career_course_name()
    if APIResult.is_error():
        message = u"list_all_career_courselist_all_career_course failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def update_wechat_career_course(name, index, _id):
    APIResult = db.api.micro.wechat_course.wechat_course.update_wechat_career_course(name=name, index=index, _id=_id)
    if APIResult.is_error():
        message = u"update_wechat_career_course failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def update_wechat_course(dict_info):
    APIResult = db.api.micro.wechat_course.wechat_course.update_wechat_course(dict_info=dict_info)
    if APIResult.is_error():
        message = u"update_wechat_course failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def update_wechat_lesson(dict_info):
    APIResult = db.api.micro.wechat_course.wechat_course.update_wechat_lesson(dict_info=dict_info)
    if APIResult.is_error():
        message = u"update_wechat_lesson failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def delete_wechat_lesson(lesson_id):
    APIResult = db.api.micro.wechat_course.wechat_course.del_wechat_lesson_by_id(lesson_id)
    if APIResult.is_error():
        message = u"del_wechat_lesson_by_id failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def delete_wechat_course(course_id):
    APIResult = db.api.micro.wechat_course.wechat_course.del_wechat_course_by_id(course_id)
    if APIResult.is_error():
        message = u"del_wechat_course_by_id failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def check_is_active(is_active):
    if is_active is None:
        is_active = 1
    else:
        is_active = 0
    return is_active
