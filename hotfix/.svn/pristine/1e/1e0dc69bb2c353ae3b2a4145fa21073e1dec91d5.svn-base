# -*- coding: utf-8 -*-
"""
@version: 2016/5/11
@author: zhangyunrui
@contact: david.zhang@maiziedu.com
@file: interface.py
@time: 2016/5/11 13:50
@note:  学生端学习相关接口
"""
import datetime

from mz_lps.models import Class, ClassStudents
from mz_lps3 import functions
from mz_lps3.functions_gt import get_classmeeting_list
from mz_lps3.models import ClassRank, ClassRankRecord
from mz_lps3_free.common.interface import Free488ClassInterface
from mz_lps4.class_dict import NORMAL_CLASS_DICT
import db.api.lps.student
from utils.logger import logger as log


class StudentOverview(object):
    """
    学生信息
    """

    @staticmethod
    def normal_classes(student_id):
        """
        接口:一个学生所有的正常班级
        :param student_id: int
        :return: cstudent_list = [
            {
                'current_task_progress': 任务完成度(int, [0, 100]),
                'is_just_beginning': True/False(是否刚开始学习),
                'class_students_count': 班级人数(int, N+(不含退班人数)),
                'class_id': 班级id(int, N+),
                'class_left_days': 班级倒计时(int, N+ or u'暂未开班'(班级未开始时)),
                'current_task_id': 当前任务id(int, N+ or -1(如果current_task_id为-1, 显示'开始学习', 进入任务地图面板),
                'class_coding': 班级编号(unicode),
                'current_task_name': 当前任务名(unicode),
                'score': 得分(int),
                'study_status': 学习状态(u'学习中' or u'休学'),
                'careercourse_image': 职业课程图片url(str),
                'careercourse_name': 专业名(unicode),
                'class_end_time': 毕业时间(str, '%Y-%m-%d'(班级毕业时间, 若此字段为空, 则表示未毕业)),
                'cstudent': 班级学生(<ClassStudents: ClassStudentsobject>),
                'last_class_rank': 排名(int, N+),
            },
            ...
        ]
        """
        classstudents = ClassStudents.objects.filter(
            user_id=student_id, status=ClassStudents.STATUS_NORMAL, student_class__lps_version='3.0',
            student_class__class_type=Class.CLASS_TYPE_NORMAL, student_class__is_active=True)

        cstudent_list = list()
        lps4_cstudent_list = list()

        for cstudent in classstudents:
            sclass = cstudent.student_class
            class_id = sclass.id

            # lps3.1的入口
            if class_id in NORMAL_CLASS_DICT.values():
                career_id = sclass.career_course.id

                student_result = db.api.lps.student.get_lps4_student_info_by_user_id(student_id, career_id)
                if student_result.is_error():
                    log.warn(
                        'get_lps_3_1_class_id_by_user_id_and_career_id is error. user_id: %s, career_id: %s' % (
                            student_id, career_id))
                    student_dict = {}
                else:
                    student_dict = student_result.result()
                if student_dict:
                    ccourse = sclass.career_course
                    now_time = datetime.datetime.now()
                    end_time = student_dict.get('end_time', now_time) or now_time
                    if (end_time - now_time).seconds > 0:
                        class_end_time = 0
                        study_status = u'学习中'
                    else:
                        class_end_time = end_time.strftime('%Y.%m.%d')
                        study_status = u'已毕业'

                    # 初始化stagetask结构数据
                    iface = functions.StageTaskInterface(class_id)
                    # 加载用户信息
                    iface.load_student_data(student_id)

                    current_task = iface.get_student_latest_task(student_id)  # 当前任务

                    lps4_cstudent_list.append(dict(
                        career_id=career_id,
                        careercourse_name=ccourse.name,
                        careercourse_image=ccourse.image.url,
                        study_status=study_status,
                        class_left_days=(end_time - now_time).days,
                        class_end_time=class_end_time,
                        current_task_progress=current_task.get_progress() if current_task else 0,
                        current_task_name=current_task.task_name if current_task else '',
                        is_just_beginning=iface.is_just_beginning(student_id),
                    ))


            else:
                # 初始化stagetask结构数据
                iface = functions.StageTaskInterface(class_id)
                # 加载用户信息
                iface.load_student_data(student_id)

                current_task = iface.get_student_latest_task(student_id)  # 当前任务

                class_students_count, last_class_rank, score, class_end_time = '-', '-', 0, ''
                if sclass.meeting_enabled:
                    class_students_count = sclass.current_student_count

                    last_class_rank_info = ClassRank.objects.filter(
                        class_id=class_id, student_id=student_id).order_by('-id').first()
                    if last_class_rank_info:
                        last_class_rank = last_class_rank_info.rank

                    score, class_end_time = 0, ''
                    if sclass.status == Class.STATUS_OVER:
                        class_end_time = sclass.class_end_time.strftime('%Y.%m.%d')
                        scores = ClassRankRecord.objects.filter(class_id=class_id, rank_type=1).order_by('-rank_date')
                        if scores:
                            for s in eval(scores.first().rank_detail):
                                # 从rank_detail中找出与被查看用户student_id相等的条目的score
                                if s['student_id'] == student_id:
                                    score = s['score']

                ccourse = sclass.career_course

                cstudent_list.append(dict(
                    careercourse_name=ccourse.name,
                    careercourse_image=ccourse.image.url,
                    class_coding=sclass.coding,
                    class_id=sclass.id,
                    study_status=u'休学' if cstudent.is_pause else u'学习中',
                    class_students_count=class_students_count,
                    last_class_rank=last_class_rank,
                    class_left_days=u'%s天' % sclass.class_left_days if sclass.class_left_days else u'暂未开班',
                    current_task_id=current_task.stage_task_id if current_task else -1,
                    current_task_name=current_task.task_name if current_task else '',
                    current_task_progress=current_task.get_progress() if current_task else 0,
                    is_just_beginning=iface.is_just_beginning(student_id),
                    class_end_time=class_end_time,
                    score=score,
                    cstudent=cstudent,
                ))

        return lps4_cstudent_list, cstudent_list

    @staticmethod
    def experience_classes(student_id):
        """
        接口:一个学生所有体验班级
        :param student_id:
        :return: cstudent_list = [
            {
                'current_task_progress': 任务完成度(int, [0, 100]),
                'careercourse_image': 职业课程图片url(str),
                'current_task_name': 当前任务名(unicode),
                'class_id': 班级id(int, N+),
                'careercourse_name': 专业名(unicode),
                'student_create_time':　体验时间(入班时间)(datetime),
                'careercourse_id': 职业课程id(int),
                'is_just_beginning': True/False(是否刚开始学习),
            },
            ...
        ]
        """
        classstudents = ClassStudents.objects.filter(
            user_id=student_id, student_class__lps_version='3.0', student_class__class_type=Class.CLASS_TYPE_EXPERIENCE,
            student_class__career_course__enable_free_488=False
        )

        cstudent_dict = dict()
        for cstudent in classstudents:
            created_md = cstudent.created.strftime('%m.%d')
            created_year = cstudent.created.strftime('%Y')
            created = (created_md, created_year)
            cstudent_dict.setdefault(created, list())

            sclass = cstudent.student_class
            class_id = sclass.id

            iface = functions.StageTaskInterface(class_id)
            iface.load_student_data(student_id)
            current_task = iface.get_student_latest_task(student_id)  # 当前任务

            ccourse = sclass.career_course

            cstudent_dict[created].append(dict(
                careercourse_id=ccourse.id,
                careercourse_name=ccourse.name,
                careercourse_image=ccourse.image.url,
                class_id=class_id,
                student_create_time=cstudent.created,
                current_task_name=current_task.task_name if current_task else '',
                current_task_progress=current_task.get_progress() if hasattr(current_task, 'student_id') else 0,
                is_just_beginning=iface.is_just_beginning(student_id),
            ))

        free_488_classstudents = ClassStudents.objects.filter(
            user_id=student_id, student_class__lps_version='3.0', student_class__class_type=Class.CLASS_TYPE_FREE_488,
            student_class__career_course__enable_free_488=True
        )

        for cstudent in free_488_classstudents:
            created_md = cstudent.created.strftime('%m.%d')
            created_year = cstudent.created.strftime('%Y')
            created = (created_md, created_year)
            cstudent_dict.setdefault(created, list())

            sclass = cstudent.student_class
            class_id = sclass.id

            ccourse = sclass.career_course

            about_to_begin_clmt = get_classmeeting_list(class_id, student_id)

            if about_to_begin_clmt:
                about_to_begin_clmt = about_to_begin_clmt[0]

            fci = Free488ClassInterface(class_id)

            cstudent_dict[created].append(dict(
                careercourse_id=ccourse.id,
                careercourse_name=ccourse.name,
                careercourse_image=ccourse.image.url,
                class_id=class_id,
                class_name=sclass.name,
                meeting_duration=sclass.meeting_duration,
                student_create_time=cstudent.created,
                about_to_begin_clmt=about_to_begin_clmt,
                is_not_started=fci.is_not_started(),
                is_ongoing=fci.is_ongoing(),
                is_finished=fci.is_finished(),
            ))

        lps_3_1_experience_classstudents = ClassStudents.objects.filter(
            user_id=student_id, student_class__lps_version='3.0', student_class__class_type=Class.CLASS_TYPE_EXPERIENCE_3_1
        )

        for cstudent in lps_3_1_experience_classstudents:
            created_md = cstudent.created.strftime('%m.%d')
            created_year = cstudent.created.strftime('%Y')
            created = (created_md, created_year)
            cstudent_dict.setdefault(created, list())

            sclass = cstudent.student_class
            class_id = sclass.id

            ccourse = sclass.career_course

            iface = functions.StageTaskInterface(class_id)
            iface.load_student_data(student_id)
            current_task = iface.get_student_latest_task(student_id)  # 当前任务

            cstudent_dict[created].append(dict(
                careercourse_id=ccourse.id,
                careercourse_name=ccourse.name,
                careercourse_image=ccourse.image.url,
                is_just_beginning=iface.is_just_beginning(student_id),
                current_task_name=current_task.task_name if current_task else '',
                current_task_progress=current_task.get_progress() if hasattr(current_task, 'student_id') else 0,
            ))

        cstudent_dict = sorted(cstudent_dict.iteritems(), reverse=True)

        return cstudent_dict

    @staticmethod
    def old_classes(student_id):
        """
        接口:一个学生所有lps2班
        :param student_id:
        :return: cstudent_list = [
            {
                'careercourse_image': 职业课程图片url(str),
                'careercourse_name': 专业名(unicode),
                'careercourse_color': 职业课程颜色(str),
                'careercourse_id': 职业课程id(int),
                'class_id': 班级id(int, N+),
                'class_coding': 班级编号(unicode),
            },
            ...
        ]
        """
        classstudents = ClassStudents.objects.filter(
            user_id=student_id, status=ClassStudents.STATUS_NORMAL, student_class__is_active=True,
            student_class__class_type=Class.CLASS_TYPE_NORMAL).exclude(student_class__lps_version='3.0')

        cstudent_list = list()
        for cstudent in classstudents:
            sclass = cstudent.student_class
            ccourse = sclass.career_course

            cstudent_list.append(dict(
                careercourse_id=ccourse.id,
                careercourse_name=ccourse.name,
                careercourse_image=ccourse.image.url,
                careercourse_color=ccourse.course_color,
                class_id=sclass.id,
                class_coding=sclass.coding,
            ))

        return cstudent_list
