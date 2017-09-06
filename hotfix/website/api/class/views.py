# -*- coding: utf-8 -*-
from core.common.http.response import success_json, failed_json
from mz_lps.models import ClassStudents, Class
from mz_lps3.functions import get_classmeeting_list
from mz_lps4.interface import get_student_meeting_list_interface
from utils.is_logined import student_in_career_required
from utils.logger import logger as log
from utils.tool import get_param_by_request
from website.api.user.decorators import app_user_required
from django.conf import settings
from mz_lps4.class_dict import NORMAL_CLASS_DICT, LPS4_DICT, week_day_dict
from website.api.user.interface import get_student_class_type


# 我的班级
@app_user_required
def app_my_class(request):
    user = request.user
    obj_list = ClassStudents.objects.filter(
            user=user, student_class__class_type__in=[0, 2], status=1)\
        .values_list('student_class_id', 'student_class__career_course_id')
    obj_dict = {}
    for student_class_id, career_course_id in obj_list:
        if obj_dict.get(career_course_id):
            if Class.objects.xall().get(id=int(student_class_id)).class_type == 0:
                obj_dict[career_course_id] = student_class_id
        else:
            obj_dict[career_course_id] = student_class_id
    data = []
    for career_id, class_id in obj_dict.iteritems():
        klass = Class.objects.xall().get(id=int(class_id))
        lps = 3 if klass.lps_version == '3.0' else 2
        if int(klass.id) in NORMAL_CLASS_DICT.values():
            lps = 4
        data.append(dict(
            is_classed=True,
            is_can_pay=klass.career_course.is_class,
            is_payed=True if klass.class_type == 0 else False,
            career_id=klass.career_course.id,
            career_name=klass.career_course.name,
            img_url=settings.SITE_URL + settings.MEDIA_URL + str(klass.career_course.app_career_image),
            student_count=klass.career_course.student_count,
            status='已报名' if klass.class_type == 0 and klass.lps_version == '3.0' else '体验班',
            lps=lps,
            small_img_url=settings.SITE_URL + settings.MEDIA_URL + str(klass.career_course.image),
            career_url=settings.SITE_URL + '/course/%s-px' % klass.career_course.short_name,
        ))
    return success_json({'list': data})


# 班会
@app_user_required
def app_meeting(request):
    user = request.user
    klass_id = request.POST.get('class_id', None)
    career_id = request.POST.get('ccourse_id', None)
    page = get_param_by_request(request.POST, "page", 1, int)
    data = []

    if not klass_id:
        # 老版本使用
        class_student = ClassStudents.objects.filter(user=user, student_class__class_type=Class.CLASS_TYPE_NORMAL,
                                                     status=1)
        # 没有学生报班信息，返回空的
        if not class_student:
            return success_json({'status': 0, 'list': [], 'career_url': settings.SITE_URL + '/course/'})
        # 如果没有在此职业课程里，也返回空的
        if career_id and not class_student.filter(student_class__career_course_id=career_id):
            return success_json({'status': 0, 'list': [], 'career_url': settings.SITE_URL + '/course/'})

        for obj in class_student:
            class_id = obj.student_class_id
            class_meeting_lst = get_classmeeting_list(class_id, user.id)
            data += class_meeting_lst
        for class_meeting in data:
            date_time = class_meeting['datetime'].strftime('%Y-%m-%d')
            class_meeting['datetime'] = date_time
            # 兼容4.0班会改状态
            try:
                _status = class_meeting['status']
                if _status == 1:
                    class_meeting['status'] = 3
                elif _status == 2:
                    class_meeting['status'] = 1
            except Exception as e:
                log.error(str(e))
        return success_json({'list': data, 'career_url': settings.SITE_URL + '/course/'})

    else:
        # lps 4
        if int(klass_id) in NORMAL_CLASS_DICT.values():
            try:
                student_in_career_required(request)
            except Exception as e:
                log.warn('student_in_career_required error.class_id %s.%s.' % (klass_id, str(e)))
                return failed_json(unicode(e))

            career_id = LPS4_DICT[int(klass_id)]
            # 获取约课信息
            try:
                meeting_list = get_student_meeting_list_interface(career_id, user)
            except Exception as e:
                return failed_json(unicode(e))
            return success_json(meeting_list)
        else:
            # lps 3
            is_pay = get_student_class_type(user, klass_id)
            if not is_pay:
                return success_json({'status': 0, 'list': [], 'career_url': settings.SITE_URL + '/course/'})
            class_meeting_lst = get_classmeeting_list(klass_id, user.id)
            if page > 1:
                class_meeting_lst = []
            for class_meeting in class_meeting_lst:
                class_meeting['week_time'] = week_day_dict[class_meeting['datetime'].weekday()]
                date_time = class_meeting['datetime'].strftime('%Y-%m-%d')
                class_meeting['datetime'] = date_time
                # 兼容4.0班会改状态
                try:
                    _status = class_meeting['status']
                    if _status == 1:
                        class_meeting['status'] = 3
                    elif _status == 2:
                        class_meeting['status'] = 1
                except Exception as e:
                    log.error(str(e))
            return success_json({'list': class_meeting_lst, 'career_url': settings.SITE_URL + '/course/',
                                 'status': 1})
