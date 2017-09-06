# -*- coding: utf-8 -*-

"""
@version: 2016/5/18
@author: Jackie
@contact: jackie@maiziedu.com
@file: context.py
@time: 2016/5/18 18:18
@note:  ??
"""
from django.template.context import RequestContext
from mz_lps3_free.common.interface import FREE488_TEACHER
import interface


def get_usercenter_context(request):
    """
    获取用户中心上下文
    包括  菜单,,user_header
    :param request:
    :return:
    """
    from .menus import EduAdminMenu, TeacherMenu, StudentMenu

    user = request.user
    menus_permissions = {}
    menus_count = {} #菜单下显示的数量
    if user.is_edu_admin():
        MenuClass = EduAdminMenu

    elif user.is_teacher():
        MenuClass = TeacherMenu
        if user.id not in FREE488_TEACHER.values():
            menus_permissions.update({'freeclasses': False})
        menus_count['studentdiscuss'] = interface.get_discuss_count(user.id)

    elif user.is_student():
        MenuClass = StudentMenu
        if not user.is_paying_subscriber():
            menus_permissions.update({'studyinfo': False, 'orderinfo': False})
        if not user.has_job_intention_info():
            menus_permissions.update({'jobinfo': False, 'resumeinfo': False})
        if not user.is_lps2_user():
            menus_permissions.update({'omycourse': False})
        menus_count['mydiscuss'] = interface.get_discuss_count(user.id)

    menu = MenuClass.get_menu(request.path)
    alias = menu.get('alias') if menu else ''

    return RequestContext(
        request,
        dict(
            MENUS=MenuClass.get_menus(menus_permissions, menus_count),
            path_alias=alias,
            head_user=request.user,
            seo=dict(seo_title=u"个人中心 - %s - 麦子学院" % (menu.get('title') if menu else ''))
        )
    )


# def render(request, *args, **kwargs):
#     kwargs['context_instance'] = get_usercenter_context(request)
#     return shortcuts.render(request, *args, **kwargs)
