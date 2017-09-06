# -*- coding: utf-8 -*-
"""
@version: 2016/5/10
@author: Jackie
@contact: jackie@maiziedu.com
@file: views.py
@time: 2016/5/10 17:09
@note:  ??
"""
import interface
from django.shortcuts import redirect, render
from django.http import Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from mz_user.interface import UserBaseInterface, CommonDataInterface
from core.common.http.response import success_json, failed_json
from mz_user.models import UserProfile
from mz_user.views import user_center_third
from mz_usercenter.base.context import get_usercenter_context
from mz_usercenter.student.interface_record import first_signup_recommend
from utils.message_queue import mq_service
from utils.logger import logger as log


@login_required(login_url="/")
def view_base(request):
    """
    基本信息
    :param request:
    :return:
    """
    user = request.user
    if request.method == 'GET':

        if user.is_edu_admin():
            return render(request, 'mz_usercenter/eduadmin/base_info.html', locals(),
                          context_instance=get_usercenter_context(request))
        elif user.is_teacher():
            return render(request, 'mz_usercenter/teacher/base_info.html', locals(),
                          context_instance=get_usercenter_context(request))
        elif user.is_student():
            # 新注册用户推荐课程弹窗
            recommend_careers = first_signup_recommend(user)

            province_list = CommonDataInterface.get_provinces()
            if user.city:
                user_province_id = user.city.province_id
                city_list = CommonDataInterface.get_cities_by_province_id(
                    user_province_id, cache_pk=user_province_id)
                user_city_id = user.city_id
            else:
                user_province_id = province_list[0][0]
                city_list = CommonDataInterface.get_cities_by_province_id(
                    user_province_id, cache_pk=user_province_id)
                user_city_id = city_list[0].get('city_id')
            user_gender = user.gender or UserProfile.GENDER_MALE
            gender_list = UserProfile.GENDERS.items()
            # 如果用户加入就业班级需要填写省份证
            is_join_job_class = interface.is_join_job_class_valid(user.id)
            # 是否是入流程（完善个人资料）guotao
            class_id = request.GET.get('class')
            is_perfected_userinfo = False
            if class_id and interface.is_joinclass_valid(user.id, class_id):
                is_perfected_userinfo = True
            birthday = user.birthday.strftime("%Y-%m-%d") if user.birthday else '1990-01-01'
            return render(request, 'mz_usercenter/student/base_info.html', locals(),
                          context_instance=get_usercenter_context(request))
        else:
            raise Http404

    elif request.method == 'POST':
        # 个人信息保存
        user = request.user

        mapping = [('nick_name', 'nick_name'), ('real_name', 'real_name'), ('id_number', 'id_number'),
                   ('gender', 'gender'), ('address', 'address'), ('qq', 'qq'), ('city_id', 'city'),
                   ('birthday', 'birthday'), ('teach_feature', 'teach_feature'), ('description', 'description'),
                   ('wechat', 'wechat')]
        kwargs = dict()
        for k, v in mapping:
            kwargs[k] = request.POST.get(v)
        bool_result, result = UserBaseInterface(user_object=user).update_profile(**kwargs)
        if not bool_result:
            return failed_json(result)
        # 消息队列
        r = mq_service.publish({
            "event": "user_study_info_sync",
            "data": {
                "user_id": user.id,
                "nick_name": request.POST.get('nick_name'),
                "qq": request.POST.get('qq'),
                "mobile": user.mobile,
                "wechat": request.POST.get('wechat')
            }
        })
        log.info('mq_user_study_info_sync: %s' % str(r))
        # 入学流程的跳转,,,,class参数传递
        source_url = request.META['HTTP_REFERER']
        import re
        _res = re.search(r'class=(?P<class_id>\d+)', source_url)
        if _res:
            class_id = _res.groupdict().get('class_id')
            if class_id:
                return success_json(next_url=reverse('home:student:study_info') + '?class=%s' % class_id)

        return success_json()


@login_required(login_url="/")
def view_settings(request):
    """
    账号设置
    :param request:
    :return:
    """
    user = request.user

    # 第三方绑定
    partner = request.GET.get('partner')
    openid = request.GET.get('openid')
    if partner and openid:
        user_center_third(partner, openid, user.id)
        return redirect(reverse('home:settings:index'))

    third = UserBaseInterface(user_object=user).get_osite_accounts()

    return render(request, 'mz_usercenter/base/setting.html', locals(),
                  context_instance=get_usercenter_context(request))


@login_required(login_url="/")
def get_my_base_info(request):
    """
    异步获取自己的一些基础信息,例如手机号,邮箱
    :param request:
    :return:
    """
    user = request.user
    data = dict(
        mobile=user.mobile if user.mobile else '',
        email=user.email if user.email else ''
    )
    return success_json(data)


# 根据省份查城市
@login_required(login_url="/")
def get_city_list(request, province_id):
    city_list = CommonDataInterface.get_cities_by_province_id(province_id, cache_pk=province_id)
    return success_json({'list': city_list})


