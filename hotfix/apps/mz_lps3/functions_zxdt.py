# -*- coding: utf-8 -*-
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")

import django

django.setup()

import json
import datetime
import string
from django.shortcuts import get_object_or_404
from django.http.response import Http404
from django.template.defaultfilters import linebreaksbr
from django.utils.html import escape
from django.utils.safestring import mark_safe, SafeData
from django.utils.text import normalize_newlines
from mz_course.models import Stage
from mz_lps.models import Paper, PaperRecord, Quiz, QuizRecord
from mz_lps3.models import UserKnowledgeItemRecord, UserTaskRecord, Task, KnowledgeItem

def breakspace(value, autoescape=None):
    autoescape = autoescape and not isinstance(value, SafeData)
    value = normalize_newlines(value)
    if autoescape:
        value = escape(value)
    return mark_safe(value.replace(' ', '&nbsp'))

class TimedTestBase(object):
    def __init__(self, user_id, class_id, knowledgeitem_id, stage_task_id):
        self.m_id = user_id
        self.m_class_id = class_id
        self.m_knowledgeitem_id = knowledgeitem_id
        self.m_stage_task_id = stage_task_id
        self.m_context = {}
        self.m_is_paper_completed = False

        self._init_data()

    def _init_data(self):
        # 取基础数据
        self.m_knowledgeitem = get_object_or_404(KnowledgeItem, id=self.m_knowledgeitem_id)
        self.m_paper_id = self.m_knowledgeitem.obj_id

        # 取record数据
        # 能进入限时答题的,UserTaskRecord必然存在
        self.m_user_task_record = get_object_or_404(UserTaskRecord, student_id=self.m_id,
                                                    class_id=self.m_class_id,
                                                    stage_task=self.m_stage_task_id)
        # 能进入限时答题的,UserKnowledgeItemRecord必然存在,因为此url是在task详情页点击链接时产生的
        self.m_knowledgeitem_record = get_object_or_404(UserKnowledgeItemRecord,
                                                        student_id=self.m_id,
                                                        class_id=self.m_class_id,
                                                        user_task_record=self.m_user_task_record,
                                                        knowledge_item=self.m_knowledgeitem_id)

        # 判断是否有paperrecord实例
        self.m_quiz_records = 0
        self.m_paper_record = PaperRecord.objects.filter(student_id=self.m_id, paper_id=self.m_paper_id)
        if len(self.m_paper_record) > 0:
            self.m_is_paper_completed = True
            self.m_quiz_records = QuizRecord.objects.filter(paper_record=self.m_paper_record[0].id).order_by('quiz')

        # 取paper和quizs数据
        self.m_paper = get_object_or_404(Paper, examine_type=6, pk=self.m_paper_id)
        self.m_quizs = Quiz.objects.filter(paper=self.m_paper_id)

    # 判断item_record状态是否为"DONE",否则改为"DONE"
    def _create_knowledge_item_record(self):
        record = self.m_knowledgeitem_record
        if record.status != "DONE":
            record.status = "DONE"
            record.done_time = datetime.datetime.now()
            record.save()

    def get_context(self):
        return self.m_context

# 学生端做题与查看错题
class StudentTimedTest(TimedTestBase):
    def _init_data(self):
        TimedTestBase._init_data(self)

        # 初始化基础数据
        self.m_context['class_id'] = self.m_class_id  #
        self.m_context['stage_task_id'] = self.m_stage_task_id  #
        self.m_context['knowledgeitem'] = self.m_knowledgeitem  #
        self.m_context['knowledgeitem_type'] = KnowledgeItem.TYPE_CHOICES[2][1]  #
        self.m_context['paper'] = self.m_paper  #
        self.m_context['paper_completed_state'] = False  #

        # 构造做题的paper数据
        new_paper = {'paper': []}
        for quiz in self.m_quizs:
            options = None
            codeOptions = "options=" + quiz.item_list
            try:
                exec (codeOptions)
            except SyntaxError:
                continue
            quiz_item = [quiz.id, linebreaksbr(breakspace(quiz.question)), options]
            new_paper['paper'].append(quiz_item)
        self.m_context['new_paper'] = json.dumps(new_paper)  #
        self.m_context['quizs_num'] = len(new_paper['paper'])  #
        self.m_context['quiz_num'] = range(len(new_paper['paper']))  #

        # 并初始化查看错题相关数据
        self.m_context['completed_paper'] = json.dumps({'paper': []})  #
        self.m_context['correct_quizs'] = 0
        self.m_context['false_quizs'] = 0
        self.m_context['accuracy_percent'] = 0

        self._set_paper_completed_state()

    def _set_paper_completed_state(self):
        if not self.m_is_paper_completed:
            return

        self.m_context['paper_completed_state'] = True
        self._create_knowledge_item_record()

        # 构造查看错题的paper数据
        paper = {'paper': []}
        for quiz_record in self.m_quiz_records:
            quiz = Quiz.objects.get(id=quiz_record.quiz.id)
            options = None
            codeOptions = "options=" + quiz.item_list
            try:
                exec (codeOptions)
            except SyntaxError:
                continue
            quiz_item = [linebreaksbr(breakspace(quiz.question)),
                         options,
                         quiz.result.upper(),
                         quiz_record.result.upper()]
            paper['paper'].append(quiz_item)
        self.m_context['completed_paper'] = json.dumps(paper)

        # 计算做题正确率
        self.m_context['accuracy_percent'] = str(int(self.m_paper_record[0].accuracy * 100))  #
        self.m_context['correct_quizs'] = str(
            int(round(len(self.m_quiz_records) * self.m_paper_record[0].accuracy, 0)))  #
        self.m_context['false_quizs'] = str(
            int(round(len(self.m_quiz_records) * (1 - self.m_paper_record[0].accuracy), 0)))  #

# 老师端查看错题
class TeacherTimedTest(TimedTestBase):
    def _init_data(self):
        TimedTestBase._init_data(self)
        # 取stage和task信息
        try:
            self.m_stage = Stage.objects.xall().get(stagetaskrelation__id=self.m_stage_task_id)
            self.m_task = Task.objects.get(stagetaskrelation__id=self.m_stage_task_id)
        except:
            raise Http404

        # 构造老师端查看错题paper数据
        paper_by_teacher = {'stagename': self.m_stage.name,
                            'taskname': self.m_task.name,
                            'papertitle': self.m_paper.title}
        quizs_by_teacher = []
        for quiz_record in self.m_quiz_records:
            quiz = Quiz.objects.get(id=quiz_record.quiz.id)
            options = None
            codeOptions = "options=" + quiz.item_list
            try:
                exec (codeOptions)
            except SyntaxError:
                continue
            item = {'question': quiz.question, 'answer': {}}
            for op in options:
                item['answer'][op[0]] = op[1]
            item['correct'] = quiz.result.upper()
            item['user_choose'] = quiz_record.result.upper()
            quizs_by_teacher.append(item)
        paper_by_teacher['quizs'] = quizs_by_teacher
        self.m_context['paper_by_teacher'] = paper_by_teacher

# 交卷
class TimedTestRecorder(TimedTestBase):
    def __init__(self, user_id, class_id, knowledgeitem_id, stage_task_id, paper):
        TimedTestBase.__init__(self, user_id, class_id, knowledgeitem_id, stage_task_id)
        self.m_commit_paper = paper

    # 获取学生提交的数据,把record写入数据库,返回正确率等数据
    def record(self):
        # 计算正确率
        quiz_correct = 0
        paper = self.m_commit_paper
        for k, v in paper.iteritems():
            quiz_id = string.atoi(k)
            quiz_result = Quiz.objects.filter(id=quiz_id)[0].result.upper()
            if quiz_result == v.upper():
                quiz_correct += 1.0
            paper_accuracy = round(quiz_correct / len(paper), 2)

        # 如果paperrecord存在,返回空元组
        if len(self.m_paper_record):
            return ()

        # 写入paperrecord
        paper_record = PaperRecord(is_active=1,
                                   date_publish=datetime.datetime.now(),
                                   examine_id=self.m_knowledgeitem.obj_id,
                                   student_id=self.m_id,
                                   paper_id=self.m_knowledgeitem.obj_id,
                                   accuracy=paper_accuracy)
        paper_record.save()

        # 写入quizrecord
        for k, v in paper.iteritems():
            quiz_record = QuizRecord(result=v.upper(),
                                     paper_record_id=paper_record.id,
                                     quiz_id=string.atoi(k))
            quiz_record.save()

        # 更改knowledgerecord
        self._create_knowledge_item_record()

        # 返回正确率
        correct_quizs = int(quiz_correct)
        false_quizs = int(len(paper) - quiz_correct)
        accuracy_percent = str(int(paper_accuracy * 100)) + "%"
        return str(correct_quizs), str(false_quizs), accuracy_percent

if __name__ == "__main__":
    # u = StudentItemExam(34000, 111, 490, 11)
    pass