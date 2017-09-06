# -*- coding:utf-8 -*-

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect

import db.api.course.careerPublicMeetingDate
from utils import tool
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.logger import logger as log

CURRENT_URL = ''

@dec_login_required
@handle_http_response_exception(501)
def career_public_meeting_date_list(request):
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    career_id = tool.get_param_by_request(request.GET, 'career_id', 0, int)
    _id = tool.get_param_by_request(request.GET, 'id', 0, int)

    if action != 'del':
        global CURRENT_URL
        CURRENT_URL = request.get_full_path()

    if action == 'query':
        result = db.api.course.careerPublicMeetingDate.list_career_public_meeting_date_by_page(page_index,
                                                                                               settings.PAGE_SIZE)
        if result.is_error():
            log.warn("get career public meeting date by page failed!")
            return render(request, '404.html', {"error": "query error"})

    if action == 'search':
        if career_id == 0:
            result = db.api.course.careerPublicMeetingDate.list_career_public_meeting_date_by_page(page_index,
                                                                                                   settings.PAGE_SIZE)

            if result.is_error():
                log.warn("get career public meeting date by page failed!")
                return render(request, '404.html', {"error": "search error"})
        else:
            result = db.api.course.careerPublicMeetingDate.list_career_public_meeting_date_by_career_id(career_id,
                                                                                                        page_index,
                                                                                                        settings.PAGE_SIZE)
            if result.is_error():
                log.warn("get career public meeting date by career id failed!"
                         "career_id: {0}".format(career_id)
                         )
                return render(request, '404.html', {"error": "search error"})

    if action == 'del':
        result = db.api.course.careerPublicMeetingDate.delete_career_public_meeting_date_by_id(_id)
        if result.is_error():
            log.warn("delete career public meeting date by career id failed!"
                     "career_public_meeting_date_id: {0}".format(_id))
            return render(request, '404.html', {"error": "delete error"})

        return HttpResponseRedirect(tool.get_correct_url(CURRENT_URL, reversed("mz_course:careerPMD_list")))

    data = {
        "result": result.result()['result'],
        "page": {"page_size": settings.PAGE_SIZE,
                 "page_index": page_index,
                 "rows_count": result.result()['rows_count'],
                 "page_count": result.result()['page_count'],
                 }, "career_id": career_id
    }

    return render(request, 'mz_course/careerPublicMeetingDate_list.html', data)
