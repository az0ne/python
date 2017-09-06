# -*- coding: utf8 -*-

import db.api.common.onevone.onevone_ops
from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request
from django.conf import settings
from utils.logger import logger as log
from django.shortcuts import render
from mz_common.common_interface import get_city_name
from mz_common.onevone.onevone_interface import excle_export, get_onevone_data, change_onevone_ops_is_done, \
    change_onevone_ops_is_done_to_1
from django.http import HttpResponse, JsonResponse
import datetime
import json


@dec_login_required
@handle_http_response_exception(501)
def onevone_ops_list(request):
    action = get_param_by_request(request, "action", "query", str)
    page_index = get_param_by_request(request.GET, "page_index", 1, int)
    APIResult = db.api.common.onevone.onevone_ops.list_onevone_ops(page_index=page_index, page_size=settings.PAGE_SIZE)

    if APIResult.is_error():
        log.warn("list onevone ops failed.")
        return render(request, "404.html", {"message": "list onevone ops failed."})
    result = APIResult.result()

    # 获取城市信息
    ops_result = result.get('result', None)
    ops_id_list = list()
    if ops_result:
        for res in ops_result:
            ops_id_list.append(res.get("id"))
            city = get_city_name(request, res.get("city_id", 0))
            if city:
                res["city_name"] = "%s-%s" % (city.get('province_name'), city.get('city_name'))
            else:
                res["city_name"] = None

    c = {"ops": result["result"], "ops_id_list": ops_id_list,
         "page": {"page_index": page_index, "rows_count": result["rows_count"],
                  "page_size": settings.PAGE_SIZE,
                  "page_count": result["page_count"]}}
    return render(request, "mz_common/onevone/onevone_ops.html", c)


@dec_login_required
@handle_http_response_exception(501)
def export_excle(request, data_type):
    page_index = get_param_by_request(request.GET, "page_index", 1, int)
    onevone_ops_data = get_onevone_data(request, data_type, page_index)
    bio = excle_export(onevone_ops_data)
    response = HttpResponse(bio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=1v1预约数据%s.xls' % datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    response['Content-Length'] = len(bio.getvalue())
    return response


@dec_login_required
@handle_http_response_exception(501)
def change_ops_is_done(request):
    obj = get_param_by_request(request.GET, "obj_change", 0, int)  # 如果取到的值为非纯数字字符串，则在int强制转换时报错返回None
    if not obj:
        obj = get_param_by_request(request.GET, "obj_change", "[]", str)
        obj = json.loads(obj)

    if isinstance(obj, list):
        for id in obj:
            change_onevone_ops_is_done_to_1(request, int(id))
    elif isinstance(obj, int):
        change_onevone_ops_is_done(request, int(obj))
    else:
        return JsonResponse(dict(status="failed"))
    return JsonResponse(dict(status="success"))
