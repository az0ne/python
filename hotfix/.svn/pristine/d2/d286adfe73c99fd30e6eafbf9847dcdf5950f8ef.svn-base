# -*- coding: utf-8 -*-

__author__ = 'lewis'
import interface, datetime
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from mz_user.models import UserProfile
from mz_lps3.models import ClassMeeting, Class
from mz_lps3.functions import get_attendance_info
from mz_common.decorators import eduadmin_required


@eduadmin_required
def get_living(request):
    """获取直播排期主页"""
    user = request.user
    # user=UserProfile.objects.get(pk=20276)
    start_date, end_date, step_prev, step_next = interface.get_week_time()
    living_data, is_data = interface.LivingSchedule(user.id, start_date, end_date).get_living_data()
    nav = 'living'
    return render(request, 'mz_eduadmin/living/index.html', locals())


@eduadmin_required
def ajax_living_page(request):
    """异步请求获取直播排期HTML"""
    user = request.user
    # user=UserProfile.objects.get(pk=20276)
    step = int(request.REQUEST.get('step', 0))
    edu_admin_id = int(request.REQUEST.get('edu_admin_id', user.id))
    start_date, end_date, step_prev, step_next = interface.get_week_time(step)
    living_data, is_data = interface.LivingSchedule(edu_admin_id, start_date, end_date).get_living_data()
    return render(request, 'mz_eduadmin/living/div_living_content.html', locals())


@eduadmin_required
def ajax_living_attendance(request, class_id, classmeeting_id):
    """异步获取考勤数据"""
    update = request.REQUEST.get('update')
    if update:
        is_update = True
    else:
        is_update = False

    class_meeting = get_object_or_404(ClassMeeting, id=int(classmeeting_id))
    try:
        class_obj = Class.objects.xall().get(id=int(class_id), lps_version='3.0')
    except:
        raise Http404

    try:
        teacher = UserProfile.objects.get(id=class_meeting.create_id)
        teacher_name = teacher.staff_name
    except UserProfile.DoesNotExist:
        teacher_name = class_obj.teacher.staff_name

    edu_admin_name = class_obj.edu_admin.staff_name
    setattr(class_meeting, 'd_week', interface.get_week_value(class_meeting.startline.weekday()))
    setattr(class_meeting, 'd_date', class_meeting.startline.strftime("%Y-%m-%d"))
    setattr(class_meeting, 'd_time', class_meeting.startline.strftime("%H:%M"))

    punctual_user_lst, late_user_lst, absent_user_lst, _ = get_attendance_info(class_meeting, class_id=class_id,
                                                                               is_update=is_update)
    punctual_user_count = len(punctual_user_lst)
    late_user_count = len(late_user_lst)
    absent_user_count = len(absent_user_lst)
    attendance = int(round(
        (punctual_user_count + late_user_count) * 1.0 / (punctual_user_count + late_user_count + absent_user_count),
        3) * 100)
    return render(request, 'mz_eduadmin/living/div_attendance.html', locals())
