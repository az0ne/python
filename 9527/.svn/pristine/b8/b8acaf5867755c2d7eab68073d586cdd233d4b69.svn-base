#!/usr/bin/env python
# -*- coding:utf-8 -*-
from utils.tool import get_param_by_request
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from django.conf import settings
import db.api.course.liveMeeting
from django.shortcuts import render
from utils.logger import logger as log

STATUS = (u'未开始', u'已结束', u'进行中')

@dec_login_required
@handle_http_response_exception(501)
def liveMeeting_list(request):
    action = get_param_by_request(request.GET, 'action', 'query', str)
    page_index = get_param_by_request(request.GET, 'page_index', 1, int)
    keyword = ''
    if action == 'search':
        keyword = get_param_by_request(request.GET, 'keyword', '', str)
        if keyword in STATUS:
            keyword = STATUS.index(keyword)
        get_meetings = db.api.course.liveMeeting.list_live_meeting_by_keyword(page_index, settings.PAGE_SIZE, '%' + keyword + '%', )
        if get_meetings.is_error():
            return render(request,"404.html", {})
    else:
        get_meetings = db.api.course.liveMeeting.list_live_meeting_by_page(page_index, settings.PAGE_SIZE)
        if get_meetings.is_error():
            return render(request, "404.html", {})
    meetings = get_meetings.result()["result"]
    if meetings:
        for meet in meetings:
            meet['status'] = STATUS[int(meet['status'])]
    c = {"meetings": meetings, 'keyword': keyword,
         "page": {"page_index": page_index, "rows_count": get_meetings.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": get_meetings.result()["page_count"]}}
    return render(request, "mz_course/liveMeeting/liveMeeting_list.html", c)


@dec_login_required
@handle_http_response_exception(501)
def liveMeeting_show(request):
    _id = get_param_by_request(request.GET, 'id', 0, int)
    class_id = get_param_by_request(request.GET, 'class_id', 0, int)
    video = []
    get_meeting = db.api.course.liveMeeting.get_live_meeting_by_id(_id, class_id)
    if get_meeting.is_error():
        log.warn("get meeting by id failed. id=%s" % _id)
        return render(request, "404.html",{})
    meeting = get_meeting.result()
    if meeting:
        meeting['status'] = STATUS[int(meeting['status'])]
        live_id = meeting.get('live_id')
        if live_id:
            get_video = db.api.course.liveMeeting.get_video_by_live_id(live_id)
            if get_video.is_error():
                log.warn("get video by live_id failed.")
                return render(request, '404.html')
            video = get_video.result()
    return render(request, "mz_course/liveMeeting/liveMeeting_show.html", {"meeting": meeting, "video": video})
