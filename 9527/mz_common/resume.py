#! /usr/bin/evn python
# -*- coding:utf-8 -*-
import json
from django.http import HttpResponse, JsonResponse

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
from db.api.common.resume import get_user_info, list_user_edu, list_user_work
from utils.logger import logger as log
from django.shortcuts import render
from mz_common.resume_interface import get_age_by_birthday, get_work_years, get_resume_info_by_user_id, \
    write_resume_to_docx
import db.api.common.resume
from django.conf import settings


@dec_login_required
@handle_http_response_exception(501)
def resume_show(request):
    username = get_param_by_request(request.GET, "user_id", 0, int)
    if username:

        # 个人信息
        APIResult = get_user_info(username)

        if APIResult.is_error():
            log.warn("get_user_info is error")
            return render(request, "404.html", dict(message=u"get_user_info is error"))
        user_info = APIResult.result()
        user_id = user_info["user_id"] if user_info else 0
        if user_info:
            # 计算年龄
            user_info["age"] = get_age_by_birthday(user_info["birthday"])
            # 计算工作年限
            try:
                user_info["work_years"] = get_work_years(user_info.get("start_work_time", 0))
            except TypeError as e:
                log.warn("user_info['start_work_time'] is None. error:%s" % e)
                user_info["work_years"] = 0

        if user_id:

            # 工作经历
            APIResult = list_user_work(user_id)
            if APIResult.is_error():
                log.warn("list_user_word is error.")
                return render(request, "404.html", dict(message=u"list_user_word is error."))
            user_works = APIResult.result()

            # 教育背景
            APIResult = list_user_edu(user_id)
            if APIResult.is_error():
                log.warn("list_user_edu is error.")
                return render(request, "404.html", dict(message=u"list_user_edu is error."))
            user_edus = APIResult.result()

            return render(request, "mz_common/resume.html", dict(user_info=user_info,
                                                                 user_edus=user_edus,
                                                                 user_works=user_works,
                                                                 username=username))
        return render(request, "mz_common/resume.html", dict(username=username,
                                                             msg=u'未查到该用户的相关简历信息，请确认用户名是否正确。'))
    return render(request, "mz_common/resume.html")


@dec_login_required
@handle_http_response_exception(501)
def resume_list(request):
    page_index = get_param_by_request(request.GET, "page_index", 1, int)
    action = get_param_by_request(request.GET, "action", "query", str)
    keyword = get_param_by_request(request.GET, "keyword", "", str)
    if "search" in action:
        APIResult = db.api.common.resume.list_resume_info_by_search("%" + keyword + "%", page_index)
    else:
        APIResult = db.api.common.resume.list_resume_info(page_index)
    if APIResult.is_error():
        log.warn("list all resume info failed. ")
        return render(request, "404.html")
    result = APIResult.result()
    c = {"resumes": result["result"], "keyword": keyword,
         "page": {"page_index": page_index, "rows_count": result["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": result["page_count"]}}

    return render(request, "mz_common/resume_list.html", c)


@dec_login_required
@handle_http_response_exception(501)
def resume_to_docx(request):
    user_id = get_param_by_request(request.GET, "user_id", 0, int)
    if user_id:
        user_info, user_edus, user_works = get_resume_info_by_user_id(request, user_id)
        response = write_resume_to_docx(user_info, user_edus, user_works)
        return response
