#!/usr/bin/env python
# -*- coding: utf8 -*-
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from wechat_course_interface import *
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from utils.tool import get_param_by_request, upload
from utils.logger import logger as log
from django.shortcuts import render
from django.core.urlresolvers import reverse


@dec_login_required
@handle_http_response_exception(501)
def wechat_course_list(request):
    action = get_param_by_request(request.GET, "action", "query", str)
    page_index = get_param_by_request(request.GET, "page_index", 1, int)
    try:
        if "search" in action:
            career_course_id = get_param_by_request(request.GET, "career_course_id", 0, int)

            result = list_all_wechat_course_by_search(page_index=page_index, page_size=settings.PAGE_SIZE,
                                                      career_course_id=career_course_id)
        else:
            result = list_all_wechat_course(page_index=page_index, page_size=settings.PAGE_SIZE)
        career_course = list_all_wechat_career_course()
    except Http404:
        return render(request, "404.html")
    request.session["course_list_url"] = request.get_full_path()
    c = {"action": action, "wechat_course": result["result"], "career_course": career_course,
         "page": {"page_index": page_index, "page_size": settings.PAGE_SIZE,
                  "rows_count": result["rows_count"], "page_count": result["page_count"],
                  }
         }
    return render(request, "mz_micro/wechat_course/wechat_course_list.html", c)


@dec_login_required
@handle_http_response_exception(501)
def wechat_lesson_list(request):
    action = get_param_by_request(request.GET, "action", "query", str)
    page_index = get_param_by_request(request.GET, "page_index", 1, int)
    course_id = get_param_by_request(request.GET, "course_id", 0, int)
    try:
        result = list_all_wechat_lesson(page_index=page_index, page_size=settings.PAGE_SIZE, course_id=course_id)
    except Http404:
        return render(request, "404.html")
    request.session["lesson_list_url"] = request.get_full_path()
    c = {"action": action, "lessons": result["result"], "course_id": course_id,
         "page": {"page_index": page_index, "page_size": settings.PAGE_SIZE,
                  "rows_count": result["rows_count"], "page_count": result["page_count"],
                  }
         }
    return render(request, "mz_micro/wechat_course/wechat_lesson_list.html", c)


@dec_login_required
@handle_http_response_exception(501)
def list_wechat_career_course(request):
    try:
        result = list_all_wechat_career_course()
    except Http404:
        return JsonResponse(dict(status="failed"))
    return JsonResponse(dict(status="success", result=result))


@dec_login_required
@handle_http_response_exception(501)
def wechat_course_edit(request):
    _id = get_param_by_request(request.GET, "course_id", 0, int)
    action = get_param_by_request(request.GET, "action", "add", str)
    course_info = dict()
    try:
        if _id and "add" not in action:
            course_info = get_wechat_course_by_id(course_id=_id)
            if course_info:
                course_info["date_publish"] = course_info.get("date_publish").strftime("%Y-%m-%dT%H:%M:%S")
        career_course = list_all_career_course()
    except Http404:
        return render(request, "404.html")
    return render(request, "mz_micro/wechat_course/wechat_course_edit.html", dict(action=action,
                                                                                  course_info=course_info,
                                                                                  career_course=career_course))


@dec_login_required
@handle_http_response_exception(501)
def wechat_lesson_edit(request):
    lesson_id = get_param_by_request(request.GET, "lesson_id", 0, int)
    action = get_param_by_request(request.GET, "action", "add", str)
    lesson = dict()
    try:
        if action == "edit" and lesson_id:
            lesson = get_wechat_lesson_by_id(lesson_id=lesson_id)
            lesson["lesson_id"] = lesson_id
            course_name = lesson.get("course_name", "")
            course_id = lesson.get("course_id", 0)
        else:
            course_id = get_param_by_request(request.GET, "course_id", 0, int)
            course = get_wechat_course_by_id(course_id)
            course_name = course.get("course_name", "")
    except Http404:
        return render(request, "404.html")
    return render(request, "mz_micro/wechat_course/wechat_lesson_edit.html", dict(action=action,
                                                                                  course_info=dict(course_id=course_id,
                                                                                                   course_name=course_name),
                                                                                  lesson=lesson))


@dec_login_required
@handle_http_response_exception(501)
def add_wechat_career_course(request):
    action = get_param_by_request(request.POST, "action", "edit", str)
    name = get_param_by_request(request.POST, 'name', "", str)
    index = get_param_by_request(request.POST, 'index', 999, int)
    if name and index:
        try:
            if "add" in action:
                insert_wechat_career_course(name, index)
            elif "edit" in action:
                _id = get_param_by_request(request.POST, "id", 0, int)
                update_wechat_career_course(name=name, index=index, _id=_id)
        except Http404:
            return render(request, "404.html")
        return JsonResponse(dict(status="success"))
    return JsonResponse(dict(status="failed"))


@dec_login_required
@handle_http_response_exception(501)
def add_wechat_course(request):
    action = get_param_by_request(request.POST, "action", "add", str)
    old_image = get_param_by_request(request.POST, "old_image", "", str)
    name = get_param_by_request(request.POST, 'name', "", str)
    image = request.FILES.get('image', None)
    description = get_param_by_request(request.POST, 'description', "", str)
    is_active = get_param_by_request(request.POST, "is_active", 0, int)
    date_publish = get_param_by_request(request.POST, "date_publish", "", str)
    student_count = get_param_by_request(request.POST, "student_count", 0, int)
    index = get_param_by_request(request.POST, "index", 999, int)
    _id = get_param_by_request(request.POST, "id", 0, int)
    teacher_id = get_param_by_request(request.POST, "teacher_id", 0, int)
    career_course_id = get_param_by_request(request.POST, "career_course_id", 0, int)
    price = get_param_by_request(request.POST, "price", 0, float)
    web_career_id = get_param_by_request(request.POST, "web_career_id", 0, int)

    if image:
        image_url = upload(image, settings.UPLOAD_IMG_PATH)
    else:
        image_url = old_image

    dict_course = dict(name=name, image_url=image_url, description=description, is_active=check_is_active(is_active),
                       date_publish=date_publish, student_count=student_count, index=index, teacher_id=teacher_id,
                       career_course_id=career_course_id, price=price, web_career_id=web_career_id, id=_id)
    try:
        if "add" in action:
            insert_wechat_course(dict_course=dict_course)
        elif "edit" in action:
            update_wechat_course(dict_info=dict_course)
    except Http404:
        return render(request, "404.html")
    return HttpResponseRedirect(request.session.get("course_list_url", reverse("mz_wechat:wechat_course_list")))


@dec_login_required
@handle_http_response_exception(501)
def add_wechat_lesson(request):
    action = get_param_by_request(request.POST, "action", "query", str)
    name = get_param_by_request(request.POST, 'name', "", str)
    video_url = get_param_by_request(request.POST, 'video_url', "", str)
    video_length = get_param_by_request(request.POST, "video_length", 0, int)
    play_count = get_param_by_request(request.POST, "play_count", 0, int)
    index = get_param_by_request(request.POST, "index", 999, int)
    need_pay = get_param_by_request(request.POST, "need_pay", 0, int)
    course_id = get_param_by_request(request.POST, "course_id", 0, int)
    dict_lesson = dict(name=name, video_length=video_length, video_url=video_url, play_count=play_count, index=index,
                       need_pay=check_is_active(need_pay), course_id=course_id)

    try:
        if "add" in action:
            insert_wechat_lesson(dict_lesson)
        elif "edit" in action:
            _id = get_param_by_request(request.POST, "lesson_id", 0, int)
            dict_lesson["id"] = _id

            update_wechat_lesson(dict_lesson)
        else:
            log.warn("the value of action error.")
    except Http404 as e:
        log.warn("modify the table of mz_wechat_lesson failed. info:%s" % e)
        return render(request, "404.html")
    return HttpResponseRedirect(request.session.get("lesson_list_url", reverse("mz_wechat:wechat_course_list")))


@dec_login_required
@handle_http_response_exception(501)
def del_wechat_lesson(request):
    lesson_id = get_param_by_request(request.GET, "lesson_id", 0, int)
    try:
        delete_wechat_lesson(lesson_id)
    except Http404:
        return render(request, "404.html")
    return HttpResponseRedirect(request.session.get("lesson_list_url", reverse("mz_wechat:wechat_course_list")))


@dec_login_required
@handle_http_response_exception(501)
def del_wechat_course(request):
    course_id = get_param_by_request(request.GET, "course_id", 0, int)
    try:
        delete_wechat_course(course_id)
    except Http404:
        return render(request, "404.html")
    return HttpResponseRedirect(request.session.get("course_list_url", reverse("mz_wechat:wechat_course_list")))


@dec_login_required
@handle_http_response_exception(501)
def get_career_course_by_id(request):
    _id = get_param_by_request(request.POST, "id", 0, int)
    try:
        career = get_wechat_career_by_id(_id)
    except Http404:
        return JsonResponse(dict(status="failed"))
    return JsonResponse(dict(status="success", career=career))
