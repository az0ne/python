# -*- coding:utf-8 -*-
from django.http import Http404
from django.http import HttpResponse

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception

from django.http import HttpResponseRedirect, JsonResponse
from db.api.lps4.career import lps4_careerData
from django.shortcuts import render
from utils.tool import get_param_by_request, upload
from django.conf import settings
from django.core.urlresolvers import reverse
from utils.logger import logger as log

CAREER_TYPE = {"CAREER": u"职业课程", "WEIKE": u"微课"}


@dec_login_required
@handle_http_response_exception(501)
def career_list(request):
    listdata = lps4_careerData.get_all_lps4_career()
    if listdata.is_error():
        return render(request, "404.html")
    careers = listdata.result()
    if careers:
        for career in careers:
            career["type_name"] = CAREER_TYPE[career["type"].upper()]
    list = {"list": careers}
    return render(request, "mz_lps4/career/careerList.html", list)


@dec_login_required
@handle_http_response_exception(501)
def revise_career(request):
    action = get_param_by_request(request.GET, 'action', 'add', str)
    career_id = get_param_by_request(request.GET, 'id', 0, int)
    career = None
    if action == "revise":
        career = get_career_by_id(request, career_id)
    c = {"career": career, "action": action}
    return render(request, "mz_lps4/career/careerrevise.html", c)


@dec_login_required
@handle_http_response_exception(501)
def save_career(request):
    action = get_param_by_request(request.POST, 'action', '', str)
    career_id = get_param_by_request(request.POST, 'careerId', 0, int)
    career_name = get_param_by_request(request.POST, 'careerName', '', str)
    career_type = get_param_by_request(request.POST, 'careerType', '', str)
    ad_type = get_param_by_request(request.POST, 'adType', "", str)
    url = ""  # 图片关联的广告url
    price = get_param_by_request(request.POST, 'price', 0, float)
    old_price = get_param_by_request(request.POST, 'old_price', 0, float)
    jobless_price = get_param_by_request(request.POST, 'jobless_price', 0, float)
    description = get_param_by_request(request.POST, 'description', "", str)
    video_url = ""
    short_name = get_param_by_request(request.POST, 'short_name', "", str)
    old_image_url = get_param_by_request(request.POST, 'old_image_url', "", str)
    image = request.FILES.get('image', '')
    ad_url = upload(image, settings.UPLOAD_IMG_PATH) if image else old_image_url

    if ad_type == "IMAGE":
        url = get_param_by_request(request.POST, 'url', "", str)

    elif ad_type == "VIDEO":
        video_url = get_param_by_request(request.POST, 'video_url', "", str)

    data = dict(id=career_id, name=career_name, type=career_type, ad_type=ad_type, ad_url=ad_url, url=url,
                price=price, old_price=old_price, description=description, jobless_price=jobless_price,
                short_name=short_name, video_url=video_url)
    if action == "revise":
        upcareerdata = lps4_careerData.up_career_name(data)
        if upcareerdata.is_error():
            return render(request, "404.html")
    elif action == "add":
        career = get_career_by_id(request, career_id)
        if not career:
            insertcareerdata = lps4_careerData.insert_career(data)
            if insertcareerdata.is_error():
                return render(request, "404.html")
        else:
            return HttpResponse(u'ERROR:该ID的课程已存在，请重新检查表单信息。')
    return HttpResponseRedirect(reverse("mz_lps4:career_list"))


@dec_login_required
@handle_http_response_exception(501)
def check_short_name(request):
    short_name = get_param_by_request(request.GET, "short_name", "", str)
    _id = get_param_by_request(request.GET, "id", 0, int)
    action = get_param_by_request(request.GET, "action", "add", str)
    is_had = False
    if short_name:
        get_info = lps4_careerData.get_count_by_short_name(short_name)
        if get_info.is_error():
            log.warn("get count by short_name failed.")
            return JsonResponse(dict(is_had=is_had, status="failed", msg=u'获取课程简称信息失败！'))
        count = get_info.result()["count"]
        get_id = get_info.result()["id"]
        if count > 0:
            is_had = False if count == 1 and get_id == _id and action == "revise" else True
        return JsonResponse(dict(is_had=is_had, status="success"))
    return JsonResponse(dict(is_had=is_had, status="failed", msg=u'课程简称不能为空！'))


def get_career_by_id(request, career_id):
    careerdata = lps4_careerData.career_data(career_id)
    if careerdata.is_error():
        return render(request, "404.html", dict(message=u'获取课程信息失败！'))
    career = careerdata.result()
    return career


def get_lps4_career_course():
    APIResult = lps4_careerData.get_all_lps4_career()
    if APIResult.is_error():
        log.warn('get all lps4 career course failed.')
        raise Http404
    career_list = APIResult.result()
    return career_list
