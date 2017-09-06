# -*- coding: utf-8 -*-
import xadmin
from mz_eduadmin.stats import models


class StudentCompletionAdmin(object):
    list_display = ('class_id', 'student_id', 'cur_task_id', 'stage_task_id', 'createtime')
    search_fields = ['class_id', 'student_id']


class QuestionnaireTopicAdmin(object):
    list_display = ('name', 'index')


class QuestionnaireItemAdmin(object):
    list_display = ('topic', 'question_stem', 'index')


class StudentQuestionnaireAdmin(object):
    list_display = ('classstudent_id', 'createtime', 'is_finished', 'subjective_item_1', 'subjective_item_2')
    search_fields = ['classstudent_id']


class StudentQuestionnaireItemScoreAdmin(object):
    list_display = ('questionnaire_item', 'student_questionnaire', 'score')
    search_fields = ['student_questionnaire']


class TeacherQuestionnaireRecordAdmin(object):
    list_display = ('teacher_id', 'class_id', 'createtime', 'topic_score', 'questionnaire_topic', 'scored_student_count')
    search_fields = ['class_id', 'teacher_id']


# Register your models here.
xadmin.site.register(models.StudentCompletion, StudentCompletionAdmin)
xadmin.site.register(models.QuestionnaireTopic, QuestionnaireTopicAdmin)
xadmin.site.register(models.QuestionnaireItem, QuestionnaireItemAdmin)
xadmin.site.register(models.StudentQuestionnaire, StudentQuestionnaireAdmin)
xadmin.site.register(models.StudentQuestionnaireItemScore, StudentQuestionnaireItemScoreAdmin)
xadmin.site.register(models.TeacherQuestionnaireRecord, TeacherQuestionnaireRecordAdmin)
