# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maiziedu_website.settings.local')
import django

django.setup()

import db.api.course.course_task
import db.api.lps.student
import db.api.lps.lps_index
from mz_lps4.class_dict import NORMAL_CLASS_DICT


def get_user_study_version(user_id):
    """
    获取用户的付费类型
    :param user_id:
    :return:
    """
    _is_lps4 = db.api.lps.lps_index.get_lps_3_1_student(user_id)
    if _is_lps4.is_error():
        is_lps4 = False
    else:
        is_lps4 = _is_lps4.result()

    _is_lps3 = db.api.lps.lps_index.get_lps_3_student(user_id, NORMAL_CLASS_DICT.values())
    if _is_lps3.is_error():
        is_lps3 = False
    else:
        is_lps3 = _is_lps3.result()

    pay_type = u'付费用户'
    if is_lps4 and is_lps3:
        user_type = 'lps3|lps4'
    elif is_lps3:
        user_type = 'lps3'
    elif is_lps4:
        user_type = 'lps4'
    else:
        user_type = u'未报班'
        pay_type = u'普通用户'

    return dict(
        pay_type=pay_type,
        user_type=user_type
    )

if __name__ == '__main__':
    get_user_study_version(90637)