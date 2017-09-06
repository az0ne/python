# -*- coding:utf-8 -*-

from utils.decorators import dec_login_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from db.api.course import course_seo as api_courseinfo
from utils import tool
from utils.handle_exception import handle_http_response_exception
from django.http import HttpResponseRedirect





@dec_login_required
@handle_http_response_exception(501)
def courseinfo_list(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)
    if key_word:
        if key_word == "%":
            key_word1 = '//' + key_word
        else:
            key_word1 = key_word
        courseinfo = api_courseinfo.get_course_by_title('%' + key_word1 + '%', page_index, settings.PAGE_SIZE)
        if courseinfo.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    else:
        courseinfo = api_courseinfo.list_course_by_page(page_index, settings.PAGE_SIZE)
        if courseinfo.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    c = {"courseinfos": courseinfo.result()["result"],
         "coursename": key_word,
         "page": {"page_index": page_index, "rows_count": courseinfo.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": courseinfo.result()["page_count"]}
         }
    return render_to_response("mz_course/course_tdk/course_seo_list.html", c, context_instance=RequestContext(request))


# @dec_login_required
# @handle_http_response_exception(501)
# def courseinfo_info(request):
#     index = tool.get_param_by_request(request.GET, 'coursename', "", str)
#     page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
#     index_joint = '%'+index+'%'
#     courseinfo = api_courseinfo.query_coursedetail(index_joint, page_index, settings.PAGE_SIZE)
#     if courseinfo.is_error():
#         return render_to_response("404.html", {}, context_instance=RequestContext(request))
#     print courseinfo.result()["result"]
#     c = {"courseinfos": courseinfo.result()["result"],
#          "coursename": index,
#          "page": {"page_index": page_index, "rows_count": courseinfo.result()["rows_count"],
#                   "page_size": settings.PAGE_SIZE,
#                   "page_count": courseinfo.result()["page_count"]}
#          }
#     return render_to_response("mz_course/course_tdk/coursequery_result.html", c, context_instance=RequestContext(request))



@dec_login_required
@handle_http_response_exception(501)
def courseinfo_edit(request):
    _id = tool.get_param_by_request(request.GET, 'id', 1, int)
    keyword = tool.get_param_by_request(request.GET, 'keyword', "", str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    action = tool.get_param_by_request(request.GET, 'action', "", str)
    courseinfo = api_courseinfo.edit_course_by_id(_id)
    if courseinfo.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    c = {"courseinfos": courseinfo.result(), "page_index":page_index, "keyword": keyword, "id":_id, "action": action, }
    return  render_to_response("mz_course/course_tdk/course_seo_add.html", c, context_instance=RequestContext(request))




@dec_login_required
@handle_http_response_exception(501)
def courseinfo_save(request):
    _id = tool.get_param_by_request(request.POST, 'id', 1, int)
    iscreat = tool.get_param_by_request(request.POST, 'iscreat', 1, int)
    keyword = tool.get_param_by_request(request.POST, 'keyword', "", str)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)
    action = tool.get_param_by_request(request.POST, 'action', "", str)
    seotitle = tool.get_param_by_request(request.POST, 'seotitle', "", str)
    seokeyword = tool.get_param_by_request(request.POST, 'seokeyword', "", str)
    seodescription = tool.get_param_by_request(request.POST, 'seodescription', "", str)
    if iscreat:
        courseinfo = api_courseinfo.edit_course_conf(_id, seotitle, seokeyword, seodescription, )
    else:
        courseinfo = api_courseinfo.cteat_course_conf(_id, seotitle, seokeyword, seodescription, )
    if courseinfo.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect( '/course/courseinfo/list/?action=search&keyword=%s&page_index=%s' % (keyword, page_index))

