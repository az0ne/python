#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from db.api.course import careerIntroduceEnterprise as api_enterprise
from db.api.apiutils import APIResult
from utils.decorators import dec_login_required
from utils import tool
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def enterprise_list(request):
    """
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    career_id = tool.get_param_by_request(request.GET, 'careerId', 0, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)

    enterprise = APIResult()
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        enterprise = api_enterprise.delete_career_page_enterprise(_id)
        if enterprise.is_error():
            # 处理错误
            return render_to_response("html404.html", {}, context_instance=RequestContext(request))

        if not enterprise.result():
            return render_to_response("delete_error.html", {}, context_instance=RequestContext(request))

        else:
            return HttpResponseRedirect(
                '/course/careerIntroduce/edit/?action=show&id='+str(career_id))

    if enterprise.is_error():
        # 处理错误
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    c = {"enterprises": enterprise.result()["result"],
         "key_word": key_word}

    return render_to_response("mz_course/careerIntroduce/careerIntroduce_show.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def enterprise_edit(request):
    """
    get one data by id from mysql,
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    career_id = tool.get_param_by_request(request.GET, 'careerId', 0, int)

    enterprise = APIResult()
    c = None
    if action == "add":
        c = {"career_id": career_id, "action": action}
        return render_to_response("mz_course/careerIntroduce/careerIntroduce_enterprise_edit.html", c,
                                  context_instance=RequestContext(request))

    if action == "edit" and (not career_id):
        _id = tool.get_param_by_request(request.GET, 'enterpriseId', 0, int)
        enterprise = api_enterprise.get_career_page_enterprise_by_id(_id)
        c = {"enterprises": enterprise.result()[0], "action": action}
        if enterprise.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        else:
            return render_to_response("mz_course/careerIntroduce/careerIntroduce_enterprise_edit.html", c,
                                      context_instance=RequestContext(request))

    if action == "edit" and career_id:
        enterprise = api_enterprise.list_career_page_enterprise_by_career_id(career_id)
        c = {"enterprises": enterprise.result(), "action": action}

        if enterprise.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        else:
            return render_to_response("mz_course/careerIntroduce/careerIntroduce_enterprise_list.html", c,
                                      context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def enterprise_save(request):
    """
    save data to mysql database,from update and add
    :param request:
    :return:
    """
    action = tool.get_param_by_request(request.POST, 'action', 'add', str)
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    career_id = tool.get_param_by_request(request.POST, 'career_id', 0, int)
    img_title = tool.get_param_by_request(request.POST, 'img_title', '', str)
    img_url = request.FILES.get('img_url', "")
    old_image_path = tool.get_param_by_request(request.POST, 'old_image_path', "", str)

    image_path = old_image_path  # 如果更新数据时，未更改图片，image_url为空，设置图片的路径为老路径
    if img_url:
        image_path = tool.upload(img_url, settings.UPLOAD_IMG_PATH)

    enterprise = APIResult()
    if action == "add":
        enterprise = api_enterprise.insert_career_page_enterprise(image_path, img_title, career_id)
    elif action == "edit":
        enterprise = api_enterprise.update_career_page_enterprise(_id, image_path, img_title, career_id)

    if enterprise.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    return HttpResponseRedirect('/course/careerIntroduce/edit/?action=show&id='+str(career_id))
