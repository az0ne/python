# -*- coding: utf-8 -*-
"""
@version: 2016/5/11
@author: 张云瑞
@contact: david.zhang@maiziedu.com
@file: interface.py
@time: 2016/5/11 9:51
@note:  教务端接口
"""
import datetime
from mz_lps.models import Class, ClassStudents
from mz_eduadmin.students.interface import ClassStudentsInterface


class EduAdminOverview(object):
    """
    教务信息
    """

    @staticmethod
    def get_info(eduadmin_id):
        """
        获取教务班级的信息
        :param eduadmin_id: int
        :return: result = {
            'paused': 休学(int),
            'quit': 退学(int),
            'behind': 落后(int),
            'finish': 已学完(int),
            'normal': 正常(int),
            'total': 总人数(int),
            'classes': {
                (班级id(int), 专业名(unicode): [班级id(int), ...],
                ...
            },
            'total_classes': 班级id总览[班级id(int), ...],
            'today': 今日新增(int),
            'graduate': 毕业(int)
        }
        """
        result = {
            'total': 0, 'today': 0,
            'graduate': 0, 'finish': 0, 'normal': 0, 'paused': 0, 'quit': 0, 'behind': 0,
            'classes': {}
        }

        classes = Class.objects.xall().filter(
            edu_admin_id=eduadmin_id,
            is_active=True,
            lps_version='3.0',
            class_type=Class.CLASS_TYPE_NORMAL
        ).values(
            'id', 'career_course_id', 'career_course__name', 'status'
        )
        total_classes = list()
        for _cls in classes:
            career_course_id = _cls.get('career_course_id')
            career_course_name = _cls.get('career_course__name')
            # classes下按专业分组
            result['classes'].setdefault((career_course_id, career_course_name), [])
            result['classes'][(career_course_id, career_course_name)].append(_cls.get('id'))
            # 班级总计
            total_classes.append(_cls.get('id'))

        result['total_classes'] = total_classes

        students = ClassStudents.objects.filter(
            student_class__edu_admin_id=eduadmin_id,
            student_class__is_active=True,
            student_class__lps_version='3.0',
            student_class__class_type=Class.CLASS_TYPE_NORMAL,
        )

        today = datetime.datetime.now().date()
        result['total'] = students.count()
        # 今日新增
        result['today'] = students.filter(created__gt=today).count()
        # 已毕业的
        result['graduate'] = students.filter(
            student_class__status=Class.STATUS_OVER, status=ClassStudents.STATUS_NORMAL
        ).count()
        # 已退学的
        result['quit'] = students.filter(status=ClassStudents.STATUS_QUIT).count()

        for _cls in classes:
            if _cls.get('status') == Class.STATUS_OVER:  # 已经结束的
                continue
            info = ClassStudentsInterface(_cls['id']).dashboard
            result['finish'] += info['finish']
            result['normal'] += info['normal']
            result['paused'] += info['paused']
            result['behind'] += info['behind']

        return result
