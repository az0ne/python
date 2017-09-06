# -*- coding: utf-8 -*-

"""
@author : Jackie
@date : 2015/12/11
@note :
"""
from django.http.response import JsonResponse
from mz_lps3.functions_zxdt import TeacherTimedTest


def student_item_exam_div(request, class_id, student_id, stage_task_id, knowledgeitem_id):
    teacher_timed_test = TeacherTimedTest(student_id, class_id, knowledgeitem_id, stage_task_id)
    return JsonResponse(teacher_timed_test.get_context()['paper_by_teacher'])
