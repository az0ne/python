#!/usr/bin/env python
# -*- coding:utf-8 -*-
from utils.tool import get_param_by_request
import db.api.common.coursepage_wiki
import db.api.course.careerCourse
from django.shortcuts import render
from utils.logger import logger as log
from utils.tool import upload
from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from utils.handle_exception import handle_http_response_exception
from utils.decorators import dec_login_required


@dec_login_required
@handle_http_response_exception(501)
def course_wiki_list(request):
    career_id = get_param_by_request(request.GET, "career_id", 0, int)
    career_courses = []
    request.session["url_back"] = request.get_full_path()

    get_career_info = get_course_wiki = db.api.common.coursepage_wiki.course_page_wiki_list()
    if career_id > 0:
        get_course_wiki = db.api.common.coursepage_wiki.get_course_page_wiki_list_by_career_id(career_id)

    if get_course_wiki.is_error() or get_career_info.is_error():
        log.warn("get all course_wiki failed.career_id=%s" % career_id)
        return render(request, "404.html", {"message": "get course_wiki failed."})
    course_wikies = get_course_wiki.result()
    career_info = get_career_info.result()

    if career_info:
        for course in career_info:
            career_info = dict(id=course["course_id"], name=course["name"])
            if career_info not in career_courses:
                career_courses.append(career_info)
    return render(request, 'mz_common/coursepage_wiki_list.html', dict(course_wikies=course_wikies,
                                                                       careercourses=career_courses,
                                                                       career_id=career_id))


@dec_login_required
@handle_http_response_exception(501)
def course_wiki_edit(request):
    action = get_param_by_request(request.GET, 'action', 'query', '')
    _id = get_param_by_request(request.GET, 'id', 0, int)
    get_course_wiki = db.api.common.coursepage_wiki.get_course_wiki_by_id(_id)
    if get_course_wiki.is_error():
        log.warn("get course_wiki by id failed.id=%s" % _id)
        return render(request, "404.html", {"message": "get course_wiki by id failed.id=%s" % _id})
    course_wiki = get_course_wiki.result()
    return render(request, 'mz_common/coursepage_wiki_edit.html', dict(action=action, course_wiki=course_wiki))


@dec_login_required
@handle_http_response_exception(501)
def course_wiki_save(request):
    _id = get_param_by_request(request.POST, 'id', 0, int)
    title = get_param_by_request(request.POST, 'title', '', str)
    wiki_url = get_param_by_request(request.POST, 'wiki_url', '', str)
    old_title_image = get_param_by_request(request.POST, 'old_title_image', '', str)
    title_image = request.FILES.get('title_image', '')
    image_path = old_title_image
    if title_image:
        image_path = upload(title_image, settings.UPLOAD_IMG_PATH)
    data = dict(id=_id, title=title, wiki_url=wiki_url, image_path=image_path)
    update_course_wiki = db.api.common.coursepage_wiki.update_course_wiki(data)
    if update_course_wiki.is_error() or not update_course_wiki.result():
        log.warn("update course_wiki failed.data:{0}".format(data))
        return render(request, "404.html", {"message": "update course_wiki failed.data:{0}".format(data)})
    return HttpResponseRedirect(request.session.get("url_back", reverse('mz_common:courseWiki_list')))
