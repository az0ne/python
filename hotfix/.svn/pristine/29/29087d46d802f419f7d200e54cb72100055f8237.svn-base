# coding: utf-8
from django.http.response import Http404
from utils.logger import logger as log

import db.api.usercenter.resume


def list_user_edu_interface(user_id):
    """

    :param user_id:
    :return:
    """
    ret_user_edu = db.api.usercenter.resume.list_user_edu(user_id)
    if ret_user_edu.is_error():
        log.warn('list_user_edu is error,user_id is %s' % user_id)
        raise Http404
    else:
        ret_user_edu = ret_user_edu.result()

    return ret_user_edu


def list_user_work_interface(user_id):
    """

    :param user_id:
    :return:
    """
    ret_user_work = db.api.usercenter.resume.list_user_work(user_id)
    if ret_user_work.is_error():
        log.warn('list_user_work is error,user_id is %s' % user_id)
        raise Http404
    else:
        ret_user_edu = ret_user_work.result()

    return ret_user_edu


def get_resume_user_info_interface(user_id):
    """

    :param user_id:
    :return:
    """
    ret_user_info = db.api.usercenter.resume.get_user_info(user_id)
    if ret_user_info.is_error():
        log.warn('get_user_info is error,user_id is %s' % user_id)
        raise Http404
    else:
        ret_user_info = ret_user_info.result()

    return ret_user_info


def get_user_class_info_interface(user_id):
    """

    :param user_id:
    :return:
    """
    ret_user_class_info = db.api.usercenter.resume.get_user_class_info(user_id)
    if ret_user_class_info.is_error():
        log.warn('get_user_class_info is error,user_id is %s' % user_id)
        raise Http404
    else:
        ret_user_class_info = ret_user_class_info.result()

    return ret_user_class_info
