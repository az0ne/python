# -*- coding: utf-8 -*-


class CoachCommentUserType(object):
    STUDENT = 10
    TEACHER = 20

    mapper = {
        10: u'学生',
        20: u'老师'
    }


class CoachUserType(object):
    STUDENT = 10            # 学生主动发起
    STUDENT_VIDEO = 11      # 学生视频问答
    TEACHER = 20            # 老师主动发起
    PROJECT = 30            # 项目辅导
    UNLOCK = 40             # 任务球解锁
    NW_COMMUNICATE = 50     # 新学员入学沟通

    students = (STUDENT, STUDENT_VIDEO)
    teachers = (TEACHER, UNLOCK)
