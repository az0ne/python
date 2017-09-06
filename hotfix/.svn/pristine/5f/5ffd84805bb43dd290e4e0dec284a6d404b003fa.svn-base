# -*- coding: utf-8 -*-

import datetime
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http.response import Http404
from django.template.context import RequestContext

import db.api.lps.student
import db.api.common.new_discuss
import db.api.usercenter.message
from mz_common.user_study_info import UserStudyInfo
from mz_lps4.class_dict import CAREER_ID_TO_SHORT_NAME, NORMAL_CLASS_DICT
from mz_lps4.interface import student_unread_num
from mz_usercenter.student.interface_resume import list_user_work_interface, list_user_edu_interface, \
    get_resume_user_info_interface

from utils.logger import logger as log


def get_menus(menus, menus_count={}):
    """
    获取所以的项
    :param menus_count: 需要显示的数量
    :return:
    """
    result = list()
    for m in menus:
        if menus_count.has_key(m['alias']):
            m['count'] = menus_count.get(m['alias'])
        result.append(m)
    return result


def get_cur_menu(menus, path):
    """
    获取当前的项
    :param path: 路径
    :return:
    """
    for m in menus:
        if path == m['link']:
            return m
    return {}


def get_lps4_context(request, career_id=0):
    """
    获取lps4上下文
    包括  菜单,,user_header
    :param request:
    :return:
    """
    # check career_id is int
    try:
        career_id = int(career_id)
    except ValueError:
        log.warn('career_id is not int %s' % career_id)
    if career_id <= 0:
        log.warn('career_id is not bigger than 0 %s' % career_id)
        raise Http404

    try:
        # get short_name from CAREER_ID_TO_SHORT_NAME by career_id
        short_name = CAREER_ID_TO_SHORT_NAME[career_id]
    except KeyError:
        log.warn('get CAREER_ID_TO_SHORT_NAME %s error' % career_id)
        raise Http404

    MENUS = (
        dict(title=u'LPS', name='', alias='lps4', link=reverse('lps4_index', args=[short_name]), cls='LPS'),
        dict(title=u'辅导', name='辅导', alias='coach', link=reverse('lps4:student_coach_list', args=[career_id]),
             cls='answers'),
        dict(title=u'约课', name='约课', alias='service', link=reverse('lps4:student_service', args=[career_id]),
             cls='one-to-one')
    )

    user = request.user
    menu = get_cur_menu(MENUS, request.path)
    # 针对辅导详情单独处理
    if '/lps4/coach/' in request.path:
        menu = dict(title=u'辅导', name='辅导', alias='coach', link=reverse('lps4:student_coach_list', args=[career_id]),
                    cls='answers')
    menus_count = {}  # 菜单下显示的数量
    is_normal_class = False  # 是否加入正式lps4班级
    end_days_list = list()  # 毕业时间
    is_pop_complete_resume = False  # 是否弹出完善简历
    is_force_pop_complete_resume = False  # 是否强制弹出完善简历
    is_employment_contract = False
    # 登陆用户
    if user and user.id:
        user_id = user.id
        # 学生信息
        student_dict = {}
        student_result = db.api.lps.student.get_lps4_student_info_by_user_id(user_id, career_id)
        if student_result.is_error():
            log.warn(
                'get_lps_3_1_class_id_by_user_id_and_career_id is error. user_id: %s, career_id: %s' % (
                    user_id, career_id))
        else:
            student_dict = student_result.result() or {}

        message_type = ['50', '11', '21', '22']  # 学生展示的消息
        menus_count['lps4'] = db.api.usercenter.message.get_my_message_count(user_id, message_type).result()
        # menus_count['discuss'] = db.api.common.new_discuss.get_user_status_count(user_id).result()

        # 加入了lps4班级
        if student_dict:
            menus_count['coach'] = student_unread_num(career_id, user_id, student_dict.get('teacher_id', 0))
            # 是否加入正式班级
            is_normal_class = False
            if student_dict.get('type') in [0, 1]:
                is_normal_class = True
                # 获取学生字典
                class_id = NORMAL_CLASS_DICT[career_id]
                user_study_info = cache.get('user_study_info_%s_%s_lps4' % (user_id, class_id))
                if not user_study_info:
                    """
                        没有命中用户学习数据缓存
                    """
                    user_study_info = UserStudyInfo(user_id, class_id, career_id).__dict__
                    cache.set('user_study_info_%s_lps4' % user_id, user_study_info, 5 * 60)

                is_employment_contract = user_study_info['is_employment_contract']

                # 离毕业天数
                try:
                    end_days = (user_study_info['end_time'] - datetime.datetime.now()).days
                except Exception as e:
                    log.error('This error raised :%s' % e)
                    raise Http404

                if end_days > 0:
                    end_days_list = list(str(end_days).rjust(3, '0'))
                    user_info = get_resume_user_info_interface(user_id)
                    user_work = list_user_work_interface(user_id)
                    user_edu = list_user_edu_interface(user_id)
                    if not (user_study_info['start_work_time'] and user_info and user_edu and user_work):
                        is_pop_complete_resume = True
                        if end_days <= 7 and (not user_study_info['is_stop']):
                            is_force_pop_complete_resume = True

    return RequestContext(
        request,
        dict(
            MENUS=get_menus(MENUS, menus_count),
            path_alias=menu.get('alias', 'lps4'),
            career_id=career_id,
            is_normal_class=is_normal_class,
            end_days_list=end_days_list,
            seo=dict(seo_title=u"%s - 麦子学院" % (menu.get('title', ''))),
            short_name=short_name,
            is_pop_complete_resume=is_pop_complete_resume,
            is_force_pop_complete_resume=is_force_pop_complete_resume,
            is_employment_contract=is_employment_contract
        )
    )
