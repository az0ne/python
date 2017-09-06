# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from maiziserver.tools import views_tools
from maiziserver.db.api.career import note as api_note
from django.http import HttpResponseNotFound,HttpResponseServerError


def note(request):
    item_id = views_tools.get_param_by_request(request.GET, "item_id", "")
    course_id = views_tools.get_param_by_request(request.GET, "course_id", "")
    knowledge_id = views_tools.get_param_by_request(request.GET, "knowledge_id",
    "")

    result = api_note.list_note()

    context = {
    "menu":'career',
    "notes":result.result(),
    "item_id":item_id,
    "course_id":course_id,
    "knowledge_id":knowledge_id
    }

    return render(request, "admin/career/note.html", context)

def item_note(request):
    item_id = views_tools.get_param_by_request(request.GET, "item_id", "")
    course_id = views_tools.get_param_by_request(request.GET, "course_id", "")
    knowledge_id = views_tools.get_param_by_request(request.GET, "knowledge_id",
    "")

    result = api_note.get_note(item_id, knowledge_id, course_id)

    context = {
    "menu":'career',
    "notes":result.result(),
    "item_id":item_id,
    "course_id":course_id,
    "knowledge_id":knowledge_id
    }

    return render(request, "admin/career/item_note.html", context)

def item_note_add(request):
    course_id = views_tools.get_param_by_request(request.GET, "course_id", "")
    knowledge_id = views_tools.get_param_by_request(request.GET, "knowledge_id", "")
    item_id = views_tools.get_param_by_request(request.GET, "item_id", "")

    context = {
        "course_id":course_id,
        "knowledge_id":knowledge_id,
        "item_id":item_id,
        "menu":"career"
    }

    return render(request, "admin/career/note_add.html",context)

@csrf_exempt
def item_note_add_do(request):

    item_id = views_tools.get_param_by_request(request.POST, "item_id","")
    knowledge_id = views_tools.get_param_by_request(request.POST, "knowledge_id","")
    course_id = views_tools.get_param_by_request(request.POST, "course_id","")
    content = views_tools.get_param_by_request(request.POST, "content","")

    result = api_note.add_note(content,item_id,knowledge_id,course_id)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()

def item_note_update(request):
    course_id = views_tools.get_param_by_request(request.GET, "course_id", "")
    knowledge_id = views_tools.get_param_by_request(request.GET, "knowledge_id", "")
    item_id = views_tools.get_param_by_request(request.GET, "item_id", "")
    note_id = views_tools.get_param_by_request(request.GET, "note_id", "")
    # print "$"*100
    # print note_id
    # print "$"*100
    result = api_note.get_note_by_id(note_id)

    context = {
    "menu":"career",
    "course_id":course_id,
    "knowledge_id":knowledge_id,
    "item_id":item_id,
    "note":result.result()
    }

    return render(request, "admin/career/note_update.html", context)

@csrf_exempt
def item_note_update_do(request):
    # course_id = views_tools.get_param_by_request(request.POST, "course_id", "")
    # knowledge_id = views_tools.get_param_by_request(request.POST, "knowledge_id", "")
    content = views_tools.get_param_by_request(request.POST, "content", "")
    note_id = views_tools.get_param_by_request(request.POST, "note_id", "")

    result = api_note.update_note(content,note_id)

    if result.is_error():
        return HttpResponseServerError

    return views_tools.success_json()
