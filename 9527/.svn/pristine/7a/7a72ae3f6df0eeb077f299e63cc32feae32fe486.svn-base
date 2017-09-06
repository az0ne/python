# -*- coding:utf-8 -*-
from utils.decorators import dec_login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from db.api.course import homepagecourse_list as api_homepagecourse
from utils import tool
from utils.handle_exception import handle_http_response_exception


HOT_CAREER_DICT = {10: "UI设计", 20: "Web 前端开发", 30: "Python Web 开发", 40: "产品经理", 50: "互联网运营"}


@dec_login_required
@handle_http_response_exception(501)
def homepagecourse_list(request):
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)
    type = tool.get_param_by_request(request.GET, 'type', 0, int)

    if type and key_word:
        if key_word == "%":
            key_word1 = '//'+key_word
        else:
            key_word1 = key_word
        homepagecourse = api_homepagecourse.get_homepagecourse_by_type('%' + key_word1 + '%', type, page_index, settings.PAGE_SIZE)
    elif type:
        homepagecourse = api_homepagecourse.get_homepagecourse_by_onlytype(type, page_index, settings.PAGE_SIZE)
    elif key_word:
        if key_word == "%":
            key_word1 = '//' + key_word
        else:
            key_word1 = key_word
        homepagecourse = api_homepagecourse.get_homepagecourse_by_keyword('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)
    else:
        homepagecourse = api_homepagecourse.get_homepagecourse_by_page(page_index, settings.PAGE_SIZE)
    if homepagecourse.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))

    for homepage_course in homepagecourse.result()["result"]:
        homepage_course["careername"] = HOT_CAREER_DICT.get(homepage_course["careerid"])

    c = {"homepagecourses": homepagecourse.result()["result"],
         "keyword": key_word,
         "type": type,
         "page": {"page_index": page_index, "rows_count": homepagecourse.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": homepagecourse.result()["page_count"]}}
    return render_to_response("mz_course/mz_homepagecourse_list.html", c, context_instance=RequestContext(request))




@dec_login_required
@handle_http_response_exception(501)
def homepagecourse_save(request):
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    type = tool.get_param_by_request(request.POST, 'type', 0, int)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, str)
    index = tool.get_param_by_request(request.POST, 'index', "", str)
    career_id = tool.get_param_by_request(request.POST, 'career_id', "", str)
    course_id = tool.get_param_by_request(request.POST, 'courseid', 0, int)
    key_word = tool.get_param_by_request(request.POST, 'keyword', "", str)
    # confirm = api_homepagecourse.infocon(career_id, course_id)
    # if confirm.is_error():
    #     return render_to_response("404.html", {}, context_instance=RequestContext(request))
    # confirm = confirm.result()
    # if confirm:01
    homepagecourse = api_homepagecourse.updatehomepagecourse( _id, course_id)
    if homepagecourse.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect('/course/homepagecourse/list/?keyword=%s&type=%s&page_index=%s' % (key_word, type, page_index))
    # else:
    #     homepagecourse = api_homepagecourse.get_homepagecourse_by_id(_id)
    #     if homepagecourse.is_error():
    #         return render_to_response("404.html", {}, context_instance=                                                      (request))
    #     homepagecourse = homepagecourse.result()[0]
    #     error = '课程名称与分类不匹配！'
    #     c = {"homepagecourses": homepagecourse, "page_index": page_index, "keyword": key_word, "id": _id,"error": error}
    #     return render_to_response("mz_course/mz_homepagecourse_edit.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def homepagecourse_edit(request):
    page_index = tool.get_param_by_request(request.GET, 'page_index', "1", int)
    _id = tool.get_param_by_request(request.GET, 'id', "0", int)
    keyword = tool.get_param_by_request(request.GET, 'keyword', "", str)
    type = tool.get_param_by_request(request.GET, 'type', 0, int)
    homepagecourse = api_homepagecourse.get_homepagecourse_by_id(_id)
    if homepagecourse.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    homepagecourse = homepagecourse.result()[0]
    homepagecourse["careername"] = HOT_CAREER_DICT.get(homepagecourse["careerid"])
    c = {"homepagecourses": homepagecourse, "page_index":page_index, "keyword": keyword, "id": _id, "type": type}
    return render_to_response("mz_course/mz_homepagecourse_edit.html", c, context_instance=RequestContext(request))


