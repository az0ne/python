# -*- coding: utf-8 -*-
"""
@version: 2016/5/17 0017
@author: zhangyunrui
@contact: david.zhang@maiziedu.com
@file: views.py
@time: 2016/5/17 0017 10:48
@note:  教务端第三方可见VIEWS
"""
from django.shortcuts import get_object_or_404, render
from mz_user.models import UserProfile
from ..base.seo import get_seo_info


def public_homepage(request, user_id):
    """
    公开的 教务面板
    :param request:
    :param user_id: 被查看用户id(int)
    :return:
    """
    # 第三方的登陆用户和网页头部用户不一样
    head_user = get_object_or_404(UserProfile, id=user_id)
    seo = get_seo_info(head_user)
    return render(request, 'mz_usercenter/eduadmin/pubulic_homepage.html', locals())
