# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http.response import JsonResponse
from django.shortcuts import render
from django.conf import settings
from mz_user.models import UserProfile
from mz_lps.models import ClassStudents
from mz_lps.models import ClassTeachers
# 定义只能学生分组才能访问的修饰符
def student_required(func):
    def is_student(request, **kwargs):
        if not request.user.is_authenticated() or not request.user.is_student():
            return HttpResponseRedirect(reverse('index_front'))
        return func(request, **kwargs)
    return is_student

# 定义只能老师分组才能访问的修饰符
def teacher_required(func):
    def is_teacher(request, **kwargs):
        if not request.user.is_authenticated() or not request.user.is_teacher():
            return HttpResponseRedirect(reverse('index_front'))
        return func(request, **kwargs)
    return is_teacher

# 定义只能老师或教务才能访问的修饰符
def teacher_or_eduadmin_required(func):
    def is_teacher(request, **kwargs):
        if not request.user.is_authenticated() or not (request.user.is_teacher() or request.user.is_edu_admin()):
            return HttpResponseRedirect(reverse('index_front'))
        return func(request, **kwargs)
    return is_teacher


# 定义只能教务老师分组才能访问的修饰符
def eduadmin_required(func):
    def wrapper(request, **kwargs):
        if not request.user.is_authenticated() or not request.user.is_edu_admin():
            return HttpResponseRedirect(reverse('index_front'))
        return func(request, **kwargs)
    return wrapper


# 定义只能超级管理员才能访问的修饰符
def superuser_required(func):
    def is_superuser(request, **kwargs):
        if not request.user.is_authenticated() or (not request.user.is_superuser and not request.user.is_staff):
            return HttpResponseRedirect(reverse('backend:admin_login'))
        return func(request, **kwargs)
    return is_superuser

# 定义只有所属班级的老师才可以访问的修饰符
def lps_student_teacher_required(func):
    def is_valid(request, **kwargs):

        # 未登录情况下不能访问
        if not request.user.is_authenticated() or not request.user.is_teacher():
            return HttpResponseRedirect(reverse('index_front'))

        # 检查当前登录用户是否是该这个学员所在班级的带班老师
        class_student = ClassStudents.objects.filter(user_id=kwargs['user_id'], student_class_id=kwargs['class_id'])
        if len(class_student) > 0:
            if not ClassTeachers.objects.filter(teacher_class_id=kwargs['class_id'], teacher=request.user.id).exists():
                return HttpResponseRedirect(reverse('index_front'))
        else:
            return HttpResponseRedirect(reverse('index_front'))

        return func(request, **kwargs)
    return is_valid


def ajax_login_required(func):
    def wrapper(request, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse(dict(success=False, code=401,
                                     errors={'login_required': ['请先登录']}))
        return func(request, **kwargs)
    return wrapper
