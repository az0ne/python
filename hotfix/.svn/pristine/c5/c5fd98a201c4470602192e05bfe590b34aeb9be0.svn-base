# -*- coding: utf-8 -*-
from django.shortcuts import render
import db.api.course.careerPublicMeeting
import db.api.course.career_course
import db.api.user.user
from utils.tool import logger as log
from utils import tool
import datetime
from django.http import JsonResponse
from django.http.response import Http404
from interface_publicMeeting import public_meeting_send_success_sms



def public_meeting_show(request,career_id):
    task_info = dict()
    get_result = db.api.course.careerPublicMeeting.get_public_meeting_by_id(career_id)
    if get_result.is_error():
        log.warn("get public meeting by id is error. id=%s" % career_id)
        raise Http404()
    result = get_result.result()
    if result:
        time = str(result["class_time"])
        result["time_tuple"] = (time[:4],time[5:7],time[8:10],time[11:12],time[12:13],time[14:15],time[15:16])
        enter_qq = str(result["enter_qq"])
        qq_info = dict(qq_group=result["qq_group_"+enter_qq],
                    qq_image=result["qq_image_"+enter_qq],
                    qq_group_key=result["qq_group_key_"+enter_qq])

        free_task_id = result["free_task_id"]
        if free_task_id > 0:
            get_task_info_result = db.api.course.careerPublicMeeting.get_public_meeting_task_info_by_task_id(free_task_id)
            if get_task_info_result.is_error():
                log.warn("get task info  by free_task_id is error. free_task_id=%s" % free_task_id)
                raise Http404()
            task_info = get_task_info_result.result()

        teacher_id = result["teacher_id"]
        get_teacher = db.api.course.career_course.get_page_teacher_by_teacher_id(teacher_id=teacher_id)
        if get_teacher.is_error():
             log.warn("get career_page_teacher by teacher_id is error. teacher_id=%s" % teacher_id)
             raise Http404()
        teacher = get_teacher.result()

        if teacher:
            get_teacher_info = db.api.user.user.get_user_by_id(teacher_id)
            if get_teacher_info.is_error():
                log.warn("get user info by id is error. id=%s" % teacher_id)
                raise Http404
            teacher["avatar_url"] = get_teacher_info.result()["avatar_url"]
        return render(request,"mz_course/course_appointment.html", {"qq_info": qq_info,"meeting": result,
                                                                "teacher": teacher, "task": task_info})
    else:
        raise Http404()


def public_meeting_save(request):
    career_id = tool.get_param_by_request(request.POST, "career_id", 0, int)
    mobile = tool.get_param_by_request(request.POST, "mobile", "", str)
    task_title = tool.get_param_by_request(request.POST, "task_title", "", str)
    enter_date = datetime.datetime.now()
    class_time = tool.get_param_by_request(request.POST, "class_time", "", str)
    qq_group = tool.get_param_by_request(request.POST, "qq_group", "", str)
    data = dict(career_id=career_id,mobile=mobile,enter_date=enter_date,class_time=class_time,qq_group=qq_group)

    add_result = db.api.course.careerPublicMeeting.insert_public_meeting_data(data)
    if add_result.is_error():
        log.warn("insert into mz_career_public_meeting error.data:{}".format(data))
        return JsonResponse({'status': 'fail'})

    public_meeting_send_success_sms(task_title, mobile, class_time, qq_group,"public_meeting_success_notify")  # 发送预约成功的短信
    return JsonResponse({'status': 'success'})

