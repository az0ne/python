# -*- coding: utf-8 -*-
__author__ = 'zhangyunrui'

from django.db import models


# 学生完成度记录
class StudentCompletion(models.Model):
    class_id = models.IntegerField(u'班级id')
    student_id = models.IntegerField(u'学生id')
    cur_task_id = models.IntegerField(u'当前任务计数')
    stage_task_id = models.IntegerField(u'阶段任务关系id', default=0)
    createtime = models.DateField(u'创建时间')

    class Meta:
        verbose_name = u'学生完成度记录'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)



# 满意度调查问卷版块
class QuestionnaireTopic(models.Model):
    name = models.CharField(u'版块名称', max_length=30)
    index = models.IntegerField(u'排序', default=99)

    class Meta:
        verbose_name = u'满意度调查问卷版块'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 满意度调查问卷题目
class QuestionnaireItem(models.Model):
    topic = models.ForeignKey(QuestionnaireTopic, verbose_name=u'问卷版块id')
    question_stem = models.CharField(u'题干', max_length=100)
    index = models.IntegerField(u'版块内排序', default=99)

    class Meta:
        verbose_name = u'满意度调查问卷题目'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 学生问卷
class StudentQuestionnaire(models.Model):
    classstudent_id = models.IntegerField(u'班级学生id')
    createtime = models.DateField(u'创建时间', auto_now_add=True)
    is_finished = models.BooleanField(u'完成状态', default=False)
    subjective_item_1 = models.CharField(u'主观题1', blank=True, null=True, max_length=300)
    subjective_item_2 = models.CharField(u'主观题2', blank=True, null=True, max_length=300)

    class Meta:
        verbose_name = u'学生问卷'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 学生问卷题目记录
class StudentQuestionnaireItemScore(models.Model):
    SCORES_JC = 1
    SCORES_JG = 2
    SCORES_ZD = 3
    SCORES_LH = 4
    SCORES_YX = 5
    SCORES = {
        SCORES_JC: u'较差',
        SCORES_JG: u'及格',
        SCORES_ZD: u'中等',
        SCORES_LH: u'良好',
        SCORES_YX: u'优秀',
    }
    questionnaire_item = models.ForeignKey(QuestionnaireItem, verbose_name=u'问卷题目id')
    student_questionnaire = models.ForeignKey(StudentQuestionnaire, verbose_name=u'学生问卷id')
    score = models.IntegerField(u'分数', choices=SCORES.items(), default=SCORES_LH)

    class Meta:
        verbose_name = u'学生问卷题目记录'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)


# 老师问卷记录
class TeacherQuestionnaireRecord(models.Model):
    teacher_id = models.IntegerField(u'老师id')
    class_id = models.IntegerField(u'班级id')
    createtime = models.DateField(u'创建时间', auto_now_add=True)
    topic_score = models.DecimalField(u'各板块得分', max_digits=4, decimal_places=2)
    questionnaire_topic = models.ForeignKey(QuestionnaireTopic, verbose_name=u'问题板块')
    scored_student_count = models.IntegerField(u'打分人数', default=0)

    class Meta:
        verbose_name = u'老师问卷记录'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return str(self.id)
