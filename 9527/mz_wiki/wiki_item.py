# -*- coding:utf-8 -*-
from utils.decorators import dec_login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from db.api.wiki import wiki_item as api_wiki_item
from db.api.wiki import wiki_course as api_wiki_course
from db.api.wiki import wiki_chapter as api_wiki_chapter
from db.api.seo import objSEO as api_seo
from utils import tool
from utils.handle_exception import handle_http_response_exception, handle_ajax_response_exception
from bs4 import BeautifulSoup

@dec_login_required
@handle_http_response_exception(501)
def wikiItem_save(request):
    course_id = tool.get_param_by_request(request.POST, 'course_id', 0, int)
    chapter_id = tool.get_param_by_request(request.POST, 'chapter', 0, int)
    name = tool.get_param_by_request(request.POST, 'name', '', str)
    short_name = tool.get_param_by_request(request.POST, 'short_name', '', str)
    index = tool.get_param_by_request(request.POST, 'index', 999, int)
    action = tool.get_param_by_request(request.POST, 'action', "add", str)
    wikiItem_dict = {'name': name, 'course_id': course_id, 'chapter_id': chapter_id, 'index': index,
                     'short_name': short_name}
    if action == 'add':
        wikiItem_dict['content'] = ""
        insert_wikiItem = api_wiki_item.insert_wiki_item(wikiItem_dict)
        if insert_wikiItem.is_error():
            return render(request, "404.html", {})
        _id = insert_wikiItem.result()

    elif action == 'edit':
        _id = tool.get_param_by_request(request.POST, 'item_id', 0, int)
        wikiItem_dict['id'] = _id
        update_wikiType = api_wiki_item.update_wiki_item(wikiItem_dict)
        if update_wikiType.is_error():
            return render(request, "404.html", {})
    return HttpResponseRedirect(
        "/wiki/wikiCourse/wikiItem_edit/?action=next&course_id=" + str(course_id) + "&id=" + str(_id))


@dec_login_required
@handle_http_response_exception(501)
def wikiItem_edit(request):
    action = tool.get_param_by_request(request.GET, 'action', "add", str)
    course_id = tool.get_param_by_request(request.GET, 'course_id', 0, int)
    items = api_wiki_item.get_wiki_item_by_course(course_id).result()
    wikiItem = None
    course = api_wiki_course.get_wiki_course_by_id(course_id).result()[0]
    chapters = api_wiki_chapter.get_wiki_chapters_by_course(course_id).result()
    seo = {}
    if action == "edit" or action == "show" or action == 'next':
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        wikiItem = api_wiki_item.get_wiki_item_by_id(_id)
        if wikiItem.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        if wikiItem:
            wikiItem = wikiItem.result()[0]
        seo_ret = api_seo.get_objSEO_by_obj('WIKIITEM', _id)
        if len(seo_ret.result()) > 0:
            seo = seo_ret.result()[0]
    c = {"item": wikiItem, 'course': course, 'chapters': chapters, 'items': items, "action": action, 'seo': seo}
    return render_to_response("mz_wiki/wikiItem_add.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def wikiItem_list(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    course_id = tool.get_param_by_request(request.GET, 'course_id', 0, int)
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        item_seo_count = api_seo.count_have_obj_seo(_id, "WIKIITEM")
        if item_seo_count > 0:
            api_seo.delete_objSEO_by_obj(_id, "WIKIITEM")

        wikiItem = api_wiki_item.delete_wiki_item(_id)
        if wikiItem.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        return HttpResponseRedirect('/wiki/wikiCourse/wikiItem_list/?action=query&course_id=' + str(course_id))
    else:
        course_id = tool.get_param_by_request(request.GET, 'course_id', 0, int)
        course = api_wiki_course.get_wiki_course_by_id(course_id)
        wikiChapter = api_wiki_chapter.get_wiki_chapters_by_course(course_id)
        wikiItems = api_wiki_item.get_wiki_item_by_course(course_id)
        if wikiChapter.is_error() or wikiItems.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

        ret_list = []
        for chapter in wikiChapter.result():
            dict = {'chapter': {}, 'items': []}
            dict['chapter'] = {'name': chapter['name'], 'id': chapter['id']}
            for item in wikiItems.result():
                if item['chapter_id'] == chapter['id']:
                    dict['items'].append(item)
            ret_list.append(dict)
        c = {"result": ret_list, 'course': course.result()[0]}
        return render_to_response("mz_wiki/wikiItem_list.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def wikiItem_content_save(request):
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    course_id = tool.get_param_by_request(request.POST, 'course_id', 0, int)
    content = tool.get_param_by_request(request.POST, 'content', '', str)
    retrieval = BeautifulSoup(content, "html.parser").get_text()

    updateContent = api_wiki_item.update_wiki_item_content(_id, content, retrieval)
    if updateContent.is_error():
        return render(request, "404.html", {})
    return HttpResponseRedirect("/wiki/wikiCourse/wikiItem_list/?action=query&course_id=" + str(course_id))


@handle_ajax_response_exception
def wikiItem_isHaveTheShortName(request):
    short_name = tool.get_param_by_request(request.GET, 'short_name', '', str)
    course_id = tool.get_param_by_request(request.GET, 'course_id', 0, int)
    is_have = False
    count = api_wiki_item.count_have_the_wikiItem_short_name(short_name, course_id).result()
    if count > 0:
        is_have = True
    result = {'is_have': is_have}
    return result
