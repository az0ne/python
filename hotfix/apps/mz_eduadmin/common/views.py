# -*- coding: utf-8 -*-
from django.http.response import JsonResponse
import interface

__author__ = 'Jackie'


def get_classes(request):
    """获取班级列表"""
    eduadmin_id = int(request.GET.get('e'))
    keyword = request.GET.get('s', '').upper()
    classes = interface.get_classes_by_eduadmin(eduadmin_id, cache_pk=eduadmin_id)
    ret = list()
    for cls in classes:
        if keyword in cls[1].upper():
            ret.append(cls)
    if not ret:
        ret = [(-1, u'暂无数据')]
    return JsonResponse(data=ret, safe=False)


def get_eduadmins(request):
    """获取班级列表"""
    keyword = request.GET.get('s', '').upper()
    eduadmins = interface.get_edu_admins()
    ret = list()
    for ea in eduadmins:
        if keyword in ea[1].upper():
            ret.append(ea)
    if not ret:
        ret = [(-1, u'暂无数据')]
    return JsonResponse(data=ret, safe=False)


def get_teachers(request):
    """ 获取教师列表"""
    keyword = request.GET.get('s', '').upper()
    teachers = interface.get_teachers()
    ret = list()
    for t in teachers:
        if keyword in t[1].upper():
            ret.append(t)
    if not ret:
        ret = [(-1, u'暂无数据')]
    return JsonResponse(data=ret, safe=False)


def get_career_courses(request):
    """获取专业列表"""
    keyword = request.GET.get('s', '').upper()
    career_courses = interface.get_career_courses()
    ret = list()
    for c in career_courses:
        if keyword in c[1].upper():
            ret.append(c)
    if not ret:
        ret = [(-1, u'暂无数据')]
    return JsonResponse(data=ret, safe=False)
