#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from db.api.course import careerIntroduceDuty as api_duty
from db.api.apiutils import APIResult
from utils.decorators import dec_login_required
from utils import tool
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def duty_list(request):
    """
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    career_id = tool.get_param_by_request(request.GET, 'careerId', 0, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)

    duty = APIResult()
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        duty = api_duty.delete_career_page_duty(_id)
        if duty.is_error():
            # 处理错误
            return render_to_response("html404.html", {}, context_instance=RequestContext(request))

        if not duty.result():
            return render_to_response("delete_error.html", {}, context_instance=RequestContext(request))

        else:
            return HttpResponseRedirect(
                '/course/careerIntroduce/edit/?action=show&id='+str(career_id))

    if duty.is_error():
        # 处理错误
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    c = {"duties": duty.result()["result"],
         "key_word": key_word}

    return render_to_response("mz_course/careerIntroduce/careerIntroduce_show.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def duty_edit(request):
    """
    get one data by id from mysql,
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    career_id = tool.get_param_by_request(request.GET, 'careerId', 0, int)

    duty = APIResult()
    c = None
    if action == "add":
        c = {"career_id": career_id, "action": action}
        return render_to_response("mz_course/careerIntroduce/careerIntroduce_duty_edit.html", c,
                                  context_instance=RequestContext(request))

    if action == "edit" and (not career_id):
        _id = tool.get_param_by_request(request.GET, 'dutyId', 0, int)
        duty = api_duty.get_career_page_duty_by_id(_id)
        c = {"duties": duty.result()[0], "action": action}
        if duty.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        else:
            return render_to_response("mz_course/careerIntroduce/careerIntroduce_duty_edit.html", c,
                                      context_instance=RequestContext(request))

    if action == "edit" and career_id:
        duty = api_duty.list_career_page_duty_by_career_id(career_id)
        c = {"duties": duty.result(), "action": action}

        if duty.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        else:
            return render_to_response("mz_course/careerIntroduce/careerIntroduce_duty_list.html", c,
                                      context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def duty_save(request):
    """
    save data to mysql database,from update and add
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.POST, 'action', 'add', str)
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    career_id = tool.get_param_by_request(request.POST, 'career_id', 1, int)
    name = tool.get_param_by_request(request.POST, 'name', "", str)
    enterprise = tool.get_param_by_request(request.POST, 'enterprise', "", str)

    duty = APIResult()
    if action == "add":
        duty = api_duty.insert_career_page_duty(name, enterprise, career_id)
    elif action == "edit":
        duty = api_duty.update_career_page_duty(_id, name, enterprise, career_id)

    if duty.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    return HttpResponseRedirect('/course/careerIntroduce/edit/?action=show&id='+str(career_id))
