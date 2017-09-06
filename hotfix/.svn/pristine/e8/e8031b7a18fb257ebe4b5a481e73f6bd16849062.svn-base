# -*- coding: utf-8 -*-
__author__ = 'guotao'
import rest_views
from django.conf.urls import patterns, url,include
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'CareerCourse', rest_views.CareerCourseViewSet)
router.register(r'CareerCourseKeyWords', rest_views.CareerCourseKeyWordsViewSet)
router.register(r'Keywords', rest_views.KeywordsViewSet)
router.register(r'Stage', rest_views.StageViewSet)
router.register(r'Course', rest_views.CourseViewSet)
router.register(r'Course_Stages_m', rest_views.Course_Stages_mViewSet)
router.register(r'UserProfile', rest_views.UserProfileViewSet)
router.register(r'CourseKeyWords', rest_views.CourseKeyWordsViewSet)
router.register(r'Lesson', rest_views.LessonViewSet)
router.register(r'Homework', rest_views.HomeworkViewSet)
router.register(r'Project', rest_views.ProjectViewSet)
router.register(r'Paper', rest_views.PaperViewSet)
router.register(r'Quiz', rest_views.QuizViewSet)
router.register(r'CourseResource', rest_views.CourseResourceViewSet)
router.register(r'LessonResource', rest_views.LessonResourceViewSet)
router.register(r'CountryDict', rest_views.CountryDictViewSet)
router.register(r'ProvinceDict', rest_views.ProvinceDictViewSet)
router.register(r'CityDict', rest_views.CityDictViewSet)
router.register(r'StudyBase', rest_views.StudyBaseViewSet)
router.register(r'StudyGoal', rest_views.StudyGoalViewSet)
# print router.ur
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    url(r'^', include(router.urls)),
)