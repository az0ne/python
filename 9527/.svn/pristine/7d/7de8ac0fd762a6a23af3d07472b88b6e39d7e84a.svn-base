#!/usr/bin/env python
# -*- coding:utf-8 -*-
from utils.tool import get_param_by_request
import db.api.homepage.homepage_wiki
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
def homepage_wiki_list(request):
    get_homepage_wiki = db.api.homepage.homepage_wiki.homepage_wiki_list()
    if get_homepage_wiki.is_error():
        log.warn("get all homepage_wiki failed")
        return render(request, "404.html", {"message": "get homepage_wiki failed."})
    homepage_wikies = get_homepage_wiki.result()
    return render(request, 'mz_homepage/homepage_wiki_list.html', dict(homepage_wikies=homepage_wikies))


@dec_login_required
@handle_http_response_exception(501)
def homepage_wiki_edit(request):
    action = get_param_by_request(request.GET, 'action', 'query', '')
    _id = get_param_by_request(request.GET, 'id', 0, int)
    get_homepage_wiki = db.api.homepage.homepage_wiki.get_homepage_wiki_by_id(_id)
    if get_homepage_wiki.is_error():
        log.warn("get homepage_wiki by id failed.id=%s" % _id)
        return render(request, "404.html", {"message": "get homepage_wiki by id failed.id=%s" % _id})
    homepage_wiki = get_homepage_wiki.result()
    return render(request, 'mz_homepage/homepage_wiki_edit.html', dict(action=action, homepage_wiki=homepage_wiki))


@dec_login_required
@handle_http_response_exception(501)
def homepage_wiki_save(request):
    _id = get_param_by_request(request.POST, 'id', 0, int)
    title = get_param_by_request(request.POST, 'title', '', str)
    abstract = get_param_by_request(request.POST, 'abstract', '', str)
    wiki_url = get_param_by_request(request.POST, 'wiki_url', '', str)
    old_title_image = get_param_by_request(request.POST, 'old_title_image', '', str)
    title_image = request.FILES.get('title_image', '')
    image_path = old_title_image
    if title_image:
        image_path = upload(title_image, settings.UPLOAD_IMG_PATH)
    data = dict(id=_id,title=title,abstract=abstract,wiki_url=wiki_url,image_path=image_path)
    update_homepage_wiki = db.api.homepage.homepage_wiki.update_homepage_wiki(data)
    if update_homepage_wiki.is_error() or not update_homepage_wiki.result():
        log.warn("update homepage_wiki failed.data:{0}".format(data))
        return render(request, "404.html", {"message": "update homepage_wiki failed.data:{0}".format(data)})
    return HttpResponseRedirect(reverse('mz_homepage:homepageWiki_list'))