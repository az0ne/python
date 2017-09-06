#! /usr/bin/evn python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from utils.logger import logger as log
import db.api.lps4.course.task

IS_PROJECT = (u"否",  u"是")


def get_task_name_by_id(request, _id):
    name = u"无"
    if _id > 0:
        APIResult = db.api.lps4.course.task.get_task_by_id(_id)
        if APIResult.is_error():
            log.warn("get task by id failed.")
            return render(request, "404.html", {})
        task = APIResult.result()
        if task:
            name = task["name"]
    return name