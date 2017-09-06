#!/usr/bin/env python
# -*- coding: utf8 -*-
from django.http import Http404

import db.api.micro.wechat_course.wechat_course_discuss
import db.api.course.careerCourse
from utils.logger import logger as log


def insert_wechat_discuss(discuss_dict):
    APIResult = db.api.micro.wechat_course.wechat_course_discuss.insert_discuss_by_id(discuss_dict=discuss_dict)
    if APIResult.is_error():
        message = u"insert_wechat_career_course failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def del_wechat_parent_discuss(_id):
    APIResult = db.api.micro.wechat_course.wechat_course_discuss.del_parent_discuss_by_id(_id=_id)
    if APIResult.is_error():
        message = u"del_parent_discuss_by_id failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def del_wechat_child_discuss(_id):
    APIResult = db.api.micro.wechat_course.wechat_course_discuss.del_child_discuss_by_id(_id=_id)
    if APIResult.is_error():
        message = u"del_child_discuss_by_id failed."
        log.warn(message)
        raise Http404
    result = APIResult.result()
    return result


def list_wechat_parent_dicuss(page_index, page_size):
    APIResult = db.api.micro.wechat_course.wechat_course_discuss.list_wechat_parent_discuss(page_index=page_index,
                                                                                            page_size=page_size)
    if APIResult.is_error():
        log.warn(u"list wechat parent discuss failed.")
        raise Http404
    result = APIResult.result()
    return result


def list_wechat_parent_dicuss_by_search(page_index, page_size, keyword):
    APIResult = db.api.micro.wechat_course.wechat_course_discuss.list_wechat_parent_discuss_by_search(
        page_index=page_index,
        page_size=page_size,
        keyword=keyword)
    if APIResult.is_error():
        log.warn(u"list wechat parent discuss by search failed.")
        raise Http404
    result = APIResult.result()
    return result


def list_wechat_child_discuss(parent_id):
    APIResult = db.api.micro.wechat_course.wechat_course_discuss.list_all_child_discuss(parent_id)
    if APIResult.is_error():
        log.warn(u"list wechat child discuss failed.")
        raise Http404
    result = APIResult.result()
    return result


def get_parent_discuss_by_id(parent_id):
    APIResult = db.api.micro.wechat_course.wechat_course_discuss.get_discuss_by_id(parent_id)
    if APIResult.is_error():
        log.warn("get wechat discuss by id failed.")
        raise Http404
    result = APIResult.result()
    return result
