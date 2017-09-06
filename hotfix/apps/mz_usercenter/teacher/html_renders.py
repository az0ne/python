# -*- coding: utf-8 -*-

"""
@version: 2016/5/27
@author: Jackie
@contact: jackie@maiziedu.com
@file: html_renders.py
@time: 2016/5/27 16:06
@note:  ??
"""


from django.template.loader import render_to_string
from django.conf import settings


def get_teacher_intro_html(teacher_id):
    """老师简介及作品页"""
    if teacher_id in (3287, 3472, 684, 40986, 48129, 4, 136574, 36413, 20365):
        return render_to_string('mz_usercenter/teacher/intros/%s.html' % teacher_id,
                                {'STATIC_URL': settings.STATIC_URL})
    return ''
