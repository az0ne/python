# -*- coding:utf-8 -*-
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
import db.api.common.app_consult_info_stream
from utils.logger import logger as log


@dec_login_required
@handle_http_response_exception(501)
def app_consult_info_list(request):
    page_index = get_param_by_request(request.GET, "page_index", 1, int)
    action = get_param_by_request(request.GET, "action", "query", str)
    keyword = get_param_by_request(request.GET, "keyword", "", str)
    if "search" in action:
        APIResult = db.api.common.app_consult_info_stream.select_app_consult_info_stream_by_search("%" + keyword + "%",
                                                                                                   page_index,
                                                                                                   settings.PAGE_SIZE)
    else:
        APIResult = db.api.common.app_consult_info_stream.select_app_consult_info_stream_by_page(page_index,
                                                                                                 settings.PAGE_SIZE)
    if APIResult.is_error():
        log.warn("list all consult  info failed. ")
        return render(request, "404.html")
    result = APIResult.result()
    c = {"consult_info": result["result"], "keyword": keyword,
         "page": {"page_index": page_index, "rows_count": result["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": result["page_count"]}}

    return render(request, "mz_common/appConsultInfoStream.html", c)


@dec_login_required
@handle_http_response_exception(501)
def app_consult_info_del(request):
    info_id = get_param_by_request(request.GET, "id", 0, int)
    if info_id:
        APIResult = db.api.common.app_consult_info_stream.del_app_consult_info_stream_by_id(info_id)
        if APIResult.is_error():
            return render(request, '404.html')
    return HttpResponseRedirect(reverse('mz_common:app_consult_info_list'))
