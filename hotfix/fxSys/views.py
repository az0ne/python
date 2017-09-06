# -*- coding:utf-8 -*-

import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password, make_password

import db.api.fxsys.index
from core.common.http.response import success_json,failed_json
from utils.tool import get_param_by_request
from utils.logger import logger as log
from mz_common.functions import paginater
from fxSys import api



def login(request):
    """登录"""
    if request.method == 'GET':
        return render(request, 'mz_fxSys/login.html', {})
    else:
        username = get_param_by_request(request.POST, 'username', 0, int)
        password = get_param_by_request(request.POST, 'password', '', str)
        if 'username' and 'password' in request.POST:
            user_info = api.get_user_info_by_username(username).result()
            if not user_info:
                log.info("login failed!")
                return render(request, 'mz_fxSys/login.html', {'error': '该用户不存在，请检查后重新输入!'})

            if not check_password(password, user_info['password']):
                log.info("password failed!")
                return render(request, 'mz_fxSys/login.html', {'error': '密码错误请重新输入！', 'username': username})
            request.session['full_name'] = user_info['full_name']
        api.update_last_login_time_by_userId(user_info['id'])  # 更新登录时间
        request.session['last_login'] = str(user_info['last_login'])
        request.session['username'] = username

        request.session['userId'] = user_info['id']
        return HttpResponseRedirect('/fxsys/index/')


def index(request):
    """主页"""
    session_name = request.session.get('username')

    if session_name is None:
        return HttpResponseRedirect(reverse('fxsys:login'))
    else:
        page_index = get_param_by_request(request.GET, "page_index", 1, int)
        start_date = get_param_by_request(request.POST, 'start_date', '', str)
        end_date = get_param_by_request(request.POST, 'end_date', '', str)
        user_info = api.get_user_info_by_username(session_name).result()
        user_id = user_info["id"]
        rebate_rl = db.api.fxsys.index.get_rebate_no_by_user_id(user_id)
        result_asset = db.api.fxsys.index.get_new_asset_by_user_id(user_id)
        payments = api.get_payments_by_user_id_and_page(user_id, start_date, end_date, page_index)

        # 没有通知
        is_notify_rl = db.api.fxsys.index.is_notify_liveness_record_by_user_id(user_id)
        if is_notify_rl.is_error():
            log.warn("is_notify_liveness_record_by_user_id is error user_id:{0}".format(user_id))
        liveness_record = is_notify_rl.result()
        # 分页
        page_count_list = 0
        payments_dict = {}
        if not result_asset.is_error():
            if not payments.is_error():
                if payments.result():
                    payments_dict = payments.result()['payments']
                    page_count_list, page_index, start_index, end_index = paginater(page_index, 10,
                                                                                    payments.result()['rows_counts'], 2)
                if user_info.has_key('activate_date'):
                    now_date = datetime.datetime.now()
                    end_time = api.cycle_liveness(user_info.get('activate_date'), now_date)[1]
                    statement_days = (end_time - now_date).days
                else:
                    statement_days = '未知'
                # 判断资产表的更新时间是否是昨天
                if result_asset.result():
                    if result_asset.result()["update_date"].date() != (datetime.datetime.now()-datetime.timedelta(days=1)).date():
                        result_asset.result()["yesterday_rebate"] = 0
                if rebate_rl.is_error():
                    log.warn("get_rebate_no_by_user_id is error user_id:{0}".format(user_info["id"]))
                    rebate_no = None
                else:
                    rebate_no = rebate_rl.result()

                data = {"user": user_info, "asset": result_asset.result(), "rebate_no": rebate_no,
                        'statement_days': statement_days, "liveness_record": liveness_record,
                        "payments": payments_dict, "start_date": start_date, "end_date": end_date,
                        "page_count_list": page_count_list, "page_index": page_index, 'url': '/fxsys/index/?'}

                return render(request, 'mz_fxSys/index.html', data)


def logout(request):
    """退出登录"""
    if 'username' in request.session:
        del request.session['username']
    return HttpResponseRedirect(reverse('fxsys:login'))


def close_liveness_notify(request):
    """
     关闭周期活跃度的通知
     :param request:
     :return:
    """
    session_name = request.session.get('username')
    if session_name is None:
        return HttpResponseRedirect(reverse('fxsys:login'))
    else:
        user_info = api.get_user_info_by_username(session_name).result()
        user_id = user_info["id"]
    result = db.api.fxsys.index.update_is_notify(user_id)
    if result.is_error():
        log.warn("update_is_notify is error user_id:{0}".format(user_id))

    return JsonResponse(data=dict(result=True))


def test(request):
    return render(request, 'mz_fxSys/index.html', {})


def register(request):
    user = request.POST.get('username')
    pwd = request.POST.get('password')
    pwd = make_password(pwd)
    register_result = api.insert_user(user, pwd).result()
    if register_result:
        return render(request, 'mz_fxSys/login.html', {'error': 'success'})
    else:
        return render(request, 'mz_fxSys/login.html', {'error': 'failed'})


def rules(request):
    return render(request, 'mz_fxSys/rules.html', {})


def score_record(request):
    user_id = request.session['userId']
    session_name = request.session.get('username')
    if user_id is None:
        return HttpResponseRedirect(reverse('fxsys:login'))
    user_info = api.get_user_info_by_username(session_name).result()
    now_date = datetime.datetime.now()
    start_time, end_time = api.cycle_liveness(user_info.get('activate_date'), now_date)
    liveness_result = db.api.fxsys.index.get_liveness_infos(user_id, start_time, end_time)
    if liveness_result.is_error():
        log.warn("get_liveness_info_dict is error user_id:{0}".format(user_id))
    liveness_infos = liveness_result.result()
    result = db.api.fxsys.index.get_liveness_info_dict(user_id)
    if result.is_error():
        log.warn("get_liveness_info_dict is error user_id:{0}".format(user_id))
    data = result.result()
    data['liveness_infos'] = liveness_infos
    data["user"] = user_info
    return render(request, 'mz_fxSys/scholarship.html', data)


def score_record_more(request):
    user_id = request.session['userId']
    if user_id is None:
        return HttpResponseRedirect(reverse('fxsys:login'))
    if request.method == 'POST':
        last_id = get_param_by_request(request.POST, 'last_id', 0, int)
        last_key = get_param_by_request(request.POST, 'last_key', "").strip()
        result = db.api.fxsys.index.get_liveness_info_dict(user_id, last_id=last_id)
        if result.is_error():
            log.warn("get_liveness_info_dict is error user_id:{0}".format(user_id))
            return failed_json(u"数据出错")
        data = result.result()
        sub_liveness_info_list = data.get("liveness_info_dict").pop(last_key, [])
        data.setdefault('sub_liveness_info_list', sub_liveness_info_list)
        html = render(request, 'mz_fxSys/scholarship_page.html', data).content
        return success_json({"html": html, "last_id": data["last_id"]})
