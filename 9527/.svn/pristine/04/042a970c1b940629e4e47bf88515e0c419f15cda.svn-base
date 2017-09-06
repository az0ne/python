# -*- coding:utf-8 -*-

from utils.decorators import dec_login_required
from django.conf import settings
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from db.api.wiki import wiki_course_type as api_wiki_course_type
from db.api.seo import objSEO as api_objSEO
from db.api.wiki import wiki_course as api_wiki_course
from db.api.wiki import wiki_item as api_wiki_item
from utils import tool
from utils.handle_exception import handle_http_response_exception,handle_ajax_response_exception


@dec_login_required
@handle_http_response_exception(501)
def wikiCourseType_save(request):

    name = tool.get_param_by_request(request.POST,'name')
    short_name =  tool.get_param_by_request(request.POST,'short_name')
    action = tool.get_param_by_request(request.POST, 'action', "add")
    index = tool.get_param_by_request(request.POST, 'index', 999)
    img_title = tool.get_param_by_request(request.POST, 'img_title')
    img_url = request.FILES.get('img_url', '')
    old_img = tool.get_param_by_request(request.POST, 'old_image')
    image_path = old_img
    if img_url:
        image_path = tool.upload(img_url,settings.UPLOAD_IMG_PATH)
    wikiType_dict = {'name': name, 'short_name': short_name,'index': index,'img_title':img_title,'img_url':image_path}

    if action == 'add':
        insert_wikiCourseType= api_wiki_course_type.insert_wiki_course_type(wikiType_dict)
        if insert_wikiCourseType.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

    elif action == 'edit':
        _id = tool.get_param_by_request(request.POST,'id',0,int)
        wikiType_dict['id']=_id
        update_wikiType = api_wiki_course_type.update_wiki_course_type(wikiType_dict)
        if update_wikiType.is_error():
           return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect("/wiki/wikiCourseType/list/?action=query")


@dec_login_required
@handle_http_response_exception(501)
def wikiCourseType_edit(request):
    action = tool.get_param_by_request(request.GET, 'action', "edit")
    wikiCourseType = None
    seo={}
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        wikiCourseType = api_wiki_course_type.get_wikiCourseType_by_id(_id)
        if wikiCourseType.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        wikiCourseType = wikiCourseType.result()[0]
        seo_ret = api_objSEO.get_objSEO_by_obj('WIKICOURSETYPE', _id)
        if len(seo_ret.result()) > 0:
            seo = seo_ret.result()[0]
    c = {"type":wikiCourseType, "action": action,'seo':seo}
    return render_to_response("mz_wiki/wikiCourseType_add.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def wikiCourseType_list(request):
    '''
    显示全部wiki类型/删除wiki类型
    :param request:
    :return:
    '''
    action = tool.get_param_by_request(request.GET, 'action', 'query')
    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        ret_course = api_wiki_course.get_wiki_course_by_typeid(_id).result()
        if len(ret_course)>0:
            for course in ret_course:
                #如果该课程下有知识点，删除知识点对应的SEO
                ret_items = api_wiki_item.get_wiki_item_by_course(course['id']).result()
                if len(ret_items)>0:
                    for item in ret_items:
                        item_seo_count = api_objSEO.count_have_obj_seo(item['id'],"WIKIITEM")
                        if item_seo_count > 0:
                            api_objSEO.delete_objSEO_by_obj(item['id'],"WIKIITEM")
                #删除课程对应的SEO
                course_seo_count = api_objSEO.count_have_obj_seo(course['id'],"WIKICOURSE")
                if course_seo_count > 0:
                    api_objSEO.delete_objSEO_by_obj(course['id'],"WIKICOURSE")
        #删除类型对应的SEO
        type_seo_count = api_objSEO.count_have_obj_seo(_id,"WIKICOURSETYPE")
        if type_seo_count > 0:
            api_objSEO.delete_objSEO_by_obj(_id,"WIKICOURSETYPE")
        #删除wiki类型、课程以及知识点
        wikiCourseType = api_wiki_course_type.delete_wiki_course_type(_id)
        if wikiCourseType.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        return HttpResponseRedirect('/wiki/wikiCourseType/list/?action=query')
    else:
        wikiCourseType = api_wiki_course_type.list_wiki_course_type()
        if wikiCourseType.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        c = {"types": wikiCourseType.result()}
        return render_to_response("mz_wiki/wikiCourseType_list.html", c, context_instance=RequestContext(request))


@handle_ajax_response_exception
def wikiCourseType_isHaveTheShortName(request):
    short_name = tool.get_param_by_request(request.GET,'short_name')
    is_have = False
    count = api_wiki_course_type.count_have_wikiCourseType_short_name(short_name).result()
    if count>0:
        is_have = True
    result = {'is_have':is_have}
    return result

