# -*- coding: utf-8 -*-

from datetime import datetime
from django.http import HttpResponse
from website.api.user.decorators import app_user_required
from utils.logger import logger as log
from utils.tool import get_param_by_request
from core.common.http.response import success_json, failed_json
from db.api.common.wechat import wechat_menu, wechat_message
import db.api


@app_user_required
def views_append_study_info(request):
    """
    append study info to mongodb
    :param request:
    :return HttpResponse:
    """

    if request.method == "GET":
        course_id = get_param_by_request(request.GET, "course_id", _type=int)
        lesson_id = get_param_by_request(request.GET, "lesson_id", _type=int)
        user_id = request.user.id
        user_nickname = request.user.nick_name

        if not (course_id or lesson_id):
            log.info("invalid params. "
                     "course_id: %s, lesson_id: %s" % (course_id, lesson_id))
            return HttpResponse()

        api_result = db.api.append_study_info(
                datetime.now(),
                user_id,
                course_id,
                lesson_id)

        if api_result.is_error() == True:
            log.warn("append_study_info failed. "
                     "course_id: %s, lesson_id: %s, user_id: %s"
                     % (course_id, lesson_id, user_id))
        else:
            res = api_result.result()

            log.biz({
                "biz_type": "user video time",
                "msg": "append_study_info succeed.",
                "day": res["day"].strftime('%Y-%m-%d %H:%M:%S'),
                "minute": res["minute"],
                "course_id": course_id,
                "lesson_id": lesson_id,
                "user_id": user_id,
                "user_name": user_nickname,
            })

    return HttpResponse()


def wechat_click_reply(request):
    # 微信点击事件回复内容
    result = wechat_menu()
    if result.is_error():
        return failed_json(u'查询数据出错')
    return success_json({'list': result.result()})


def wechat_message_reply(request):
    # 微信消息回复内容
    result = wechat_message()
    if result.is_error():
        return failed_json(u'查询数据出错')
    return success_json({'list': result.result()})

