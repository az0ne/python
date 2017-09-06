#!/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.handle_exception import handle_http_response_exception
from utils.decorators import dec_login_required
from utils import tool
from utils.tool import get_correct_url
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.conf import settings
from db.api.micro import micro_course as api_micro_course
from db.api.course import careerCourse as api_careerCourse
from db.api.admin import user as api_user
import sys
from django.core.urlresolvers import reverse

reload(sys)
sys.setdefaultencoding('utf8')

STATUS_CODE = {
    '-2': '已过期',
    '-1': '未发布',
    '0': '未开始',
    '1': '进行中',
    '2': '已经结束'
}

@dec_login_required
@handle_http_response_exception(501)
def webcast_edit(request):
    '''
    直播课堂 新增，修改，以及查看页面的view
    :param request:
    :return:
    '''
    action = tool.get_param_by_request(request.GET, 'action', 'add', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    micro_course = None
    if 'add' not in action:
        _id = tool.get_param_by_request(request.GET, 'id')
        get_micro_ret = api_micro_course.get_micro_by_id(_id)
        if get_micro_ret.is_error():
            return render(request, "404.html", {})
        if get_micro_ret.result():
            micro_course = get_micro_ret.result()[0]
            micro_course['status_des'] = STATUS_CODE.get(str(micro_course['status']), '状态错误')
            get_user_info = api_user.get_userprofileinfo_by_id(micro_course['teacher_id']).result()
            if get_user_info:
                micro_course['teacher_name'] = get_user_info[0]['nick_name']

    get_careerCourses = api_careerCourse.list_career_course_name()
    if get_careerCourses.is_error():
        return render(request, '404.html', {})
    careerCourses = get_careerCourses.result()
    return render(request, "mz_micro/webcast_add.html", {'action': action, 'micro_course': micro_course,
                                                         'page_index': page_index,
                                                         'careerCourses': careerCourses})


@dec_login_required
@handle_http_response_exception(501)
def webcast_list(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    keyword = ''
    request.session["url_back"] = request.get_full_path()
    if 'search' in action:
        keyword = tool.get_param_by_request(request.GET, 'keyword', '', str)
        get_micro_courses = api_micro_course.get_micro_by_keyword(page_index, settings.PAGE_SIZE, '%' + keyword + '%', )
    else:
        get_micro_courses = api_micro_course.list_micro_course_by_page(page_index, settings.PAGE_SIZE)

    if get_micro_courses.is_error():
        return render(request, "404.html", {})
    micro_courses = get_micro_courses.result()['result']
    if micro_courses:
        for course in micro_courses:
            course['status_des'] = STATUS_CODE.get(str(course['status']), '状态错误')  # 添加课程状态描述字段

    c = {"micro_courses": micro_courses, 'keyword': keyword,
         "page": {"page_index": page_index, "rows_count": get_micro_courses.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": get_micro_courses.result()["page_count"]}}
    return render(request, "mz_micro/webcast_list.html", c)


@dec_login_required
@handle_http_response_exception(501)
def webcast_save(request):
    """
    新增微课，获取数据在数据库中新增记录
    """
    back_img = request.FILES.get('back_img', '')
    playback_img = request.FILES.get('playback_img', '')
    subject = tool.get_param_by_request(request.POST, 'subject', '', str)
    info = tool.get_param_by_request(request.POST, 'info', '', str)
    vod_url = tool.get_param_by_request(request.POST, 'vod_url', '', str)
    startDate = tool.get_param_by_request(request.POST, 'startDate', '', str)
    invalidDate = tool.get_param_by_request(request.POST, 'invalidDate', '', str)
    teacher_id = tool.get_param_by_request(request.POST, 'teacher_id', 0, int)
    career_id_1 = tool.get_param_by_request(request.POST, 'career_id_1', 0, int)
    career_id_2 = tool.get_param_by_request(request.POST, 'career_id_2', 0, int)
    career_id_3 = tool.get_param_by_request(request.POST, 'career_id_3', 0, int)
    min_student_count = tool.get_param_by_request(request.POST, 'min_student_count', 0, int)
    max_student_count = tool.get_param_by_request(request.POST, 'max_student_count', 0, int)
    back_image_path = ''
    playback_image_path = ''
    if back_img:
        back_image_path = tool.upload(back_img, settings.UPLOAD_IMG_PATH)
    if playback_img:
        playback_image_path = tool.upload(playback_img, settings.UPLOAD_IMG_PATH)
    if startDate > invalidDate:
        startDate, invalidDate = invalidDate, startDate
    course_dict = {'title': subject, 'info': info, 'start_date': startDate,
                   'end_date': invalidDate, 'status': -1, 'back_img': back_image_path,'playback_img':playback_image_path,
                   'vod_url': vod_url, 'teacher_id': teacher_id, 'career_id_1': career_id_1, 'career_id_2': career_id_2,
                   'career_id_3': career_id_3, 'student_count': 0, 'min_student_count': min_student_count,
                   'max_student_count': max_student_count}
    insert_ret = api_micro_course.insert_micro_crouse(course_dict)
    if insert_ret.is_error():
        error_msg = '数据添加失败！'
        return render(request, "404.html", {'message': error_msg})
    return HttpResponseRedirect(request.session.get("url_back", reverse('mz_micro:webcast_list')))


@dec_login_required
@handle_http_response_exception(501)
def webcast_status_change(request):
    """
    更改微课状态
    """
    status = tool.get_param_by_request(request.POST, 'status', -1, int)
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    change_status_ret = api_micro_course.update_status_by_id(status, _id)
    if change_status_ret.is_error():
        return render(request, '404.html', {})
    return HttpResponseRedirect(request.session.get("url_back", reverse('mz_micro:webcast_list')))




@dec_login_required
@handle_http_response_exception(501)
def update_student_by_id(request):
    '''
    更新学生人数
    :param request:
    :return:
    '''
    student_count = tool.get_param_by_request(request.POST, 'student_count', 0, int)
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    min_student_count = tool.get_param_by_request(request.POST, 'min_student_count', 0, int)
    max_student_count = tool.get_param_by_request(request.POST, 'max_student_count', 0, int)
    update_student_ret = api_micro_course.update_student_count_by_id(student_count, min_student_count,
                                                                     max_student_count, _id)
    if update_student_ret.is_error():
        return render(request, '404.html', {})
    return HttpResponseRedirect(request.session.get("url_back", reverse('mz_micro:webcast_list')))




@dec_login_required
@handle_http_response_exception(501)
def update_vod_url_by_id(request):
    '''
    修改点播地址
    :param request:
    :return:
    '''
    vod_url = tool.get_param_by_request(request.POST, 'vod_url', '', str)
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    update_vod_url = api_micro_course.update_vod_url_by_id(vod_url, _id)
    if update_vod_url.is_error():
        return render(request, '404.html', {})
    return HttpResponseRedirect(request.session.get("url_back", reverse('mz_micro:webcast_list')))

@dec_login_required
@handle_http_response_exception(501)
def is_selected_course_time(request):
    '''
    判断课程是否选择了开始时间和结束时间
    :param request:
    :return: TRUE/FALSE
    '''
    _id = tool.get_param_by_request(request.GET, 'id', 0, int)
    if _id > 0:
        is_selected = False
        is_get = api_micro_course.is_selected_course_time(_id).result()
        if is_get:
            if is_get[0]['start_date'] and is_get[0]['end_date']:
                is_selected = True
        return JsonResponse({'is_selected': is_selected})

@dec_login_required
@handle_http_response_exception(501)
def update_course_date_by_id(request):
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    start_date = tool.get_param_by_request(request.POST, 'start_date', None)
    end_date = tool.get_param_by_request(request.POST, 'end_date', None)
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    ret_update = api_micro_course.update_course_date_by_id(start_date=start_date, end_date=end_date, _id=_id)
    if ret_update.is_error():
        return render(request, '404.html', {})
    return HttpResponseRedirect(request.session.get("url_back", reverse('mz_micro:webcast_list')))
