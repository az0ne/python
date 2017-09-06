# -*- coding: utf-8 -*-
__author__ = 'guotao'
from rest_serializers import *
from rest_framework import viewsets,generics
#--------课程信息部分-----------------------------------------------------------------------------------------------
class CareerCourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CareerCourse.objects.filter(course_scope=None)
    serializer_class = CareerCourseSerializer

class CareerCourseKeyWordsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CareerCourseKeyWords.objects.all()
    serializer_class = CareerCourseKeyWordsSerializer

class KeywordsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Keywords.objects.all()
    serializer_class = KeywordsSerializer

class StageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.filter(is_active=True)
    serializer_class = CourseSerializer

class Course_Stages_mViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course_Stages_m.objects.all()
    serializer_class = Course_Stages_mSerializer

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.filter(groups__name=u"老师")
    serializer_class = UserProfileSerializer

class CourseKeyWordsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CourseKeyWords.objects.all()
    serializer_class = CourseKeyWordsSerializer

class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class HomeworkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class PaperViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer

class QuizViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class CourseResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CourseResource.objects.all()
    serializer_class = CourseResourceSerializer

class LessonResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LessonResource.objects.all()
    serializer_class = LessonResourceSerializer

#-----公共数据信息------------------------------------------------------------------------------------------------------
class CountryDictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CountryDict.objects.all()
    serializer_class = CountryDictSerializer

class ProvinceDictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProvinceDict.objects.all()
    serializer_class = ProvinceDictSerializer

class CityDictViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CityDict.objects.all()
    serializer_class = CityDictSerializer

class StudyBaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudyBase.objects.all()
    serializer_class = StudyBaseSerializer

class StudyGoalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StudyGoal.objects.all()
    serializer_class = StudyGoalSerializer
#---------------------------------------------------------------------------------------------------------------------
