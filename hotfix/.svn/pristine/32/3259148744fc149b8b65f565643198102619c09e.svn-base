# -*- coding: utf-8 -*-
"""
@version: 2016/5/17 0017
@author: zhangyunrui
@contact: david.zhang@maiziedu.com
@file: views.py
@time: 2016/5/17 0017 10:48
@note:  教务端自己可见VIEWS
"""
from django.shortcuts import render
from mz_common.decorators import eduadmin_required
from mz_usercenter.base.context import get_usercenter_context
from mz_usercenter.eduadmin.interface import EduAdminOverview


@eduadmin_required
def view_index(request):
    """
    教务面板
    :param request:
    :return:
    """
    user_id = request.user.id
    edu_info = EduAdminOverview.get_info(user_id)

    return render(request, 'mz_usercenter/eduadmin/homepage.html', locals(),
                  context_instance=get_usercenter_context(request))
