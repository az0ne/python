# -*- coding:utf-8 -*-
import datetime
from utils.decorators import dec_login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
import json
from db.api.course import objTagRelation as api_objTagRelation
from db.api.course import careerObjRelation as api_careerObjRelation
from db.api.article import article as api_acticle
from db.api.seo import objSEO as api_objSEO
from utils import tool
from utils.handle_exception import handle_http_response_exception
from bs4 import BeautifulSoup

# 全局变量
CURRENT_URL = ''  # 记录查看或修改某一条数据前的url地址


# Create your views here.
def article_page(request, template_name):
    session_name = request.session.get('username')
    if session_name is None:
        return render_to_response('loginindex.html', {}, context_instance=RequestContext(request))
    else:
        return render_to_response(template_name, {'session_name': session_name},
                                  context_instance=RequestContext(request))
    return render(request, template_name)


@dec_login_required
@handle_http_response_exception(501)
def article_save(request):
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    key_word = tool.get_param_by_request(request.POST, 'keyword', "", str)
    action = tool.get_param_by_request(request.POST, 'action', "add", str)
    title = tool.get_param_by_request(request.POST, 'title', "", str)
    sub_title = tool.get_param_by_request(request.POST, 'sub_title', '', str)
    content = tool.get_param_by_request(request.POST, 'content', "", str)
    abstract = tool.get_param_by_request(request.POST, 'abstract', "", str)
    image_url = request.FILES.get('title_image', '')
    old_image_path = tool.get_param_by_request(request.POST, 'old_image', " ", str)
    article_type_id = tool.get_param_by_request(request.POST, 'article_type', 4, int)
    is_top = tool.get_param_by_request(request.POST, 'is_top', 0, int)
    is_actived = 1  # tool.get_param_by_request(request.POST, 'is_actived', 1, int)
    obj_type = 'ARTICLE'
    seo_title = tool.get_param_by_request(request.POST, 'seo_title', "", str)
    seo_keywords = tool.get_param_by_request(request.POST, 'seo_keywords', "", str)
    seo_description = tool.get_param_by_request(request.POST, 'seo_description', "", str)
    careercatagory_id = tool.get_param_by_request(request.POST, 'careercatagory', 0, int)
    career_id = tool.get_param_by_request(request.POST, 'careercourse', 0, int)
    page_index = tool.get_param_by_request(request.POST, 'page_index', "1", str)
    #  page_index = tool.get_param_by_request(request.GET, 'page_index', "1", int)
    image_path = old_image_path  # 如果更新数据时，未更改图片，image_url为空，设置图片的路径为老路径
    publish_date = datetime.datetime.now()
    tags_list = request.POST.getlist('tag')

    if image_url:
        image_path = tool.upload(image_url, settings.ARTICLE_IMG_UPLOAD_PATH)

    html = content
    retrieval = BeautifulSoup(html, "html.parser").get_text()
    if action == 'add':
        user_id = request.session['userid']
        username = api_acticle.get_userprofileinfo_by_id(user_id)
        nick_name = ""
        user_head = ""
        if username.result():
            if username.result()[0]["nick_name"]:
                nick_name = username.result()[0]["nick_name"]
            if username.result()[0]["avatar_small_thumbnall"]:
                user_head = username.result()[0]["avatar_small_thumbnall"]
        article = api_acticle.insert_Article(title, sub_title, content, abstract, image_path, user_id, nick_name,
                                             user_head, publish_date, article_type_id, is_top, retrieval)
        obj_id = article.result()
        ret_seo = api_objSEO.insert_obj_seo(obj_type, obj_id, seo_title, seo_keywords, seo_description)
        ret_careerobj = api_careerObjRelation.insert_career_obj_relation(obj_type, obj_id, career_id, is_actived)
        if len(tags_list) > 0:
            for tag_id in tags_list:
                api_objTagRelation.insert_obj_tag_relation(obj_type, obj_id, tag_id, careercatagory_id)
        if article.is_error() or ret_seo.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))

    elif action == 'edit':
        article = api_acticle.update_Article(_id, title, sub_title, content, abstract, image_path, article_type_id,
                                             is_top, retrieval)
        del_objTagRelation = api_objTagRelation.delete_objTagRelation_by_obj(_id, obj_type)
        del_objSEO = api_objSEO.delete_objSEO_by_obj(_id, obj_type)
        del_career = api_careerObjRelation.delete_careerobjrelation_by_obj(_id, obj_type)
        if not del_objSEO.is_error():
            ret_seo = api_objSEO.insert_obj_seo(obj_type, _id, seo_title, seo_keywords, seo_description)
        if not del_career.is_error():
            ret_careerobj = api_careerObjRelation.insert_career_obj_relation(obj_type, _id, career_id, is_actived)
        if len(tags_list) > 0:
            for tag_id in tags_list:
                ret_objTagRelation = api_objTagRelation.insert_obj_tag_relation(obj_type, _id, tag_id,
                                                                                careercatagory_id)
        if article.is_error() or del_objTagRelation.is_error() or del_objSEO.is_error() or ret_seo.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect(tool.get_correct_url(CURRENT_URL, reverse('mz_article:article_list')))


@dec_login_required
@handle_http_response_exception(501)
def article_edit(request):
    action = tool.get_param_by_request(request.GET, 'action', "add")
    page_index = tool.get_param_by_request(request.GET, 'page_index', "1", int)
    obj_type = 'ARTICLE'
    article = None
    if action == "edit" or action == "show":
        _id = tool.get_param_by_request(request.GET, 'id', "0", int)
        keyword = tool.get_param_by_request(request.GET, 'keyword', "", str)
        article = api_acticle.get_Article_by_id(_id)
        tags = api_objTagRelation.get_tags_by_obj(_id, obj_type).result()
        careercourse_list = api_careerObjRelation.get_careercourse_by_obj(_id, obj_type).result()
        if article.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        article = article.result()[0]
        careercourse = careercourse_list[0] if len(careercourse_list) > 0 else None
        c = {"article": article, 'careercourse': careercourse, 'tags': json.dumps(tags), "action": action,
             "page_index": page_index, "keyword": keyword}
    else:
        c = {"article": article, "action": action, "page_index": page_index}
    return render_to_response("mz_article/article_add.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def article_list(request):
    action = tool.get_param_by_request(request.GET, 'action', 'query', str)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)
    article_type_id = tool.get_param_by_request(request.GET, 'articleTypeId', 0, int)
    career_course_id = tool.get_param_by_request(request.GET, 'careerCourseId', 0, int)
    sort = tool.get_param_by_request(request.GET, 'sort', 1, int)

    obj_type = 'ARTICLE'

    if action == "delete":
        _id = tool.get_param_by_request(request.GET, 'id', 0, int)
        del_objTagRelation = api_objTagRelation.delete_objTagRelation_by_obj(_id, obj_type)
        del_objSEO = api_objSEO.delete_objSEO_by_obj(_id, obj_type)
        del_career = api_careerObjRelation.delete_careerobjrelation_by_obj(_id, obj_type)
        article = api_acticle.delete_Article(_id)
        if article.is_error() or del_objTagRelation.is_error() or del_objSEO.is_error() or del_career.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        return HttpResponseRedirect(tool.get_correct_url(CURRENT_URL, reverse('mz_article:article_list')))
    if action == "careerchked":
        chkid = tool.get_param_by_request(request.GET, 'id', 0, int)
        article = api_acticle.checked_param(chkid)
        if article.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        return HttpResponseRedirect(tool.get_correct_url(CURRENT_URL, reverse('mz_article:article_list')))

    if action == "careerchk":
        chkedid = tool.get_param_by_request(request.GET, 'id', 0, int)
        article = api_acticle.check_param(chkedid)
        if article.is_error():
            return render_to_response("404.html", {}, context_instance=RequestContext(request))
        return HttpResponseRedirect(tool.get_correct_url(CURRENT_URL, reverse('mz_article:article_list')))

    if action == 'query' or action == 'search':
        global CURRENT_URL
        CURRENT_URL = request.get_full_path()
        article = api_acticle.list_Article_by_page(key_word, article_type_id, career_course_id, sort, page_index,
                                                   settings.PAGE_SIZE)

    if article.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    c = {"articles": article.result()["result"],
         "articleTypeId": article_type_id,
         "careerCourseId": career_course_id,
         "keyword": key_word,
         "sort": sort,
         "page": {"page_index": page_index, "rows_count": article.result()["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": article.result()["page_count"]}}

    return render_to_response("mz_article/article_list.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def article_adpic(request):
    _id = tool.get_param_by_request(request.GET, 'id', 0, int)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    article = api_acticle.insert_pic(_id)
    key_word = tool.get_param_by_request(request.GET, 'keyword', "", str)
    if article.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    c = {"articles": article.result(), "page_index": page_index, "keyword": key_word}
    return render_to_response("mz_article/article_addpic.html", c, context_instance=RequestContext(request))


def articletitle_save(request):
    key_word = tool.get_param_by_request(request.POST, "keyword", "", str)
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, str)

    old_image_pathone = tool.get_param_by_request(request.POST, 'old_imageone', '')
    old_image_pathtwo = tool.get_param_by_request(request.POST, 'old_imagetwo', '')
    old_image_paththr = tool.get_param_by_request(request.POST, 'old_imagethr', '')

    image_titleone = request.FILES.get('title_image1', '')
    image_titletwo = request.FILES.get('title_image2', '')
    image_titlethr = request.FILES.get('title_image3', '')

    image_pathone = old_image_pathone
    image_pathtwo = old_image_pathtwo
    image_paththr = old_image_paththr

    if image_titleone:
        image_pathone = tool.upload(image_titleone, settings.ARTICLE_IMG_UPLOAD_PATH)
    if image_titletwo:
        image_pathtwo = tool.upload(image_titletwo, settings.ARTICLE_IMG_UPLOAD_PATH)
    if image_titlethr:
        image_paththr = tool.upload(image_titlethr, settings.ARTICLE_IMG_UPLOAD_PATH)

    article = api_acticle.insert_Articletitleimg(_id, image_pathone, image_pathtwo, image_paththr)
    if article.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect(tool.get_correct_url(CURRENT_URL, reverse('mz_article:article_list')))


@dec_login_required
@handle_http_response_exception(501)
def article_infochag(request):
    _id = tool.get_param_by_request(request.GET, 'id', 0, int)
    page_index = tool.get_param_by_request(request.GET, 'page_index', 1, int)
    article = api_acticle.article_likeinfo(_id)
    if article.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    c = {"articles": article.result(), "page_index": page_index, "id": _id,}
    return render_to_response("mz_article/chagarticle_info.html", c, context_instance=RequestContext(request))


@dec_login_required
@handle_http_response_exception(501)
def article_confchg(request):
    _id = tool.get_param_by_request(request.POST, 'id', 0, int)
    key_word = tool.get_param_by_request(request.POST, 'keyword', "", str)
    page_index = tool.get_param_by_request(request.POST, 'page_index', 1, int)
    view = tool.get_param_by_request(request.POST, 'view_count', 1, int)
    praise = tool.get_param_by_request(request.POST, 'praise_count', 1, int)
    article = api_acticle.article_chginfo(_id, view, praise)
    if article.is_error():
        return render_to_response("404.html", {}, context_instance=RequestContext(request))
    return HttpResponseRedirect(tool.get_correct_url(CURRENT_URL, reverse('mz_article:article_list')))
