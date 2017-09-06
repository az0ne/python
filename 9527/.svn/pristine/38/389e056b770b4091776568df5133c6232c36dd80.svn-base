# -*- coding:utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
from mz_lps4.teacher_evaluation.interface import *
from django.core.urlresolvers import reverse
import db.api.lps4.teacher_evaluation.warning_time


@dec_login_required
@handle_http_response_exception(501)
def warning_time_list(request):
    APIResult = db.api.lps4.teacher_evaluation.warning_time.get_all_warning_time()
    if APIResult.is_error():
        log.warn("get all waring time from api failed.")
        return render(request, "404.html")
    result = APIResult.result()
    data = dict(result=result)
    return render(request, "mz_lps4/teacher_evaluation/warning_time_list.html", data)


@dec_login_required
@handle_http_response_exception(501)
def warning_time_edit(request):
    action = get_param_by_request(request.GET, "action", "add", str)
    if "edit" in action:
        try:
            _id = get_param_by_request(request.GET, "warn_id", 0, int)
            result = get_warning_time(_id)
        except Http404:
            return render(request, "404.html")
    else:
        result = dict()
    data = dict(result=result, action=action)
    return render(request, "mz_lps4/teacher_evaluation/warnning_time_edit.html", data)


@dec_login_required
@handle_http_response_exception(501)
def warning_time_delete(request):
    _id = get_param_by_request(request.GET, "warning_id", 0, int)
    try:
        delete_warning_time(_id)
    except Http404:
        return render(request, "404.html", dict(message="delete warning time failed."))
    return HttpResponseRedirect(reverse('mz_lps4:warningTimeList'))


@dec_login_required
@handle_http_response_exception(501)
def warning_time_save(request):
    action = get_param_by_request(request.POST, "action", "", str)
    type = get_param_by_request(request.POST, "warn_type", 0, int)
    title = get_param_by_request(request.POST, "title", "", str)
    warn_one_hour = get_param_by_request(request.POST, "warn_one_hour", 0, float)
    warn_two_hour = get_param_by_request(request.POST, "warn_two_hour", 0, float)
    warn_three_hour = get_param_by_request(request.POST, "warn_three_hour", 0, float)
    warn_dict = dict(title=title, type=type, warn_one_hour=warn_one_hour,
                     warn_two_hour=warn_two_hour, warn_three_hour=warn_three_hour)
    if "add" in action:
        try:
            warn_dict = dict(title=title, type=type, warn_one_hour=warn_one_hour,
                             warn_two_hour=warn_two_hour, warn_three_hour=warn_three_hour)
            insert_warning_time(warn_dict)
        except Http404:
            return render(request, "404.html", dict(message="add warning time failed."))
    elif "edit" in action:
        _id = get_param_by_request(request.POST, "warn_id", 0, int)
        warn_dict.update(dict(id=_id))
        try:
            update_warning_time(warn_dict=warn_dict)
        except Http404:
            return render(request, "404.html", dict(message="update warning time failed."))
    return HttpResponseRedirect(reverse('mz_lps4:warningTimeList'))
