# coding: utf-8
import datetime

from mz_common.user_study_info_interface import get_class_and_student_info_by_user_id_and_class_id_interface, \
    get_teachers_by_class_id_interface, get_user_info_interface, get_lps4_student_info_by_user_id_interface
from mz_lps4.class_dict import NORMAL_CLASS_DICT
from mz_usercenter.student.interface_resume import get_user_class_info_interface


class UserStudyInfo(object):
    """
    用户当前职业信息
    """

    def __init__(self, user_id, class_id, career_id=0):
        self.user_id = user_id
        self.class_id = class_id
        self.start_time = None
        self.end_time = None
        self.is_stop = False
        self.is_quit = False
        self.lps_version = 4
        self.is_view_resume_intro = False
        self.start_work_time = 0
        self.is_employment_contract = False
        self.teacher_team = {'teacher': [], 'edu_admin': [], 'assistant': []}
        self._get_user_current_career(user_id, class_id, career_id)
        self._get_teacher_team_info()

    def _get_user_current_career(self, user_id, class_id, career_id):
        user_class_info = get_user_class_info_interface(user_id)
        if user_class_info:
            self.is_view_resume_intro = user_class_info['is_view_resume_intro']
            self.start_work_time = user_class_info['start_work_time']

        # 如果班级在NORMAL_CLASS_DICT里，走lps4的流程
        if class_id in NORMAL_CLASS_DICT.values():
            student_dict = get_lps4_student_info_by_user_id_interface(user_id, career_id)
            if student_dict:
                self.start_time = student_dict.get('start_time', None)
                self.end_time = student_dict.get('end_time', None)
                self.is_stop = student_dict.get('is_stop', None)
                self.is_employment_contract = student_dict.get('type', 0) == 1
                self.teacher_id = student_dict.get('teacher_id', None)
        # 再查lps3和lps2
        else:
            student_dict = get_class_and_student_info_by_user_id_and_class_id_interface(user_id, class_id)
            if student_dict:
                meeting_enabled = student_dict.get('meeting_enabled', None)
                meeting_start = student_dict.get('meeting_start', None)
                meeting_duration = student_dict.get('meeting_duration', None)
                self.lps_version = 3 if student_dict.get('lps_version', None) == '3.0' else 2
                self.edu_admin = student_dict.get('edu_admin', None)
                if meeting_enabled and meeting_start and meeting_duration:
                    self.start_time = meeting_start
                    self.end_time = meeting_start + datetime.timedelta(days=meeting_duration)
                    self.is_stop = student_dict.get('is_pause', None)
                    self.is_quit = student_dict.get('cs.status', None) != 1
                    self.is_employment_contract = student_dict.get('is_employment_contract', False)

    def _get_teacher_team_info(self):
        teacher_id_list = []
        eduadmin_id_list = []
        if self.lps_version != 4:
            teachers = get_teachers_by_class_id_interface(self.class_id)
            if teachers:
                for t in teachers:
                    teacher_id_list.append(t['id'])
            if self.edu_admin:
                eduadmin_id_list.append(self.edu_admin)
                del self.edu_admin

        elif self.teacher_id:
            teacher_id_list.append(self.teacher_id)
            del self.teacher_id

        if teacher_id_list:
            self.teacher_team['teacher'] = list(get_user_info_interface(teacher_id_list))
        if eduadmin_id_list:
            self.teacher_team['edu_admin'] = list(get_user_info_interface(eduadmin_id_list))
