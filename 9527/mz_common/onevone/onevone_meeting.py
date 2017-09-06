# -*- coding: utf8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
from utils.logger import logger as log
import db.api.common.onevone.onevone_meeting
import db.api.lps4.career.lps4_careerData
from django.conf import settings


@dec_login_required
@handle_http_response_exception(501)
def onevone_meeting_edit(request):
    STATUS = {"CREATE": "已创建", "DATED": "已预约", "ENDED": "已结束", "START": "已开始"}
    action = get_param_by_request(request.GET, "action", "show", str)
    _id = get_param_by_request(request.GET, "id", 0, int)
    meeting = None
    if _id > 0:
        APIResult = db.api.common.onevone.onevone_meeting.get_onevone_meeting_by_id(_id)
        if APIResult.is_error():
            log.warn("get onevone meeting failed.")
            return render(request, "404.html", {"message": "get onevone meeting failed."})
        meeting = APIResult.result()
        if meeting:
            status = meeting["status"]
            meeting["status_name"] = STATUS[status] if status in STATUS else status
            if action == "edit":
                meeting["start_time"] = meeting["start_time"].strftime('%Y-%m-%dT%H:%M')
                meeting["end_time"] = meeting["end_time"].strftime('%Y-%m-%dT%H:%M')
    return render(request, "mz_common/onevone/onevone_meeting_edit.html", dict(action=action,
                                                                               meeting=meeting))


@dec_login_required
@handle_http_response_exception(501)
def onevone_meeting_list(request):
    action = get_param_by_request(request.GET, "action", "query", str)
    page_index = get_param_by_request(request.GET, "page_index", 1, int)
    keywords = dict()
    request.session["url_back"] = request.get_full_path()
    if action == "search":
        career_id = get_param_by_request(request.GET, "career", 0, int)
        status = get_param_by_request(request.GET, "status", "", str)
        start_time = get_param_by_request(request.GET, "start_time", "", str)
        nick_name = get_param_by_request(request.GET, "nick_name", "", str)
        phone = get_param_by_request(request.GET, "phone", "", str)
        user_id = get_param_by_request(request.GET, "user_id", 0, int)
        keywords = dict(career_id=career_id, status=status, start_time=start_time, nick_name=nick_name, phone=phone,
                        user_id=user_id)
        APIResult = db.api.common.onevone.onevone_meeting.list_onevone_meeting_on_search(page_index=page_index,
                                                                                         page_size=settings.PAGE_SIZE,
                                                                                         data=keywords)
    else:
        APIResult = db.api.common.onevone.onevone_meeting.list_onevone_meeting(page_index=page_index,
                                                                               page_size=settings.PAGE_SIZE)
    if APIResult.is_error():
        log.warn("list onevone meetings failed.")
        return render(request, "404.html", {"message": "list onevone meeting failed."})
    result = APIResult.result()
    get_careers = db.api.lps4.career.lps4_careerData.get_all_lps4_career()
    if get_careers.is_error():
        log.warn("get all lps4 career failed.")
        return render(request, "404.html", {"message": "get all lps4 career failed."})
    careers = get_careers.result()
    c = {"meetings": result["result"], "keywords": keywords, "careers": careers,
         "page": {"page_index": page_index, "rows_count": result["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": result["page_count"]}}
    return render(request, "mz_common/onevone/onevone_meeting_list.html", c)


@dec_login_required
@handle_http_response_exception(501)
def onevone_meeting_update(request):
    _id = get_param_by_request(request.POST, "id", 0, int)
    video_url = get_param_by_request(request.POST, "video_url", "", str)
    video_token = get_param_by_request(request.POST, "video_token", "", str)
    start_time = get_param_by_request(request.POST, "start_time", "", str)
    end_time = get_param_by_request(request.POST, "end_time", "", str)
    data = dict(id=_id, video_url=video_url, start_time=start_time, end_time=end_time, video_token=video_token)
    if _id > 0:
        APIResult = db.api.common.onevone.onevone_meeting.update_onevone_meeting_by_id(data)
        if APIResult.is_error():
            log.warn("update onevone meeting failed.")
            return render(request, "404.html", {})
    return HttpResponseRedirect(request.session.get("url_back", reverse("mz_common:onevone_meeting_list")))


@dec_login_required
@handle_http_response_exception(501)
def onevone_meeting_delete(request):
    _id = get_param_by_request(request.GET, "id", 0, int)
    if _id > 0:
        APIResult = db.api.common.onevone.onevone_meeting.delect_onevone_meeting_by_id(_id)
        if APIResult.is_error():
            log.warn("delete onevone meeting failed.")
            return render(request, "404.html", {})
    return HttpResponseRedirect(request.session.get("url_back", reverse("mz_common:onevone_meeting_list")))


@dec_login_required
@handle_http_response_exception(501)
def onevone_meeting_update_status(request):
    _id = get_param_by_request(request.POST, "id", 0, int)
    status = get_param_by_request(request.POST, "status", "", str)
    if _id and status:
        APIResult = db.api.common.onevone.onevone_meeting.update_onevone_status_by_id(status=status, _id=_id)
        if APIResult.is_error():
            log.warn("update onevone meeting status failed.")
    return HttpResponseRedirect(request.session.get("url_back", reverse("mz_common:onevone_meeting_list")))
