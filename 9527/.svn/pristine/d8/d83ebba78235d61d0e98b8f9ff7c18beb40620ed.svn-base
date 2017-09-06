# -*- coding:utf-8 -*-

from utils.decorators import dec_login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from db.api.lps import study_info as api_studyinfo
from utils import tool
from utils.handle_exception import handle_http_response_exception





@dec_login_required
@handle_http_response_exception(501)
def studyinfo_query(request):
    return render_to_response("mz_common/businessinfoquery.html", {}, context_instance=RequestContext(request))



@dec_login_required
@handle_http_response_exception(501)
def studyinfo_student(request):
    index = tool.get_param_by_request(request.GET, 'email', "", str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    studyinfo = api_studyinfo.query_emaildetail(index, page_index, settings.PAGE_SIZE)
    if studyinfo.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    c = {"studyinfos": studyinfo.result()["result"],
         "email": index,
         "page": {"page_index": page_index, "rows_count": studyinfo.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": studyinfo.result()["page_count"]}
         }
    return render_to_response("mz_common/businessquery_result.html", c, context_instance=RequestContext(request))



@dec_login_required
@handle_http_response_exception(501)
def studyinfo_studentinfo(request):
    _id = tool.get_param_by_request(request.GET, 'id', 1, int)
    date = tool.get_param_by_request(request.GET, 'date', "", str)
    username = tool.get_param_by_request(request.GET, 'username', str)
    studyinfo = api_studyinfo.query_datedetail(_id, date)
    if studyinfo.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    c = {"studyinfos": studyinfo.result(), "date": date, "username": username}
    return  render_to_response("mz_common/businessquery_detail.html", c, context_instance=RequestContext(request))



