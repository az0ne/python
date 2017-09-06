#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.http import JsonResponse

from utils.decorators import dec_login_validate
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request, upload
from db.api.apiutils import cache
from utils.logger import logger as log


@dec_login_validate
def cache_keys(request):

    log.info("started cache_keys request. user_id: %s, user_name: %s" % (
        request.session["userid"], request.session["username"]))

    return HttpResponse("\n".join(cache.keys()))


@dec_login_validate
def delete_cache(request):

    log.info("started delete_cache request. user_id: %s, user_name: %s" % (
        request.session["userid"], request.session["username"]))

    key = get_param_by_request(request.GET, "key", "", str)
    
    if not key:
        return HttpResponse(False)
        
    return HttpResponse(bool(cache.delete(key)))


# @dec_login_validate
@handle_http_response_exception(501)
def upload_file(request):
    image_url = ""
    if request.method == 'POST':
        image = request.FILES.get('image', None)
        if image:
            image_url = upload(image, settings.UPLOAD_IMG_PATH)
    return JsonResponse(dict(img_url=image_url))
