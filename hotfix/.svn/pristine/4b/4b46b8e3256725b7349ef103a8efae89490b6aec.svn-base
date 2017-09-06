# -*- coding: utf-8 -*-
from mz_course.models import CareerCourse
from mz_lps.models import Class
from mz_user.models import UserProfile
from utils.decorators_cache import cache_data

__author__ = 'Jackie'


@cache_data(60 * 1)
def get_classes_by_eduadmin(eduadmin_id, cache_pk=None):
    """获取教务老师的班级"""
    objs = Class.objects.xall().filter(
        edu_admin_id=eduadmin_id, lps_version='3.0',
        class_type=Class.CLASS_TYPE_NORMAL).order_by('-id')
    objs = list((obj.id, obj.coding) for obj in objs)
    return objs


@cache_data(60 * 1)
def get_edu_admins():
    """获取教务人员
    :return
    """
    objs = UserProfile.objects.filter(groups__name='教务').values('id', 'nick_name', 'real_name')
    objs = list((obj['id'], obj['real_name'] or obj['nick_name']) for obj in objs)
    return objs


@cache_data(60 * 1)
def get_teachers():
    """
    获取所有老师
    :return:
    """
    objs = UserProfile.objects.filter(groups__name='老师').values('id', 'nick_name', 'real_name')
    objs = list((obj['id'], obj['real_name'] or obj['nick_name']) for obj in objs)
    return objs


@cache_data(60 * 1)
def get_career_courses():
    """
    获取所有课程
    :return:
    """
    objs = CareerCourse.objects.all().values('id', 'name', 'short_name').order_by('name')
    objs = list((obj['id'], obj['name'], obj['short_name']) for obj in objs)
    return objs
