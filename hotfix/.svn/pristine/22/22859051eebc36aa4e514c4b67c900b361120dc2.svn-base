# -*- coding: utf-8 -*-

"""
@version: 2016/5/18
@author: Jackie
@contact: jackie@maiziedu.com
@file: menus.py
@time: 2016/5/18 15:25
@note:  ??
"""

from django.core.urlresolvers import reverse


class MenuBase:
    MENUS = []
    MAPPING = {}

    @classmethod
    def get_alias(cls, path):
        path = cls.MAPPING.get(path, path)
        for g in cls.MENUS:
            for m in g:
                if m['link'] == path:
                    return m['alias']

    @classmethod
    def get_menu(cls, path):
        path = cls.MAPPING.get(path, path)
        for g in cls.MENUS:
            for m in g:
                if m['link'] == path:
                    return m

    @classmethod
    def get_menus(cls, menus_permissions={}, menus_count={}):
        """
        获取菜单,两层结构
        :param menus_enabled:   for example {'one_alias':False}  default True
        """
        result = list()
        for g in cls.MENUS:
            _subm = []
            for m in g:
                if menus_count.has_key(m['alias']):
                    m['count'] = menus_count.get(m['alias'])
                if menus_permissions.get(m['alias'], True):
                    _subm.append(m)
            if _subm:
                result.append(_subm)
        return result


class StudentMenu(MenuBase):
    """
    个人中心学生菜单
    """
    MENUS = [  # 学生菜单
        [
            dict(title=u'已报名课程', alias='mycourse', link=reverse('home:student:mycourse'), icon='pcICO2'),
            dict(title=u'免费试学课程', alias='expcourse', link=reverse('home:student:expcourse'), icon='pcICOtry'),
            dict(title=u'我的课程(老版)', alias='omycourse', link=reverse('home:student:omycourse'), icon='pcICO2'),
            dict(title=u'我的问答', alias='mydiscuss', link=reverse('home:student:my_discuss'), icon='pcICOanswer')
        ],
        [
            dict(title=u'基本资料', alias='basicinfo', link=reverse('home:base:index'), icon='pcICO4'),
            dict(title=u'学习信息', alias='studyinfo', link=reverse('home:student:study_info'), icon='pcICO5'),
            dict(title=u'就业信息', alias='jobinfo', link=reverse('home:student:job_info'), icon='pcICO6'),
            dict(title=u'简历信息', alias='resumeinfo', link=reverse('home:student:resume_info'), icon='pcICOruseme'),
            dict(title=u'账号设置', alias='accountset', link=reverse('home:settings:index'), icon='pcICO7')],
        [
            dict(title=u'订单记录', alias='orderinfo', link=reverse('home:student:order_info'), icon='pcICO8')]
    ]

    MAPPING = {reverse('home:index'): reverse('home:student:mycourse')}


class TeacherMenu(MenuBase):
    MENUS = [  # 教师菜单
        [
            dict(title=u'老师个人主页', alias='teacherindex', link=reverse('home:teacher:teacher_index'),
                 icon='pcICO3'), ],
        [
            dict(title=u'进行中班级', alias='processingclasses', link=reverse('home:teacher:processing_classes'),
                 icon='pcICO20'),
            dict(title=u'已毕业班级', alias='graduatedclasses', link=reverse('home:teacher:graduated_classes'),
                 icon='pcICO21'),

            dict(title=u'LPS2班级', alias='oldclasses', link=reverse('home:teacher:old_classes'),
                 icon='pcICO20'),
            dict(title=u'免费试学班', alias='freeclasses', link=reverse('home:teacher:free_classes'),
                     icon='pcICOtry'), ],
        [
            dict(title=u'学生问答', alias='studentdiscuss', link=reverse('home:teacher:student_discuss'),
                 icon='pcICOanswer'),
            dict(title=u'辅导', alias='oneservice', link=reverse('home:teacher:onevone_service'),
                 icon='pcICOonevoneser'),
            dict(title=u'约课', alias='onemeeting', link=reverse('home:teacher:onevone_meeting'),
                 icon='pcICOonevoneline'), ],
        [
            dict(title=u'基本资料', alias='basicinfo', link=reverse('home:base:index'), icon='pcICO4'),
            dict(title=u'账号设置', alias='accountset', link=reverse('home:settings:index'), icon='pcICO7')]
    ]

    MAPPING = {reverse('home:index'): reverse('home:teacher:teacher_index')}


class EduAdminMenu(MenuBase):
    MENUS = [  # 教务菜单
        [
            dict(title=u'教务面板', alias='eduadmin', link=reverse('home:eduadmin:index'), icon='pcICO3'), ],
        [
            dict(title=u'基本资料', alias='basicinfo', link=reverse('home:base:index'), icon='pcICO4'),
            dict(title=u'账号设置', alias='accountset', link=reverse('home:settings:index'), icon='pcICO7')],
    ]

    MAPPING = {reverse('home:index'): reverse('home:eduadmin:index')}
