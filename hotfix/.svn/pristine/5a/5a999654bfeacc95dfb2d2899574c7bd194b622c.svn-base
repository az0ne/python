# -*- coding: utf-8 -*-

__author__ = 'Jackie'

"""
当前任务还剩不到一天时，进行短信提醒：
亲爱的同学，您还剩不到1天时间可完成当前任务“任务名称”啦，
快抓紧时间学习吧！若因故不能正常安排学习，请及时联系您的班主任申请休学哦。【麦子学院】

1.找出当前正在进行的LPS3.0的班级
2.找出班级中

"""

import djevn

djevn.load()

import datetime
from django.conf import settings
from mz_common.mz_log2mongo import MzL2M
from utils.sms_manager import send_sms, get_templates_id

from mz_lps.models import Class
from mz_lps3.functions import get_student_doing_tasks_timeleft

logger = MzL2M.getLogger("mongodb_logger")


def send_message(mobile, task_name):
    try:
        send_sms.delay(settings.SMS_APIKEY, get_templates_id('studying_reminder'),
                 mobile.encode('utf8'), task_name.encode('utf8'))
    except Exception, e:
        logger.error(e)


def main():
    objs = Class.objects.xall().filter(
        lps_version='3.0', class_type=Class.CLASS_TYPE_NORMAL,
        is_active=True, status=1, meeting_enabled=True)
    classes = list()
    for cls in objs:
        meeting_finish = cls.meeting_start + datetime.timedelta(days=(cls.meeting_duration or 1))
        if meeting_finish > datetime.datetime.now():  # 班会未结束
            classes.append(cls)
    for cls in classes:
        assert isinstance(cls, Class)
        for cstudent in cls.classstudents_set.all().filter(is_pause=False):
            if not cstudent.is_active:
                continue
            student = cstudent.user
            if not student.mobile:  # 未登记手机号
                continue
            results = get_student_doing_tasks_timeleft(cls.id, cstudent.user_id)
            print results
            for result in results:
                if 0 <= result['timeleft'] <= 24 * 60 * 60:  # task not expired and left time no more than 24h
                    send_message(student.mobile, result['task_name'])
                    break


if __name__ == "__main__":
    main()
