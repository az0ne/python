# -*- coding:utf-8 -*-
from rest_framework import serializers
from mz_course.models import CareerCourse,Stage,Course,Lesson
from mz_lps.models import Project,Quiz
from mz_lps2.models import UserTask

class CareerCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerCourse
        fields = ('is_unlock', 'id', )
    is_unlock = serializers.BooleanField()


class CourseProjectSerializer(serializers.Serializer):
    description = serializers.CharField()
    upload_file = serializers.FileField()
    score = serializers.IntegerField()
    record_id = serializers.CharField()
    setting_url = serializers.CharField()
    remark = serializers.CharField()

    def restore_object(self, attrs, instance=None):
        if instance:
            instance.description = attrs['description']
            instance.upload_file = attrs['upload_file']
            instance.score = attrs['score']
            instance.record_id = attrs['record_id']
            instance.setting_url = attrs['setting_url']
            instance.remark = attrs['remark']
            return instance
        return  Project(**attrs)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'is_complete', 'name', 'has_exam', 'is_complete_paper', 'exam_accuracy',
                  'has_homework', 'homework','result', 'code_exercise_type')
    is_complete = serializers.BooleanField()
    has_exam = serializers.BooleanField()
    is_complete_paper = serializers.BooleanField()
    exam_accuracy = serializers.CharField()
    has_homework = serializers.BooleanField()
    homework = serializers.FileField()
    result = serializers.CharField()


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('question', 'item_list', 'id')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'is_complete', 'is_underway', 'score', 'lesson_count', 'lesson_complete_count',
                  'lesson_has_exam_count', 'lesson_exam_complete_count', 'lesson_has_homework_count',
                  'homework_complete_count', 'has_paper', 'is_complete_paper', 'paper_accuracy', 'project', 'lesson',
                  'uncomplete_quiz', 'is_required')
    score = serializers.IntegerField(default=0)
    is_complete = serializers.BooleanField()
    is_underway = serializers.BooleanField()
    lesson_count = serializers.IntegerField()
    lesson_complete_count = serializers.IntegerField()
    lesson_has_exam_count = serializers.IntegerField()
    lesson_exam_complete_count = serializers.IntegerField()
    lesson_has_homework_count = serializers.IntegerField()
    homework_complete_count = serializers.IntegerField()
    has_paper = serializers.BooleanField()
    is_complete_paper = serializers.BooleanField()
    paper_accuracy = serializers.CharField()
    project = CourseProjectSerializer()
    lesson = LessonSerializer(many = True)
    uncomplete_quiz = QuizSerializer(many= True)
    is_required = serializers.BooleanField()


class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ('id', 'name', 'description', 'prev_stage', 'next_stage')

    prev_stage = serializers.IntegerField()
    next_stage = serializers.IntegerField()

#老师任务序列化
class TeacherUserTaskSerializer(serializers.Serializer):
    type = serializers.CharField()
    href = serializers.CharField()
    title = serializers.CharField()
    time = serializers.CharField()
    content = serializers.CharField()
    status = serializers.IntegerField()

class Stu_StatusUserTaskSerializer(serializers.Serializer):
    student_id = serializers.IntegerField()
    stustatus_id = serializers.IntegerField()
    type = serializers.CharField()
    title = serializers.CharField()
    content = serializers.CharField()
    time = serializers.CharField()

class GiveScoreUserTaskSerializer(serializers.Serializer):
    type = serializers.CharField()
    href = serializers.CharField()
    title = serializers.CharField()
    time = serializers.CharField()
    content = serializers.CharField()
    status = serializers.IntegerField()
    classmeeting_id=serializers.IntegerField()

class ClassMeetingkSerializer(serializers.Serializer):
    type = serializers.CharField()
    join_url = serializers.CharField()
    token = serializers.CharField()
    nick_name = serializers.CharField()
    content = serializers.CharField()

class CourseUserTaskSerializer(serializers.Serializer):
    finish_date = serializers.CharField()
    href = serializers.CharField()
    type = serializers.CharField()
    title = serializers.CharField()
    text1 = serializers.CharField()
    text2 = serializers.CharField()
    is_ext = serializers.IntegerField()
    create_datetime = serializers.CharField()
    status = serializers.IntegerField()