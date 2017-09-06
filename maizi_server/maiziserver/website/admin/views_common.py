# -*- coding: utf-8 -*-

from PIL import Image
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.user import user as api_user
from django.http import HttpResponseNotFound,HttpResponseServerError, StreamingHttpResponse
from django.http.response import JsonResponse
import os
import random
import time


def add_success(request):
    op_url = views_tools.get_param_by_request(request.GET, "op_url", "")
    return_url = views_tools.get_param_by_request(request.GET, "return_url", "")
    context ={
        "op_url" : op_url,
        "return_url" : return_url
    }
    return render(request,'add_success.html',context)

def update_success(request):
    return_url = views_tools.get_param_by_request(request.GET, "return_url", "")
    context ={
        "return_url" : return_url
    }
    return render(request,'update_success.html',context)

@csrf_exempt
def upload(request):

    file = request.FILES.get('file', None)

    # im = Image.open(file)
    # x,y = im.size
    # if x!=300 and y != 400:
    #     return JsonResponse({"success": 1, "code": False, "error": "像素要求为300×400"})

    file_type_list = [".png",".jpg",".doc",".docx",".pdf",".xls",".xlsx",".ppt",".pptx"]

    file_name = time.strftime("%Y%m%d%H%M%S", time.localtime())
    extension = ""
    is_type = False
    for ex in file_type_list:
        if file.name.find(ex) != -1:
            is_type = True
            file_name = file_name + ex
            extension = ex
            break
    if is_type == False:
        return JsonResponse({"success": 1, "code": False, "error": "请上传正确的格式"})


    destination = open(os.path.join(settings.UPLOAD_DOCUMENT_DIRS , file_name), 'wb+')  # 打开特定的文件进行二进制的写操作

    for chunk in file.chunks():  # 分块写入文件
        destination.write(chunk)
    destination.close()

    return JsonResponse({"success":1,"code":True,"file_name":file_name,"extension":extension})

@csrf_exempt
def upload_check_ratio(request):
        file = request.FILES.get('file', None)

        im = Image.open(file)
        x,y = im.size
        if x!=640 and y != 480:
            return JsonResponse({"success": 1, "code": False, "error": "像素要求为640×480"})

        return JsonResponse({"success":1,"code":True})
