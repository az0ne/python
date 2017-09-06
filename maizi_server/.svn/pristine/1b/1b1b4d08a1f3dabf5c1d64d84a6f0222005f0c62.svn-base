# -*- coding: utf-8 -*-
import datetime
from collections import OrderedDict

from django.http import HttpResponse
from django.http.response import HttpResponseServerError
from django.shortcuts import render

from maiziserver.db.api.activity import activity as api_activity
from maiziserver.db.api.activity.activity import get_active_point_by_month, \
    get_total_active_point_by_phone
from maiziserver.db.api.career import career as api_career

from maiziserver.tools import views_tools


def get_query_assistant(request):
    page_index = views_tools.get_param_by_request(request.GET, "page_index", 1, int)
    page_size = views_tools.get_param_by_request(request.GET, "page_size", 10, int)

    account = views_tools.get_param_by_request(request.GET, "account", "")
    student_name = views_tools.get_param_by_request(request.GET, "student_name", "")
    career_id = views_tools.get_param_by_request(request.GET, "career_id", -1, int)
    career_job = views_tools.get_param_by_request(request.GET, "career_job", -1, int)
    assistant_id = views_tools.get_param_by_request(request.GET, "assistant_id", -1, int)
    teacher_id = views_tools.get_param_by_request(request.GET, "teacher_id", -1, int)
    reward = views_tools.get_param_by_request(request.GET, "reward", -1, int)

    page = {
        "page_index": page_index,
        "page_size": page_size
    }

    query = {
        "account": account,
        "student_name": student_name,
        "career_id": str(career_id),
        "career_job": str(career_job),
        "assistant_id": str(assistant_id),
        "teacher_id": str(teacher_id),
        "reward": str(reward)
    }

    return {
        "query": query,
        "page": page
    }


def learning_activity_query(request):
    query_info = get_query_assistant(request)
    skip = views_tools.get_skip(query_info["page"]["page_index"], query_info["page"]["page_size"])
    result = api_activity.list_learn_activity(query_info["query"]["student_name"],
                                              query_info["query"]["career_job"],
                                              query_info["query"]["career_id"],
                                              skip)
    if result.is_error():
        return HttpResponseServerError()

    rows_count = result.result()["rows_count"]
    student_list = result.result()["result"]
    print student_list
    page = views_tools.get_page(query_info["page"]["page_index"],
                                query_info["page"]["page_size"],
                                rows_count)

    career_list = api_career.list_career().result()["result"]

    context = {
        "menu": "assistant",
        "url": "/student_assistant_monitor_learn_activity/",
        "page": page,
        "query": query_info["query"],
        "queryString": views_tools.getQueryString(query_info["query"]),
        "student_list": student_list,
        "career_list": career_list,
    }

    return context


def learning_activity_index(request):
    # 学习活跃的主页

    context = learning_activity_query(request)

    return render(request, 'admin/monitor-learn-activity/index.html', context)


def list_active_point_by_student(request):
    phone = views_tools.get_param_by_request(request.GET, 'phone', '', str)

    total_score = get_total_active_point_by_phone(phone)
    print total_score
    currentMonth = datetime.datetime.now().month
    currentYear = datetime.datetime.now().year

    # maybe buggy here
    try:
        result_list = [
            (currentMonth, currentYear,
             get_active_point_by_month(phone, currentYear, currentMonth).result()['result'][0]),
            # (currentMonth-1, currentYear,
            #  get_active_point_by_month(student_id, currentYear, currentMonth-1).result()['result'][0]),
            # (currentMonth-2, currentYear,
            #  get_active_point_by_month(student_id, currentYear, currentMonth-2).result()['result'][0]),
            # (currentMonth-3, currentYear,
            #  get_active_point_by_month(student_id, currentYear, currentMonth-3).result()['result'][0]),
        ]
    except Exception as e:
        result_list=[]

    context = {
        "menu": "assistant",
        "url": "student_assistant/active_points/",
        "result_list": result_list,
        "total_score": total_score.result()['result'][0]['score']
    }

    return render(request, 'admin/monitor-learn-activity/points.html', context)
