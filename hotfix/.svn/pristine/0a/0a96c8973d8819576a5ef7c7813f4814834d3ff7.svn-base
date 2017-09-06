# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
import interface
from mz_common.decorators import eduadmin_required
from mz_eduadmin.common import interface as ci
from mz_lps.models import Class, ClassStudents
from mz_user.models import UserProfile

__author__ = 'Jackie'


@eduadmin_required
def index(request):
    user = request.user
    input_class = request.GET.get('c')  # 选择班级
    input_query = request.GET.get('q', '').strip()  # 按名字查询
    input_eduadmin = request.GET.get('e')  # 输入教务人员

    current_class = ''

    if input_query and input_eduadmin:  # 根据学生姓名查询
        current_eduadmin = get_object_or_404(UserProfile, id=input_eduadmin).id
        csi = interface.QueryStudentsInterface(input_eduadmin, input_query)
        dashboard = csi.dashboard
        data = csi.data
        query_string = input_query
    else:
        if input_class:
            current_class = Class.objects.xall().get(id=input_class)
            current_eduadmin = current_class.edu_admin_id
        else:
            current_eduadmin = user.id  # user.id
            classes = ci.get_classes_by_eduadmin(current_eduadmin)
            if classes:
                current_class = Class.objects.xall().get(id=classes[0][0])
        if current_class:
            csi = interface.ClassStudentsInterface(current_class.id)
            dashboard = csi.dashboard
            data = csi.data

    edu_admins = ci.get_edu_admins()
    nav = 'students'
    return render(request, 'mz_eduadmin/students/index.html', locals())


@eduadmin_required
def student_change_class(request, class_id, student_id):
    cstudent = get_object_or_404(ClassStudents, user_id=student_id, student_class_id=class_id)
    if cstudent.student_class.edu_admin_id != request.user.id or cstudent.status == ClassStudents.STATUS_QUIT:
        raise PermissionDenied

    if request.method == 'GET':
        student_name = cstudent.user.real_name or cstudent.user.nick_name
        return render(request, 'mz_eduadmin/students/div_zhuanban.html', locals())
    else:
        to_class = request.POST.get('to_class', '').strip().upper()
        remark = request.POST.get('remark', '').strip()
        if remark:
            flag, message = interface.change_student_class(class_id, student_id, request.user.id, to_class, remark)
        else:
            flag, message = False, u'请填写备注'
        return JsonResponse(data=dict(status=bool(flag), message=message))


@eduadmin_required
def student_quit_class(request, class_id, student_id):
    cstudent = get_object_or_404(ClassStudents, user_id=student_id, student_class_id=class_id)
    if cstudent.student_class.edu_admin_id != request.user.id or cstudent.status == ClassStudents.STATUS_QUIT:
        raise PermissionDenied
    if request.method == 'GET':
        student_name = cstudent.user.real_name or cstudent.user.nick_name
        return render(request, 'mz_eduadmin/students/div_tuixue.html', locals())
    else:
        remark = request.POST.get('remark', '').strip()

        if remark:
            flag, message = interface.student_quit_class(class_id, student_id, request.user.id, remark)
        else:
            flag, message = False, u'请填写备注'
        return JsonResponse(data=dict(status=bool(flag), message=message))


@eduadmin_required
def student_pause(request, class_id, student_id):
    cstudent = get_object_or_404(ClassStudents, user_id=student_id, student_class_id=class_id)
    if cstudent.student_class.edu_admin_id != request.user.id or cstudent.status == ClassStudents.STATUS_QUIT:
        raise PermissionDenied
    if request.method == 'GET':
        student_name = cstudent.user.real_name or cstudent.user.nick_name
        pause_type = 'resume' if cstudent.is_pause else 'pause'
        return render(request, 'mz_eduadmin/students/div_xiuxue.html', locals())
    else:
        remark = request.POST.get('remark', '').strip()
        tp = request.POST.get('pause_type', 'pause')
        if remark:
            flag, message = interface.student_pause_studying(class_id, student_id, request.user.id, remark, type=tp)
        else:
            flag, message = False, u'请填写备注'
        return JsonResponse(data=dict(status=bool(flag), message=message))


@eduadmin_required
def export_class_students(request, class_id):
    iface = interface.ClassStudentsExportInterface(class_id)
    excel = iface.export()
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = (
    u'attachment; filename=%s-%s.xls' % (iface.course_name, iface.class_name)).encode('utf-8')

    excel.save(response)
    return response
