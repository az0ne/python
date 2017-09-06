# -*- coding: utf-8 -*-
from datetime import datetime

from django.http.response import Http404, JsonResponse
from django.views.decorators.http import require_GET

from mz_common.decorators import student_required
from mz_lps.models import ClassStudents
from mz_lps3.functions_yf import format_date, add_date
from mz_lps3.models import ClassMeetingAttendance, ClassMeeting


@require_GET
@student_required
def calender_detail(request, class_id):
    if not request.is_ajax():
        raise Http404()
    cur_user = request.user
    # uid = request.GET['uid']        # test
    # cur_user = UserProfile.objects.get(pk=uid)  # test

    if not class_id:
        return JsonResponse(
            {'status': False, 'message': 'no class id'}, status=404)
    try:
        cs = ClassStudents.objects.get(student_class_id=class_id, user=cur_user)
        cls = cs.student_class
    except ClassStudents.DoesNotExist:
        return JsonResponse(
            {'status': False, 'message': 'not find class'}, status=404)

    now = datetime.now()
    data = {
        format_date(cls.meeting_start or now): u'开学日',
        format_date(
            add_date(cls.meeting_start or now,
                     cls.meeting_duration or 90)): u'毕业日',
        format_date(datetime.now()): u'今天'
    }

    cm_ids = ClassMeeting.objects.filter(    # 获取此班级下的所有班会id
        classmeetingrelation__class_id=class_id)\
        .values_list('id', flat=True)
    cmas = ClassMeetingAttendance.objects.filter(   # 获取考勤记录
        class_meeting_id__in=cm_ids, student_id=cur_user.id)
    for cma in cmas:
        if cma.class_meeting.status == 1:
            data[format_date(cma.class_meeting.startline)] = cma.status_text

    cms = ClassMeeting.objects.filter(    # 获取未开始的班会
        classmeetingrelation__class_id=class_id, startline__gt=datetime.now())
    for cm in cms:
        data[format_date(cm.startline)] = u'班会'

    return JsonResponse({'status': True, 'data': data})
