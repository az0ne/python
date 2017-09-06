# -*- coding: utf-8 -*-

"""
@version: 2016/4/18
@author: Jackie
@contact: jackie@maiziedu.com
@file: student_status_monitor.py
@time: 2016/4/18 17:05
@note:  ??
"""

import djevn

djevn.load()

from mz_lps.models import ClassStudents, Class
from mz_eduadmin.students.interface import student_quit_class
from django.conf import settings
from utils.sms_manager import send_sms, get_templates_id


def send_message(mobile, user_name, class_code):
    try:
        send_sms.delay(settings.SMS_APIKEY, get_templates_id('student_deadline_quit'),
                       mobile, user_name.encode('utf-8'), class_code.encode('utf-8'))
    except Exception, e:
        print e


def main():
    objs = ClassStudents.objects.filter(
        student_class__lps_version='3.0',
        student_class__class_type=Class.CLASS_TYPE_NORMAL,
        student_class__meeting_enabled=True,
        status=ClassStudents.STATUS_NORMAL
    ).exclude(
        deadline=None
    )
    for cstudent in objs:
        if cstudent.is_overdue:
            student_quit_class(cstudent.student_class_id, cstudent.user_id, 1, u'试学到期未续费,系统自动退班')
            if cstudent.user.valid_mobile:
                send_message(cstudent.user.mobile, cstudent.user.real_name, cstudent.student_class.coding)


if __name__ == "__main__":
    main()
