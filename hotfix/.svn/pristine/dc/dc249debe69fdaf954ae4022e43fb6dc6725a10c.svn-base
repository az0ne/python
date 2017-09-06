# -*- coding: utf-8 -*-
import json
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from mz_common.decorators import eduadmin_required
from mz_eduadmin.classes.interface import get_class_info, get_edu_admin_class_info, update_class_state, \
    get_edu_admin_name_by_id, check_class_create_parameters
from mz_eduadmin.classes import interface

@eduadmin_required
def index(request):
    if ('GET' == request.method):
        edu_admin_id = request.GET.get('b')
        is_self = True

        if edu_admin_id and long(edu_admin_id) != request.user.id:
            is_self = False
        else:
            edu_admin_id = request.user.id #20276

        class_info_list, career_course_list, teacher_list = get_class_info(edu_admin_id, is_self)
        is_empty = False
        if not class_info_list:
            is_empty = True

        return render(request, 'mz_eduadmin/classes/index.html',
                  {'class_info_list': class_info_list,
                   'edu_admin_class_info': get_edu_admin_class_info(edu_admin_id),
                   'nav': 'classes',
                   'status_list': json.dumps(['招生中', '停止招生', '已毕业']),
                   'career_course_list': json.dumps(career_course_list) ,
                   'teacher_list': json.dumps(teacher_list),
                   'is_empty': is_empty,
                   'edu_admin_name': get_edu_admin_name_by_id(edu_admin_id),
                   'edu_admin_id': edu_admin_id})

    return HttpResponse('')

@eduadmin_required
def update_state(request):
    class_id = long(request.GET.get('i'))
    class_state = request.GET.get('e')
    update_class_state(class_id, class_state)

    return HttpResponse('ok')

@eduadmin_required
def create_class(request):
    if (not request.POST.get('career_course')):
        return JsonResponse({'status':False, "message":"专业不能为空"})
    if (not request.POST.get('class_no')):
        return JsonResponse({'status':False, "message":"班级编号不能为空"})
    if (not request.POST.get('teacher1')):
        return JsonResponse({'status':False, "message":"教师不能为空"})
    if (not request.POST.get('edu_admin')):
        return JsonResponse({'status':False, "message":"教务不能为空"})
    if (not request.POST.get('qq_group')):
        return JsonResponse({'status':False, "message":"qq群号不能为空"})
    if (not request.POST.get('key_group')):
        return JsonResponse({'status':False, "message":"qq群key不能为空"})
    if (not request.POST.get('image')):
        return JsonResponse({'status':False, "message":"必须选上传QQ群二维码"})

    create_parameters = dict(career_course=long(request.POST.get('career_course')),
                             class_no=request.POST.get('class_no'),
                             teachers=interface.get_teachers_para(request.POST),
                             edu_admin=long(request.POST.get('edu_admin')),
                             qq_group=request.POST.get('qq_group'),
                             key_group=request.POST.get('key_group'),
                             image=request.POST.get('image')[9:],
                             open_yaer=request.POST.get('open_yaer'),
                             open_month=request.POST.get('open_month'),
                             open_day=request.POST.get('open_day'),
                             open_time=int(request.POST.get('open_time')))

    status, msg = check_class_create_parameters(create_parameters)
    if status == False:
        return JsonResponse({'status': False, "message": msg})
    try:
        interface.create_class(create_parameters)
    except:
        return JsonResponse({'status':False, "message":"创建失败请稍后再试！"})

    return JsonResponse({'status':True, "message":"创建成功"})

@eduadmin_required
def get_class_teachers(request):
    try:
        class_id = long(request.GET.get('s'))
        teachers = interface.get_teachers_by_class_id(class_id)
        return JsonResponse({'status':True, "message":teachers})
    except:
        return JsonResponse({'status':False, "message":"获取老师信息失败！"})

@eduadmin_required
def update_class_teachers(request, class_id):
    try:
        teachers = interface.get_teachers_para(request.POST, 'addTeacherv')
        if not teachers:
            return JsonResponse({'status':False, "message":"班级老师不能为空！"})
        interface.update_teacher(class_id, teachers)
        return JsonResponse({'status':True, "message":""})
    except:
        return JsonResponse({'status':False, "message":"更新老师信息失败！"})