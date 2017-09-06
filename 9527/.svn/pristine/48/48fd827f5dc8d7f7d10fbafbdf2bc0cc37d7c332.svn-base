# -*- coding:utf-8 -*-

from utils.decorators import dec_login_required

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from db.api.wiki import wiki_course_type as api_wiki_course_type
from db.api.wiki import wiki_course as api_wiki_course
from db.api.wiki import wiki_item as api_wiki_item
from db.api.seo import objSEO as api_objSEO
from utils import tool
from utils.handle_exception import handle_http_response_exception



@dec_login_required
@handle_http_response_exception(501)
def wiki_SEO_save(request):
    obj_id = tool.get_param_by_request(request.POST,'obj_id')
    obj_type = tool.get_param_by_request(request.POST,'obj_type')
    seo_title = tool.get_param_by_request(request.POST,'seo_title')
    seo_keywords = tool.get_param_by_request(request.POST,'seo_keywords')
    seo_description = tool.get_param_by_request(request.POST,'seo_description')
    # action = tool.get_param_by_request(request.POST, 'action', "edit")
    dict_obj={'obj_id':obj_id,'obj_type':obj_type,'seo_title':seo_title,'seo_keywords':seo_keywords,'seo_description':seo_description}
    get_ret = api_objSEO.get_objSEO_by_obj(obj_type,obj_id)
    if len(get_ret.result())>0:
        seo_ret = api_objSEO.update_objSEO_by_obj(dict_obj)
    else:
        seo_ret = api_objSEO.insert_obj_seo(obj_type,obj_id,seo_title,seo_keywords,seo_description)
    # seo的新增和删除在wiki新增和删除时同时操作，以下注销
    # del_seo = api_objSEO.delete_objSEO_by_obj_id()
    # insert_seo = api_objSEO.insert_obj_seo(obj_type,obj_id,seo_title,seo_keyword,seo_description)
    if seo_ret.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    if obj_type=='WIKIITEM':
        course_id = tool.get_param_by_request(request.POST,'course_id')
        URL = '/wiki/wikiCourse/wikiItem_list/?action=query&course_id='+str(course_id)
    elif obj_type == 'WIKICOURSE':
        URL = '/wiki/wikiCourse/list/?action=query'
    elif obj_type=='WIKICOURSETYPE':
        URL = '/wiki/wikiCourseType/list/?action=query'

    return HttpResponseRedirect(URL)


@dec_login_required
@handle_http_response_exception(501)
def wiki_SEO_edit(request):
    action = tool.get_param_by_request(request.GET,'action','edit')
    obj_id = tool.get_param_by_request(request.GET,'obj_id')
    obj_type = tool.get_param_by_request(request.GET,'obj_type')
    course_id = tool.get_param_by_request(request.GET,'course_id')
    seo = None
    if action =='edit' or action == 'show':
        if obj_type=='WIKICOURSETYPE':
            obj_ret = api_wiki_course_type.get_wikiCourseType_by_id(obj_id).result()[0]
        elif obj_type=='WIKICOURSE':
            obj_ret = api_wiki_course.get_wiki_course_by_id(obj_id).result()[0]
        else:
            obj_ret = api_wiki_item.get_wiki_item_by_id(obj_id).result()[0]
        obj = {'id':obj_ret['id'],'name':obj_ret['name']}
        wikiSEO = api_objSEO.get_objSEO_by_obj(obj_type,obj_id)
        if wikiSEO.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        if len(wikiSEO.result()) == 0:
            seo = {}
        else:
            seo=wikiSEO.result()[0]
    c={"wikiSEO":seo,'obj_type':obj_type,'obj':obj,"action": action,'course_id':course_id}
    return render_to_response("mz_wiki/wiki_seo_add.html", c, context_instance=RequestContext(request))