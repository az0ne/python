# -*- coding:utf-8 -*-

from utils.decorators import dec_login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from db.api.wiki import wiki_chapter as api_wiki_chapter
from db.api.wiki import wiki_course as api_wiki_course
from utils import tool
from utils.handle_exception import handle_http_response_exception


@dec_login_required
@handle_http_response_exception(501)
def wikiChapter_save(request):
    name = tool.get_param_by_request(request.POST, 'name', '', str)
    course_id = tool.get_param_by_request(request.POST, 'course_id', 0, int)
    index = tool.get_param_by_request(request.POST, 'index', 999, int)
    action = tool.get_param_by_request(request.POST, 'action', "add", str)
    video_course_id = tool.get_param_by_request(request.POST, 'video_course_id', 0, int)
    wikiChapter_dict = {'name': name, 'course_id': course_id, 'index': index, 'video_course_id': video_course_id}
    if action == 'add':
        insert_wikiChapter = api_wiki_chapter.insert_wiki_chapter(wikiChapter_dict)
        if insert_wikiChapter.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    elif action == 'edit':
        _id = tool.get_param_by_request(request.POST, 'id', 0, int)
        wikiChapter_dict['id'] = _id
        update_wikiChapter = api_wiki_chapter.update_wiki_chapter(wikiChapter_dict)
        if update_wikiChapter.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect("/wiki/wikiCourse/wikiItem_list/?action=query&course_id=" + str(course_id))


@dec_login_required
@handle_http_response_exception(501)
def wikiChapter_edit(request):
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    course_id = tool.get_param_by_request(request.GET, 'course_id', 0, int)
    chapters = api_wiki_chapter.get_wiki_chapters_by_course(course_id).result()
    wikiCourse = api_wiki_course.get_wiki_course_by_id(course_id).result()[0]
    wikiChapter = None
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        wikiChapter = api_wiki_chapter.get_wiki_chapter_by_id(_id)
        if wikiChapter.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        wikiChapter = wikiChapter.result()[0]
    data = {"chapters": chapters, 'course': wikiCourse, 'wikiChapter': wikiChapter, "action": action}
    return render_to_response("mz_wiki/wikiChapter_add.html", data, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def wikiChapter_list(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    course_id = tool.get_param_by_request(request.GET, 'course_id', 0, int)
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        del_wikiChapter = api_wiki_chapter.delete_wiki_chapter(_id)
        if del_wikiChapter.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        return HttpResponseRedirect('/wiki/wikiCourse/wikiItem_list/?action=query&course_id=' + str(course_id))
    else:
        wikiCourse = api_wiki_course.get_wiki_course_by_id(course_id)
        wikiChapter = api_wiki_chapter.get_wiki_chapters_by_course(course_id)
        if wikiChapter.is_error() or wikiCourse.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        ret_wikiChapter = wikiChapter.result()
        ret_course = wikiCourse.result()[0]
    c = {'chapters': ret_wikiChapter, 'course': ret_course}
    return render_to_response("mz_wiki/wikiChapter_list.html", c, context_instance=RequestContext(request))
