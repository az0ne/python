#!/usr/bin/env python
# -*- coding:utf-8 -*-
from utils.handle_exception import handle_http_response_exception
from utils.decorators import dec_login_required
from utils import tool
import db.api.course.careerPublicMeeting
from django.shortcuts import render
from django.core.urlresolvers import reverse
from utils.logger import logger as log
from django.http import HttpResponseRedirect
from utils.tool import get_correct_url

CURRENT_URL = ''

@dec_login_required
@handle_http_response_exception(501)
def career_public_meeting_list(request):
    action = tool.get_param_by_request(request.GET, "action", "query", str)
    keyword = ""
    global CURRENT_URL
    CURRENT_URL = request.get_full_path()
    if "search" in action:
        keyword = tool.get_param_by_request(request.GET, "keyword", "", str)
        get_result = db.api.course.careerPublicMeeting.get_public_meeting_by_keyword('%' + keyword + '%', )
    else:
        get_result = db.api.course.careerPublicMeeting.list_public_meeting()
    if get_result.is_error():
        log.warn("get career public meeting error.")
        return render(request, "404.html", {})
    result = get_result.result()
    return render(request, "mz_course/careerPublicMeeting/careerPublicMeeting_list.html", {"meetings": result,
                                                                                            "keyword": keyword})


@dec_login_required
@handle_http_response_exception(501)
def career_public_meeting_edit(request):
    action = tool.get_param_by_request(request.GET, "action", "edit", str)
    _id = tool.get_param_by_request(request.GET, "id", 0, int)
    result = db.api.course.careerPublicMeeting.get_public_meeting_by_id(_id)
    meeting = ""
    if result.is_error():
        log.warn("get career public meeting by id error.id:%s" % _id)
        return render(request, "404.html", {})
    if result.result():
        meeting = result.result()[0]
        meeting["utc_time"] = meeting["class_time"].strftime("%Y-%m-%dT%H:%M:%S")
    data = {"action": action, "meeting": meeting}
    return render(request, "mz_course/careerPublicMeeting/careerPublicMeeting_edit.html", data)


@dec_login_required
@handle_http_response_exception(501)
def career_public_meeting_save(request):
    class_time = tool.get_param_by_request(request.POST, "class_time", "", str)
    enter_qq = tool.get_param_by_request(request.POST, "enter_qq", 1, int)
    _id = tool.get_param_by_request(request.POST, "id", 0, int)
    result = db.api.course.careerPublicMeeting.update_public_meeting_by_id(class_time=class_time,
                                                                           enter_qq=enter_qq,
                                                                           _id=_id)
    if result.is_error():
        log.warn("update career public meeting error.")
        return render(request, "404.html", {})
    return HttpResponseRedirect(get_correct_url(CURRENT_URL, reverse("mz_course:public_meeting_list")))

