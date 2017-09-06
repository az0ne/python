# -*- coding: utf-8 -*-

import time,datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse ,HttpResponsePermanentRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password

from utils.decorators import dec_login_required
from utils.handle_exception import handle_http_response_exception
from utils.tool import get_param_by_request,get_back_url
from utils.logger import logger as log
import db.api.fxsys.rebatetype
import db.api.fxsys.user
import db.api.fxsys.new_asset
from mz_fxsys import user_api
from myproject import settings
from calc_fxsys_data import update_liveness_by_userinfo,calc_frozen_rebate


@dec_login_required
@handle_http_response_exception(501)
def add_user(request):
    """增加"""
    username = get_param_by_request(request.POST, 'username', '', str)
    password = make_password(get_param_by_request(request.POST, 'password', '123456', str))
    full_name = get_param_by_request(request.POST, 'full_name', '', str)
    ID_card_No = get_param_by_request(request.POST, 'ID_card_No', '', str)
    contract_num = get_param_by_request(request.POST, 'contract_num', '', str)
    enterprise_name = get_param_by_request(request.POST, 'enterprise_name', '', str)
    type_id = get_param_by_request(request.POST, 'type_id', 0, int)
    role_id = get_param_by_request(request.POST, 'role_id', 0, int)
    parent_id = get_param_by_request(request.POST, 'parent_id', 0, int)
    activate_date = get_param_by_request(request.POST, 'activate_date', '', str)
    rebate_type_id = get_param_by_request(request.POST, 'rebate_type_id', 0, int)
    maiziedu_id = get_param_by_request(request.POST, 'maiziedu_id', '', str)
    fxsys_note = get_param_by_request(request.POST, 'fxsys_note', '', str)

    cash_back_way = get_param_by_request(request.POST, 'cash_back_way', 0, int)
    cash_back_maximum = get_param_by_request(request.POST, 'cash_back_maximum', 0, int)
    cash_back_day = get_param_by_request(request.POST, 'cash_back_day', '0', str)

    print cash_back_way
    print cash_back_maximum
    print cash_back_day
    print fxsys_note

    result = db.api.fxsys.user.is_exits_maizi_user(maiziedu_id)
    if result.is_error():
        log.info('is_exits_maizi_user is error maiziedu_id:{0}'.format(maiziedu_id))
    if not result.result():
        return HttpResponsePermanentRedirect(reverse("mz_fxsys:add_user"))

    maiziedu_id = result.result()[0].get('id')
    if type_id == 2:  # 用户类型为合作伙伴时，角色ID设置为0
        role_id = 0
    grandparent_id = (parent_id == 0 and [0] or [get_grandparent_id_by_parent_id(parent_id)])[0]

    user = user_api.insert_user(username, password, full_name, ID_card_No, contract_num, enterprise_name, type_id,
                                role_id, parent_id, grandparent_id, activate_date, rebate_type_id, maiziedu_id, fxsys_note, cash_back_way, cash_back_maximum, cash_back_day)
    if user.is_error():
        log.info("insert user data failed!")
    else:
        log.info('{username},新增{fxsys_username}用户.--三级分销系统'.format(
            username=request.session.get('username', ''), fxsys_username=username))
        users = user_api.get_user_by_username(username)
        if not users.is_error():
            result = db.api.fxsys.new_asset.add_new_asset(users.result()[0]['id'])
            if result.is_error():
                log.warn("add_new_asset is error user_id:{0}".format(users.result()[0]['id']))
        return HttpResponseRedirect(reverse('mz_fxsys:get_user'))


@dec_login_required
@handle_http_response_exception(501)
def get_user_list(request):
    """查询"""
    user_id = get_param_by_request(request.GET, 'user_id', 0, int)
    action = get_param_by_request(request.GET, 'action', 'search', str)
    type_id = get_param_by_request(request.GET, 'type_id', 0, int)
    role_id = get_param_by_request(request.GET, 'role_id', 0, int)
    user_name = get_param_by_request(request.GET, 'user_name', "", str)
    page_index = get_param_by_request(request.GET, 'page_index', 1, int)
    fxsys_note = get_param_by_request(request.GET, 'fxsys_note', "", str)

    # tool.count_award()

    if user_id != 0:
        user = user_api.select_user_by_id(user_id)
        rebate_types = db.api.fxsys.rebatetype.list_rebate_type()
        if not user.is_error() and not rebate_types.is_error():
            log.info('{username},查看了{fxsys_username}用户信息.--三级分销系统'.format(
                username=request.session.get('username', ''), fxsys_username=user.result()['username']))
            user_info = user.result()
            user_info['maiziedu_name'] =user_info["mobile"] or user_info["email"]
            data = {'user': user_info, 'rebate_types': rebate_types.result(), 'action': action, 'page_index': page_index}

            return render(request, 'mz_fxsys/user_edit.html', data)

    if user_id == 0:
        if action == "add":
            rebate_types = db.api.fxsys.rebatetype.list_rebate_type()
            if rebate_types.is_error():
                log.warn('list_rebate_type is error')
            return render(request, 'mz_fxsys/user_edit.html', {'action': action, 'rebate_types': rebate_types.result()})

        if action == "search":
            user = user_api.select_user_by_page(page_index, settings.PAGE_SIZE, type_id, role_id, user_name)
            if not user.is_error():
                log.info('{username},查看了用户数据.--三级分销系统'.format(username=request.session.get('username', '')))
            data = {
                "users": user.result()['result'],
                "type_id": type_id,
                "role_id": role_id,
                "user_name": user_name,
                "page": {
                    "page_index": page_index, "rows_count": user.result()['rows_count'],
                    "page_size": settings.PAGE_SIZE, "page_count": user.result()['page_count']
                },
            }
            return render(request, 'mz_fxsys/user_list.html', data)


@dec_login_required
@handle_http_response_exception(501)
def del_user(request):
    """删除"""
    user_id = get_param_by_request(request.GET, 'id', 0, int)
    username = get_param_by_request(request.GET, 'uname', '', str)
    user = user_api.del_user(user_id).result()
    if user:
        log.info('{username},已删除{fxsys_username}用户.--三级分销系统'.format(
            username=request.session.get('username', ''), fxsys_username=username))
        return HttpResponseRedirect(reverse('mz_fxsys:get_user'))
    else:
        log.info("delect user by user_id! user_id:%s", (user_id,))


@dec_login_required
@handle_http_response_exception(501)
def update_user(request):
    """修改"""
    user_id = get_param_by_request(request.GET, 'uid', 0, int)
    username = get_param_by_request(request.POST, 'username', '', str)
    full_name = get_param_by_request(request.POST, 'full_name', '', str)
    ID_card_No = get_param_by_request(request.POST, 'ID_card_No', '', str)
    contract_num = get_param_by_request(request.POST, 'contract_num', '', str)
    enterprise_name = get_param_by_request(request.POST, 'enterprise_name', '', str)
    # type_id = get_param_by_request(request.POST, 'type_id', 0, int)
    role_id = get_param_by_request(request.POST, 'role_id', 0, int)
    # parent_id = get_param_by_request(request.POST, 'parent_id', 0, int)
    activate_date = get_param_by_request(request.POST, 'activate_date', '', str)
    rebate_type_id = get_param_by_request(request.POST, 'rebate_type_id', 0, int)
    maiziedu_id = get_param_by_request(request.POST, 'maiziedu_id', '', str)
    page_index = get_param_by_request(request.GET, 'page_index', 1, int)
    # grandparent_id = get_grandparent_id_by_parent_id(parent_id)
    is_suspend = get_param_by_request(request.POST, 'is_suspend', 0, int)
    is_graduate = get_param_by_request(request.POST, 'is_graduate', 0, int)
    is_suspend_old = get_param_by_request(request.POST, 'is_suspend_old', 0, int)
    fxsys_note = get_param_by_request(request.POST, 'fxsys_note', '', str)

    cash_back_way = get_param_by_request(request.POST, 'cash_back_way', 0, int)
    cash_back_maximum = get_param_by_request(request.POST, 'cash_back_maximum', 0, int)
    cash_back_day = get_param_by_request(request.POST, 'cash_back_day', '0', str)

    if maiziedu_id == '':
        return HttpResponseRedirect(get_back_url(request, reverse('mz_fxsys:get_user')))
    result = db.api.fxsys.user.is_exits_maizi_user(maiziedu_id)
    if result.is_error():
        log.info('is_exits_maizi_user is error maiziedu_id:{0}'.format(maiziedu_id))
    if not result.result():
        return HttpResponseRedirect(get_back_url(request, reverse('mz_fxsys:get_user')+"?page_index="+str(page_index)))
    maiziedu_id = result.result()[0].get('id')
    # 变更为未休学，重新填写激活周期
    if is_suspend_old == 1 and is_suspend == 0:
        activate_date = (datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    user = user_api.update_user(user_id, full_name, ID_card_No, contract_num, enterprise_name, role_id, activate_date,
                                rebate_type_id, maiziedu_id, is_suspend, is_graduate, fxsys_note, cash_back_way, cash_back_maximum, cash_back_day)

    if not user.is_error():
        # 变更为已休学，立即结算积分和冻结
        if is_suspend == 1 and is_suspend_old == 0:
            userresult = db.api.fxsys.user.get_fxsys_user_by_id(user_id)
            update_liveness_by_userinfo(userresult.result(), is_settlement=True, prompt_settlement=True)
            calc_frozen_rebate()

        log.info('{username},修改了{fxsys_username}用户.--三级分销系统'.format(
            username=request.session.get('username', ''), fxsys_username=username))
        db.api.fxsys.new_asset.add_new_asset(user_id)
        return HttpResponseRedirect(reverse('mz_fxsys:get_user')+"?page_index="+str(page_index))


@dec_login_required
def update_activate(request):
    """更改用户激活日期"""
    user_id = get_param_by_request(request.GET, 'id', 0, int)
    username = get_param_by_request(request.GET, 'uname', '', str)
    update_status = user_api.update_activate_date_by_userId(user_id)
    if not update_status.is_error():
        log.info('{username},更新了{fxsys_username}的激活时间。激活时间:{date}--三级分销系统'.format(
            username=request.session.get('username', ''), fxsys_username=username,
            date=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())))
        return HttpResponseRedirect(reverse('mz_fxsys:get_user'))


@dec_login_required
def get_all_user(request):
    """获取所有用户名和姓名"""
    users = user_api.get_all_user()
    if users.is_error():
        result = ''
    else:
        data = {'result': users.result()}

    return JsonResponse(data)


def get_grandparent_id_by_parent_id(parent_id):
    """根据父级ID，来查询爷级ID"""
    grandparent_id = 0
    user = user_api.select_user_by_id(parent_id)
    if not user.is_error():
        if user.result():
            grandparent_id = int(user.result()['parent_id'])
    return grandparent_id

#
# def delect_payments_by_user_id(user_id):
#     """根据用户ID删除该用户的收支明细信息"""
#     payments_info = payments_api.select_payments_by_user_id(user_id)
#     if not payments_info.is_error():
#         if payments_info.result():
#             for p in payments_info.result():
#                 payments_api.delect_payments_by_user_id(p['id'])

#
# def update_user_role_relation(user_id):
#     """刪除用户后，更新用户关系"""
#     users = user_api.get_user_role_by_parent(user_id)
#     if not users.is_error():
#         if users.result():
#             for u in users.result():
#                 if int(u['parent_id']) == user_id:
#                     if int(u['grandparent_id']) != 0:
#                         parent_id = get_grandparent_id_by_parent_id(u['grandparent_id'])
#                         user_api.update_user_role_relation(u['id'], parent_id=u['grandparent_id'],
#                                                            grandparent_id=str(parent_id))
#                     else:
#                         user_api.update_user_role_relation(u['id'], parent_id='0')
#                 if int(u['grandparent_id']) == user_id:
#                     parent_id = get_grandparent_id_by_parent_id(u['parent_id'])
#                     user_api.update_user_role_relation(u['id'], grandparent_id=str(parent_id))


def get_user_parentId_by_userId(user_id):
    """获取父级ID"""
    parent_id = 0
    user = user_api.select_user_by_id(user_id)
    if not user.is_error():
        if user.result():
            parent_id = user.result()['parent_id']
    return parent_id


@dec_login_required
def validate_user_exist_by_username(request):
    """验证用户是否存在"""
    # username = get_param_by_request(request.GET, 'uname', '', str)
    # user = user_api.validate_user_exist_by_username(username)
    # if user.is_error():
    #     log.warn('validate user exist failed. '
    #              'username: {0}'.format(username))
    #     user = False
    # else:
    #     user = user.result()

    user_list = []
    users = user_api.get_all_user()
    if not users.is_error():
        if len(users.result()) > 0:
            for u in users.result():
                user_list.append(u['username'])
    data = {'result': user_list}
    return JsonResponse(data)
