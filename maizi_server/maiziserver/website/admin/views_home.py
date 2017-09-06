# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.user import user as api_user
from django.http import HttpResponseNotFound,HttpResponseServerError

def home(request):
    context ={
    }
    return render(request,'welcome.html',context)