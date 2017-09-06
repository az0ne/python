#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.http import JsonResponse

from utils.logger import logger as log
from utils import tool
from utils.decorators import dec_login_validate
from utils.handle_exception import handle_http_response_exception
import db.api.course.careerCatagory
import db.api.course.tag
import db.api.course.careerCourse
import db.api.course.careerIntroduce
import db.api.course.taskDesc
import db.api.course.course_ajax
import db.api.article.article_type
import db.api.course.questionnaire



@handle_http_response_exception(501)
def get_career_course_name(request):
    """
    获取职业课程表(mz_career_course)中的name、id字段用于填充下拉列表框
    :param request:
    :return:JSON数据:{result:{'id':xx,'name':'xxxx'}}
    """
    career_course_name = db.api.course.careerCourse.list_career_course_name()

    if career_course_name.is_error():
        log.warn('get career course name failed!')
        result = {}
    else:
        result = career_course_name.result()

    c = {"result": result}

    return JsonResponse(c)


@dec_login_validate
@handle_http_response_exception(501)
def list_career_catagory_name(request):
    """
    获取专业方向(mz_course_careercatagory)的id和name，用于填充下拉列表框
    :param request:
    :return: JSON数据类型为：{result:[{'id':xx,'name':'xxx'}]}
    """
    career_catagory_name = db.api.course.careerCatagory.list_career_catagory()
    if career_catagory_name.is_error():
        log.warn('get career catagory name failed!')
        result = {}
    else:
        result = career_catagory_name.result()
    result = {"result": result}

    return JsonResponse(result)


@dec_login_validate
@handle_http_response_exception(501)
def courseTag_list_all(request):
    """
    获取课程标签（mz_course_tag）的id,name, 用于填充下拉列表框
    :param request:
    :return: JSON数据类型为：{result:[{'id':xx,'name':'xxx'}]}
    """
    course_tag = db.api.course.tag.list_courseTag()
    if course_tag.is_error():
        log.warn('get career tag name failed!')
        result = {}
    else:
        result = course_tag.result()

    c = {"result": result}

    return JsonResponse(c)


@dec_login_validate
@handle_http_response_exception(501)
def get_is_homepage_course_name(request):
    """
    获取小课程（mz_course_course），并is_acitive=1的id，name字段
    :param request:
    :return: JSON数据类型为:{result:[{'id':xx,'name':'xxxx'}]}
    """
    course_ajax = db.api.course.course_ajax.course_ajax()
    if course_ajax.is_error():
        log.warn('get course course name and where is_acitive=1 failed!')
        result = {}
    else:
        result = course_ajax.result()

    c = {"result": result}

    return JsonResponse(c)


@dec_login_validate
@handle_http_response_exception(501)
def get_career_introduce_name(request):
    """
    获取职业课程表(mz_career_page)中的name、id字段用于填充下拉列表框
    :param request:
    :return:JSON数据类型为:{result:[{'id':xx,'name':'xxxx'}]}
    """
    career_name = db.api.course.careerIntroduce.list_career_introduce_name()
    if career_name.is_error():
        log.warn('get career tag name failed!')
        result = {}
    else:
        result = career_name.result()

    c = {"result": result}

    return JsonResponse(c)


@dec_login_validate
@handle_http_response_exception(501)
def get_all_article_type_name(request):
    """
    使用ajax异步请求方式，获取文章类型的名称和id值，填充到下拉列表框中
    :param request:
    :return: JSON数据类型为:{result:[{'id':xx,'name':'xxxx'}]}
    """
    article_type = db.api.article.article_type.get_all_article_type_name()
    if article_type.is_error():
        log.warn('get all article type name for combobox fill data failed!')
        c = {'result': {}}
    else:
        c = {'result': article_type.result()}

        return JsonResponse(c)


@dec_login_validate
@handle_http_response_exception(501)
def get_is_homepage_article_type_name(request):
    """
    使用ajax异步请求方式，获取文章类型的名称和id值，填充到下拉列表框中
    :param request:
    :return: JSON数据类型为:{result:[{'id':xx,'name':'xxxx'}]}
    """
    article_type = db.api.article.article_type.get_is_homepage_article_type_name()
    if article_type.is_error():
        log.warn('get all article type name for combobox fill data failed!')
        c = {'result': {}}
    else:
        c = {'result': article_type.result()}

        return JsonResponse(c)


@dec_login_validate
@handle_http_response_exception(501)
def questionnaire_get(request):
    """
    获取问卷（mz_free_questionnaire）名称
    :param request:
    :return:JSON数据类型为:{result:[{'id':xx,'name':'xxxx'}]}
    """
    questionnaire = db.api.course.questionnaire.ajax_questionnaire()
    if questionnaire.is_error():
        log.warn('get free questionnaire name failed!')
        result = {}
    else:
        result = questionnaire.result()

    c = {'result':result}

    return JsonResponse(c)


# ——————————————————————————————————————————————————————验证唯一性———————————————————————————————————————————————————— #
@dec_login_validate
@handle_http_response_exception(501)
def validate_unique_career_page_id(request):
    """
    验证职业课程介绍的(mz_career_page)id值是否已存在
    :param request:
    :return:JSON数据:{result:{'id':xx,'name':xx}}
    """
    # id中封装到有该课程的id_名字,如:1_嵌入式驱动开发
    career_id_and_name = tool.get_param_by_request(request.GET, 'id', "", str)
    career_id = career_id_and_name.split('_')[0]
    career_introduce = db.api.course.careerIntroduce.select_career_introduce_by_career_id(career_id)
    if career_introduce.is_error():
        log.warn('validate career introduce of id if is unique failed!')
        result = {}
    else:
        result = career_introduce.result()

    c = {"result": result}

    return JsonResponse(c)


@dec_login_validate
@handle_http_response_exception(501)
def validate_unique_free_task_desc_id(request):
    """
       验证任务描述（mz_free_task_desc）的id值是否已存在
       :param request:
       :return:JSON数据:{result:{'count':xx}}
       """
    task_id = tool.get_param_by_request(request.GET, 'id', 1, int)
    task_desc = db.api.course.taskDesc.select_task_desc_by_task_id(task_id)
    if task_desc.is_error():
        log.warn('validate task desc of id if is unique failed!')
        result = {}
    else:
        result = task_desc.result()

    c = {"result": result}

    return JsonResponse(c)


@dec_login_validate
@handle_http_response_exception(501)
def validate_unique_article_type_id(request):
    """
        验证文章类型的（mz_common_articletype）id值是否已存在
        :param request:
        :return:JSON数据:{result:{'id':xx,'name':xx}}
        """

    _id = tool.get_param_by_request(request.GET, 'id', 1, int)
    article_type = db.api.article.article_type.validate_unique_id(_id)

    if article_type.is_error():
        log.warn('validate unique id failed!')
        c = {'result': {}}
    else:
        c = {"result": article_type.result()}

    return JsonResponse(c)
