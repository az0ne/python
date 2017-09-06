# -*- coding: utf-8 -*-
__author__ = 'guotao'
from django.db import models
from rest_framework import serializers
from mz_course.models import CareerCourse,Keywords,Stage,Course_Stages_m,Course,Lesson,CourseResource,LessonResource
from mz_user.models import UserProfile,CountryDict,ProvinceDict,CityDict,StudyBase,StudyGoal
from mz_lps.models import Homework,Project,Paper,Quiz

#中间表需要映射,因此需要补充------------------------------------------------------------------------------------------------

class CareerCourseKeyWords(models.Model):
    careercourse = models.ForeignKey(CareerCourse)
    keywords = models.ForeignKey(Keywords)

    class Meta:
        verbose_name = "职业课程关键词"
        verbose_name_plural = verbose_name
        ordering = ['-id']
        db_table = 'mz_course_careercourse_search_keywords'
        unique_together = (("careercourse", "keywords"),)

class CourseKeyWords(models.Model):
    course = models.ForeignKey(Course)
    keywords = models.ForeignKey(Keywords)

    class Meta:
        verbose_name = "职业课程关键词"
        verbose_name_plural = verbose_name
        ordering = ['-id']
        db_table = 'mz_course_course_search_keywords'
        unique_together = (("course", "keywords"),)

#需要序列化的数据表--------------------------------------------------------------------------------------------------------

class CareerCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerCourse
        fields = ('id', 'name', 'short_name', 'image','course_color','description','index','seo_title',)

class CareerCourseKeyWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerCourseKeyWords
        fields = ('id', 'careercourse', 'keywords')

class KeywordsSerializer(serializers.ModelSerializer):
        class Meta:
            model = Keywords
            fields = ('id', 'name')

class StageSerializer(serializers.ModelSerializer):
        class Meta:
            model = Stage
            fields = ('id', 'name','description','index','career_course')

class CourseSerializer(serializers.ModelSerializer):
        class Meta:
            model = Course
            fields = ('id', 'name','image','description','is_active','date_publish','need_days','need_days_base',
                      'is_novice','is_click','index','teacher')

class Course_Stages_mSerializer(serializers.ModelSerializer):
        class Meta:
            model = Course_Stages_m
            fields = ('id', 'course','stage','is_required')

class UserProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = UserProfile
            fields = ('id','uuid', 'email','nick_name','mobile','position','description','username','avatar_url')

class CourseKeyWordsSerializer(serializers.ModelSerializer):
        class Meta:
            model = CourseKeyWords
            fields = ('id', 'course', 'keywords')

class LessonSerializer(serializers.ModelSerializer):
        class Meta:
            model = Lesson
            fields = ('id','name', 'video_url','video_length','index','seo_title','seo_keyword','seo_description',
                      'have_homework','course')

#----------作业资源--------------------------------------------------------------------------------------------------
class HomeworkSerializer(serializers.ModelSerializer):
        class Meta:
            model = Homework
            fields = ('id', 'description', 'examine_type','relation_type','relation_id','is_active','date_publish','score',
                      'study_point')

class ProjectSerializer(serializers.ModelSerializer):
        class Meta:
            model = Project
            fields = ('id', 'description', 'examine_type','relation_type','relation_id','is_active','date_publish','score',
                      'study_point')

class PaperSerializer(serializers.ModelSerializer):
        class Meta:
            model = Paper
            fields = ('id', 'description', 'examine_type','relation_type','relation_id','is_active','date_publish','score',
                      'study_point')

class QuizSerializer(serializers.ModelSerializer):
        class Meta:
            model = Quiz
            fields = ('id', 'question', 'item_list','result','index','paper')


class CourseResourceSerializer(serializers.ModelSerializer):
        class Meta:
            model = CourseResource
            fields = ('id', 'name', 'download_url','download_count','course')

class LessonResourceSerializer(serializers.ModelSerializer):
        class Meta:
            model = LessonResource
            fields = ('id', 'name', 'download_url','download_count','lesson')

#------------------公共数据资源----------------------------------------------------------------------------------------
class CountryDictSerializer(serializers.ModelSerializer):
        class Meta:
            model = CountryDict
            fields = ('id', 'name', 'index')

class ProvinceDictSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProvinceDict
            fields = ('id', 'name', 'index','country')

class CityDictSerializer(serializers.ModelSerializer):
        class Meta:
            model = CityDict
            fields = ('id', 'name', 'index','province')

class StudyBaseSerializer(serializers.ModelSerializer):
        class Meta:
            model = StudyBase
            fields = ('id', 'name', 'index')

class StudyGoalSerializer(serializers.ModelSerializer):
        class Meta:
            model = StudyGoal
            fields = ('id', 'name', 'index')

