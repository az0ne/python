# -*- coding:utf-8 -*-
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from db.api.course import tag as api_tag
from db.api.course import course_ajax as api_courseajax
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
