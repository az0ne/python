#!/usr/bin/env python
# -*- coding: utf8 -*-
from django.http import HttpResponseRedirect
from django.conf import settings

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request, upload
from utils.logger import logger as log
from django.shortcuts import render
from django.core.urlresolvers import reverse
import db.api.micro.wechat_course.wechat_course_question


@dec_login_required
@handle_http_response_exception(501)
def wechat_question_list(request):
    action = get_param_by_request(request.GET, "action", "query", str)
    page_index = get_param_by_request(request.GET, "page_index", 1, int)
    APIResult = db.api.micro.wechat_course.wechat_course_question.list_wechat_question(page_index=page_index,
                                                                                       page_size=settings.PAGE_SIZE)
    request.session["wechat_question_list"] = request.get_full_path()
    if APIResult.is_error():
        log.warn("list wechat question failed.")
        return render(request, "404.html")
    result = APIResult.result()
    c = {"action": action, "questions": result["result"],
         "page": {"page_index": page_index, "page_size": settings.PAGE_SIZE,
                  "rows_count": result["rows_count"], "page_count": result["page_count"]}}
    return render(request, "mz_micro/wechat_course/wechat_course_question_list.html", c)


@dec_login_required
@handle_http_response_exception(501)
def wechat_question_edit(request):
    action = get_param_by_request(request.GET, "action", "query", str)
    _id = get_param_by_request(request.GET, "question_id", 0, int)
    result = dict()
    if "edit" in action:
        APIResult = db.api.micro.wechat_course.wechat_course_question.get_wechat_question_by_id(_id)
        if APIResult.is_error():
            log.warn("get wechat question by id failed.")
            return render(request, "404.html")
        result = APIResult.result()

    c = {"action": action, "question": result}
    return render(request, "mz_micro/wechat_course/wechat_course_question_edit.html", c)


@dec_login_required
@handle_http_response_exception(501)
def wechat_question_del(request):
    _id = get_param_by_request(request.GET, "question_id", 0, int)
    APIResult = db.api.micro.wechat_course.wechat_course_question.delete_wechat_question_by_id(_id)
    if APIResult.is_error():
        log.warn("delete wechat question by id failed.")
        return render(request, "404.html")
    return HttpResponseRedirect(
        request.session.get("wechat_question_list", reverse("mz_wechat:wechat_course_question_list")))


@dec_login_required
@handle_http_response_exception(501)
def wechat_question_save(request):
    action = get_param_by_request(request.POST, "action", "add", str)
    question_id = get_param_by_request(request.POST, "question_id", 0, int)
    question = get_param_by_request(request.POST, "question", "", str)
    answer = get_param_by_request(request.POST, "answer", "", str)
    nick_name = get_param_by_request(request.POST, "nick_name", "", str)
    course_id = get_param_by_request(request.POST, "course_id", 0, int)
    old_avatar_url = get_param_by_request(request.POST, "old_avatar_url", "", str)
    image = request.FILES.get('image', None)
    if image:
        avatar_url = upload(image, settings.UPLOAD_IMG_PATH)
    else:
        avatar_url = old_avatar_url
    question_dict = dict(id=question_id, question=question, answer=answer,
                         nick_name=nick_name, course_id=course_id, avatar_url=avatar_url)
    if "edit" in action:
        APIResult = db.api.micro.wechat_course.wechat_course_question.update_wechat_question_by_id(question_dict)
        if APIResult.is_error():
            log.warn("update wechat question failed.")
            return render(request, "404.html")
    elif "add" in action:
        APIResult = db.api.micro.wechat_course.wechat_course_question.insert_wechat_question(question_dict)
        if APIResult.is_error():
            log.warn("insert wechat question failed.")
            return render(request, "404.html")

    return HttpResponseRedirect(
        request.session.get("wechat_question_list", reverse("mz_wechat:wechat_course_question_list")))
