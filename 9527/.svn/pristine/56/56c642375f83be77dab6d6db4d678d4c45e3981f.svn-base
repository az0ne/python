# -*- coding:utf-8 -*-
import datetime
import db.api.course.course
from utils.decorators import dec_login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from db.api.wiki import wiki_course as api_wiki_course
from db.api.wiki import wiki_course_type as api_wiki_type
from db.api.seo import objSEO as api_seo
from db.api.wiki import wiki_item as api_wiki_item
from utils import tool
from utils.logger import logger as log
from utils.handle_exception import handle_http_response_exception, handle_ajax_response_exception


@dec_login_required
@handle_http_response_exception(501)
def wikiCourse_save(request):
    name = tool.get_param_by_request(request.POST, 'name', '', str)
    short_name = tool.get_param_by_request(request.POST, 'short_name', '', str)
    type_id = tool.get_param_by_request(request.POST, 'wikiCourseType', 0, int)
    course_id = tool.get_param_by_request(request.POST, 'course_id', 0, int)
    action = tool.get_param_by_request(request.POST, 'action', "add", str)
    index = tool.get_param_by_request(request.POST, 'index', 999, int)
    img_title = tool.get_param_by_request(request.POST, 'img_title', '', str)
    img_url = request.FILES.get('img_url', '')
    old_img = tool.get_param_by_request(request.POST, 'old_image', '', str)
    is_homepage = tool.get_param_by_request(request.POST, 'is_homepage', 0, int)
    info = tool.get_param_by_request(request.POST, 'info', '', str)
    recommend_course_id1 = request.POST.get('recommend_course_id1')
    recommend_course_id2 = request.POST.get('recommend_course_id2')
    recommend_course_id3 = request.POST.get('recommend_course_id3')
    recommend_course_id4 = request.POST.get('recommend_course_id4')
    image_path = old_img
    if img_url:
        image_path = tool.upload(img_url, settings.UPLOAD_IMG_PATH)
    wikiCourse_dict = {'name': name, 'short_name': short_name, 'type_id': type_id, 'course_id': course_id,
                       'index': index, 'img_title': img_title, 'img_url': image_path, 'is_homepage': is_homepage,
                       'info': info,
                       'recommend_course_id1': recommend_course_id1, 'recommend_course_id2': recommend_course_id2,
                       'recommend_course_id3': recommend_course_id3, 'recommend_course_id4': recommend_course_id4}

    if action == 'add':
        insert_wikiCourse = api_wiki_course.insert_wiki_course(wikiCourse_dict)
        if insert_wikiCourse.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

    elif action == 'edit':
        _id = tool.get_param_by_request(request.POST, 'id', 0, int)
        wikiCourse_dict['id'] = _id
        wikiCourse = api_wiki_course.update_wiki_course(wikiCourse_dict)
        if wikiCourse.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect("/wiki/wikiCourse/list/?action=query")


@dec_login_required
@handle_http_response_exception(501)
def wikiCourse_edit(request):
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    wikiCourse = None
    seo = {}
    wikiTypes = api_wiki_type.list_wiki_course_type().result()
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        wikiCourse = api_wiki_course.get_wiki_course_by_id(_id)
        if wikiCourse.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        wikiCourse = wikiCourse.result()[0]
        seo_ret = api_seo.get_objSEO_by_obj('WIKICOURSE', _id)
        if len(seo_ret.result()) > 0:
            seo = seo_ret.result()[0]

    active_courses = db.api.course.course.get_active_courses()
    if active_courses.is_error():
        log.warn('get active courses faild.')
        active_courses = []
    else:
        active_courses = active_courses.result()

    c = {
        "types": wikiTypes, 'course': wikiCourse, "action": action,
        'seo': seo, 'active_courses': active_courses
    }
    return render_to_response("mz_wiki/wikiCourse_add.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def wikiCourse_list(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        ret_items = api_wiki_item.get_wiki_item_by_course(_id).result()
        if len(ret_items) > 0:
            for item in ret_items:
                item_seo_count = api_seo.count_have_obj_seo(item['id'], "WIKIITEM")
                if item_seo_count > 0:
                    api_seo.delete_objSEO_by_obj(item['id'], "WIKIITEM")
        course_seo_count = api_seo.count_have_obj_seo(_id, "WIKICOURSE")
        if course_seo_count > 0:
            api_seo.delete_objSEO_by_obj(_id, "WIKICOURSE")
        wikiCourse = api_wiki_course.delete_wiki_course(_id)
        if wikiCourse.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        return HttpResponseRedirect('/wiki/wikiCourse/list/?action=query')
    else:
        wikiCourse = api_wiki_course.list_wiki_course()
        if wikiCourse.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        wikiCourse_ret = wikiCourse.result()
        wikiType_ret = api_wiki_type.list_wiki_course_type().result()
        ret_list = []
        for type in wikiType_ret:
            dict = {'type': {}, 'course': []}
            dict['type'] = type['name']
            for course in wikiCourse_ret:
                if course['type_id'] == type['id']:
                    dict['course'].append(course)
            ret_list.append(dict)
        c = {"result": ret_list}
        return render_to_response("mz_wiki/wikiCourse_list.html", c, context_instance=RequestContext(request))


@handle_ajax_response_exception
def wikiCourse_isHaveTheShortName(request):
    short_name = tool.get_param_by_request(request.GET, 'short_name', '', str)
    is_have = False
    count = api_wiki_course.count_have_the_wikiCourse_short_name(short_name).result()
    if count > 0:
        is_have = True
    result = {'is_have': is_have}
    return result
