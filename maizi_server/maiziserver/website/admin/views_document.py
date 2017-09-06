# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.document import document as api_document
from django.http import HttpResponseNotFound,HttpResponseServerError,StreamingHttpResponse
import os

def get_query(request):

    name = views_tools.get_param_by_request(request.GET, "name", "")
    type = views_tools.get_param_by_request(request.GET, "type", "")

    page = {}
    query = {
            "name": name,
            "type": type
    }

    return {
        "query": query,
        "page": page
    }

def document_query(request):
    query_info = get_query(request)
    result = api_document.list_document(query_info["query"]["type"], query_info["query"]["name"])
    if result.is_error():
        return HttpResponseServerError()

    document_list = result.result()["result"]

    context = {
        "menu":"document",
        "url": "/document/",
        "page": {},
        "query": query_info["query"],
        "queryString": views_tools.getQueryString(query_info["query"]),
        "document_list": document_list
    }

    return context

def document(request):
    context = document_query(request)

    return render(request,'admin/document.html',context)

def document_delete(request):

    document_id = views_tools.get_param_by_request(request.GET, "id", "")

    result = api_document.delete(document_id)
    if result.is_error():
        return HttpResponseServerError()

    context = career_query(request)
    return render(request,'admin/document.html',context)

def document_add(request):
    context = {
        "menu": "document"
    }
    return render(request,'admin/document_add.html',context)

@csrf_exempt
def document_add_do(request):

    name = views_tools.get_param_by_request(request.POST, "name", "")
    type = views_tools.get_param_by_request(request.POST, "type", "0")
    author = views_tools.get_param_by_request(request.POST, "author", "")
    extension = views_tools.get_param_by_request(request.POST, "extension", "")
    file_name = views_tools.get_param_by_request(request.POST, "file_name", "")

    uploader = "李希"#request.session["real_name"]
    result = api_document.add(name,file_name,author,uploader,type,extension)
    return views_tools.success_json()

def download_document(request):
    id = views_tools.get_param_by_request(request.GET, "id", "")

    result = api_document.get_document_by_id(id)

    if result.is_error():
        return HttpResponseServerError()

    document_info = result.result()
    if document_info == None:
        return HttpResponseServerError()

    full_file_name = os.path.join(settings.UPLOAD_DOCUMENT_DIRS,document_info["file_name"])

    def file_iterator(file_name, chunk_size=512):
        with open(file_name,'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    response = StreamingHttpResponse(file_iterator(full_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format((document_info["name"] + document_info["extension"]).encode('utf-8'))
    response['Content-Length'] = os.path.getsize(full_file_name)
    return response
