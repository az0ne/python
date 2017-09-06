#! /usr/bin/evn python
# -*- coding:utf-8 -*-
from django.shortcuts import render
import db.api.lps4.common.tree
import db.api.course.stage
import db.api.lps4.career.lps4_careerData
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.logger import logger as log
from utils.tool import get_param_by_request
from django.http import JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings


@dec_login_required
@handle_http_response_exception(501)
def lps4_tree_edit(request):
    action = get_param_by_request(request.GET, "action", "add", str)
    APIResult = db.api.lps4.career.lps4_careerData.get_all_lps4_career()
    tree = None
    stages = None
    if APIResult.is_error():
        log.warn("get all lps4 career failed.")
        return render(request, "404.html")
    careers = APIResult.result()
    if action == "edit":
        _id = get_param_by_request(request.GET, "id", 0, int)
        get_tree = db.api.lps4.common.tree.get_lps4_tree_by_id(_id)
        if get_tree.is_error():
            log.warn("get lps4 tree by id failed.")
            return render(request, "404.html")
        tree = get_tree.result()
        if tree:
            get_stage = db.api.course.stage.get_stage_by_career_id(tree["career_id"])
            if get_stage.is_error():
                log.warn("get stage by career_id failed.")
                return render(request, "404.html")
            stages = get_stage.result()
    return render(request, "mz_lps4/tree/lps4_tree_edit.html", dict(action=action,
                                                                    careers=careers,
                                                                    tree=tree,
                                                                    stages=stages
                                                                    ))


@dec_login_required
@handle_http_response_exception(501)
def lps4_tree_list(request):
    action = get_param_by_request(request.GET, "action", "query", str)
    career_id = get_param_by_request(request.GET, "career_id", 0, int)
    page_index = get_param_by_request(request.GET, "page_index", 1, int)
    request.session["url_back"] = request.get_full_path()
    got_career = db.api.lps4.common.tree.list_lps4_tree()  # 获取lps4_tree中有的career
    if got_career.is_error():
        log.warn("list lps4 tree failed.")
        return render(request, "404.html")
    careers = got_career.result()
    had_careers = set((career["career_id"], career["career_name"]) for career in careers)
    dict_had_careers = []
    for career in had_careers:
        dict_had_careers.append(dict(id=career[0], name=career[1]))

    if action == "search":
        APIResult = db.api.lps4.common.tree.list_lps4_tree_by_search(page_index=page_index,
                                                                     page_size=settings.PAGE_SIZE,
                                                                     career_id=career_id)
    else:
        APIResult = db.api.lps4.common.tree.list_lps4_tree_by_page(page_index=page_index,
                                                                   page_size=settings.PAGE_SIZE)
    if APIResult.is_error():
        log.warn("list all lps4 tree failed.")
        return render(request, "404.html", {})
    result = APIResult.result()
    c = {"trees": result["result"], "careers": dict_had_careers, "career_id": career_id,
         "page": {"page_index": page_index, "rows_count": result["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": result["page_count"]}}
    return render(request, "mz_lps4/tree/lps4_tree_list.html", c)


@dec_login_required
@handle_http_response_exception(501)
def lps4_tree_save(request):
    action = get_param_by_request(request.POST, "action", "", str)
    if action in ["add", "edit"]:
        career_id = get_param_by_request(request.POST, "career", 0, int)
        stage_id = get_param_by_request(request.POST, "stage", 0, int)
        name = get_param_by_request(request.POST, "stage_name", "", str)
        index = get_param_by_request(request.POST, "index", 0, int)
        data = dict(career_id=career_id, stage_id=stage_id, stage_name=name, index=index)
        if action == "edit":
            _id = get_param_by_request(request.POST, "id", 0, int)
            data["id"] = _id
            APIResult = db.api.lps4.common.tree.update_lps4_tree(data)
        else:
            APIResult = db.api.lps4.common.tree.insert_lps4_tree(data)
        if APIResult.is_error():
            log.warn("add or edit lps4 tree failed.")
            return render(request, "404.html", {})
    return HttpResponseRedirect(request.session.get("url_back", reverse("mz_lps4:tree_list")))


@dec_login_required
@handle_http_response_exception(501)
def delete_lps4_by_id(request):
    _id = get_param_by_request(request.GET, "id", 0, int)
    APIResult = db.api.lps4.common.tree.delete_lps4_tree_by_id(_id)
    if APIResult.is_error():
        log.warn("delete lps4 tree failed.")
        return render(request, "404.html", {})
    return HttpResponseRedirect(reverse("mz_lps4:tree_list"))


@dec_login_required
@handle_http_response_exception(501)
def get_stage_by_career_id(request):
    career_id = get_param_by_request(request.GET, "career_id", 0, int)
    stages = None
    if career_id:
        get_stages = db.api.course.stage.get_stage_by_career_id(career_id)
        if get_stages.is_error():
            log.warn("get stage by career id failed.")
            return render(request, "404.html")
        stages = get_stages.result()
        return JsonResponse(dict(status="success", stages=stages))
    return JsonResponse(dict(status="failed", stages=stages))
