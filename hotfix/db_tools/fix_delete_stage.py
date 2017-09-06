# -*- coding: utf-8 -*-
__author__ = 'qxoo'
'''
修复课程阶段的试学阶段被删除后，用户的 unlockstage 数据丢失，导致部分功能不能正常使用，如上传项目制作
'''

import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"/..")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")

import django

django.setup()


from mz_lps.models import ClassStudents, Class
from mz_user.models import UserUnlockStage
from mz_course.models import Stage
from mz_pay.models import UserPurchase


def get_user_unlockstage(careercourse, user):
    stage_list = Stage.objects.filter(career_course=careercourse)
    user_stage_count = UserUnlockStage.objects.filter(stage__career_course=careercourse, user=user).count()
    result_stage_list = []
    if user_stage_count < stage_list.count() and user_stage_count == 0:
        if UserPurchase.objects.filter(user=user, pay_careercourse=careercourse, pay_type=0, pay_status=1).count():
            return result_stage_list
        if UserPurchase.objects.filter(user=user, pay_careercourse=careercourse, pay_type=1, pay_status=1).count():
            for stage in stage_list:
                if stage.is_try:
                    result_stage_list.append(stage)
    return result_stage_list


def re_unlock_user_stage(user_stage_list, user):
    for stage in user_stage_list:
        UserUnlockStage.objects.get_or_create(user=user, stage_id=stage.id)
        # pass


def get_all_user():
    return ClassStudents.objects.filter(student_class__class_type=Class.CLASS_TYPE_NORMAL)


def main():
    print 'log : %s ' % pwd + '../log/fix_delete_stage_log.log'
    fl = open(pwd + '/../log/fix_delete_stage_log.log', 'wa')

    class_student_list = get_all_user()
    for class_student in class_student_list:
        user_stage_list = get_user_unlockstage(class_student.student_class.career_course, class_student.user)
        if user_stage_list:
            print 'user: %s , careercourse_name: %s , careercourse_id: %s' %\
                  (class_student.user.id,
                   class_student.student_class.career_course.name,
                   class_student.student_class.career_course.id)
            fl.write('user: %s , careercourse_name: %s , careercourse_id: %s' %
                     (class_student.user.id,
                      class_student.student_class.career_course.name,
                      class_student.student_class.career_course.id))
            fl.write('\n')
            re_unlock_user_stage(user_stage_list, class_student.user)
            # break

    fl.close()


if __name__ == '__main__':
    main()