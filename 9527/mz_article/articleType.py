# -*- coding:utf-8 -*-

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import JsonResponse
from django.core.urlresolvers import reverse

from utils.decorators import dec_login_required, dec_login_validate
from django.conf import settings
from db.api.article import article_type as api_articleType
from utils import tool
from utils.logger import logger as log
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def articleType_save(request):
    """
    保存文章类型
    :param request:
    :return:重定向到list页面
    """
    action = tool.get_param_by_request(request.POST, 'action', "add", str)
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    name = tool.get_param_by_request(request.POST, 'name', '', str)
    homepage_img = request.FILES.get('homepage_img', '')
    old_image_path = tool.get_param_by_request(request.POST, 'old_image_path', '', str)
    short_name = tool.get_param_by_request(request.POST, 'short_name', '', str)
    index = tool.get_param_by_request(request.POST, 'index', 0, int)

    image_path = old_image_path
    if homepage_img:
        image_path = tool.upload(homepage_img, settings.ARTICLE_IMG_UPLOAD_PATH)
    if action == 'add':
        article_type = api_articleType.insert_articleType(_id, name, short_name, image_path, index)
        if article_type.is_error():
            return render_to_response("404.html", {}, RequestContext(request))

    elif action == 'edit':
        article_type = api_articleType.update_articleType(_id, name, short_name, image_path, index)
        if article_type.is_error():
            return render_to_response("404.html", {}, RequestContext(request))
    return HttpResponseRedirect(reverse("mz_article:articleType_list"))


@dec_login_required
@handle_http_response_exception(501)
def articleType_isHomepage_save(request):
    """
    修改is_homepage字段的值
    :param request:
    :return:true/false
    """
    _id = tool.get_param_by_request(request.GET, 'id', 0, int)
    is_homepage = tool.get_param_by_request(request.GET, 'is_homepage', '', str)

    article_type = api_articleType.update_articleType_isHomepage(_id, is_homepage)
    if article_type.is_error():
        result = ''
    else:
        result = article_type.result()

    result = {"result": result}
    return JsonResponse(result)


@dec_login_required
@handle_http_response_exception(501)
def articleType_isVisible_save(request):
    """
    修改is_visible字段的值
    :param request:
    :return:true/false
    """
    _id = tool.get_param_by_request(request.GET, 'id', 0, int)
    is_visible = tool.get_param_by_request(request.GET, 'is_visible', '', str)

    article_type = api_articleType.update_articleType_isVisible(_id, is_visible)
    if article_type.is_error():
        result = ''
    else:
        result = article_type.result()

    result = {"result": result}
    return JsonResponse(result)


@dec_login_required
@handle_http_response_exception(501)
def articleType_isCareer_save(request):
    """
    修改is_career字段的值
    :param request:
    :return:true/false
    """
    _id = tool.get_param_by_request(request.GET, 'id', 0, int)
    is_career = tool.get_param_by_request(request.GET, 'is_career', '', str)

    article_type = api_articleType.update_articleType_isCareer(_id, is_career)
    if article_type.is_error():
        result = ''
    else:
        result = article_type.result()

    result = {"result": result}
    return JsonResponse(result)


@dec_login_required
@handle_http_response_exception(501)
def articleType_edit(request):
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    article_type = None
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        article_type = api_articleType.get_articletype_by_id(_id)
        if article_type.is_error():
            return render_to_response("404.html", {}, RequestContext(request))
        article_type = article_type.result()[0]

    c = {"articleType": article_type, "action": action}
    return render_to_response("mz_article/articleType_edit.html", c, RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def articleType_list(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)

    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        article_type = api_articleType.delete_articleType_by_id(_id)
        if article_type.is_error():
            return render_to_response("404.html", {}, RequestContext(request))

    if action == "search":
        article_type = api_articleType.list_articletype_by_name('%' + key_word + '%')

    else:
        article_type = api_articleType.list_articleType()

    if article_type.is_error():
        return render_to_response("404.html", {}, RequestContext(request))

    c = {"articleTypes": article_type.result(), "key_word": key_word}

    return render_to_response("mz_article/articleType_list.html", c, RequestContext(request))

