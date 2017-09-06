# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from mz_lps.models import ClassStudents, Class

__author__ = 'Jackie'


def check_student_status(func):
    def _wrapper(request, **kwargs):
        user = request.user
        class_id = None
        if kwargs:
            class_id = kwargs.get('class_id')
        if class_id is None:
            class_id = request.GET.get('class_id') or request.POST.get('class_id')

        cstudent = get_object_or_404(ClassStudents, student_class_id=class_id, user_id=user.id)
        request.cstudent = cstudent
        try:
            request.cclass = Class.objects.xall().get(id=class_id)
        except Class.DoesNotExist:
            raise Http404
        if cstudent.status == cstudent.STATUS_QUIT:  # 已退班
            raise PermissionDenied(u'已退班,无学习权限')
        if cstudent.is_trial_user:
            if cstudent.is_overdue:
                raise PermissionDenied(u'试学缴费期已过,资源已释放!')
        return func(request, **kwargs)

    return _wrapper
