# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


# 教务模块URL
urlpatterns = patterns("",
    url(r'^$', 'maiziserver.website.admin.views_student.student_assistant', name='student_assistant'),
    url(r'^update/$', 'maiziserver.website.admin.views_student.student_assistant_update',name='student_assistant_update'),
    url(r'^update/do/$','maiziserver.website.admin.views_student.student_assistant_update_do',name='student_assistant_update_do'),


    url(r'^change_teacher/$', 'maiziserver.website.admin.views_student.student_assistant_change_teacher', name='student_assistant_change_teacher'),
    url(r'^change_teacher/add/$', 'maiziserver.website.admin.views_student.student_assistant_change_teacher_add', name='student_assistant_change_teacher_add'),
    url(r'^change_teacher/add/do/$', 'maiziserver.website.admin.views_student.student_assistant_change_teacher_add_do', name='student_assistant_change_teacher_add_do'),

    url(r'^change_assistant/$', 'maiziserver.website.admin.views_student.student_assistant_change_assistant', name='student_assistant_change_assistant'),
    url(r'^change_assistant/add/$', 'maiziserver.website.admin.views_student.student_assistant_change_assistant_add', name='student_assistant_change_assistant_add'),
    url(r'^change_assistant/add/do/$', 'maiziserver.website.admin.views_student.student_assistant_change_assistant_add_do', name='student_assistant_change_assistant_add_do'),

    url(r'^communication/$', 'maiziserver.website.admin.views_student.student_assistant_communication', name='student_assistant_communication'),
    url(r'^communication/add/$', 'maiziserver.website.admin.views_student.student_assistant_communication_add', name='student_assistant_communication_add'),
    url(r'^communication/add/do/$', 'maiziserver.website.admin.views_student.student_assistant_communication_add_do', name='student_assistant_communication_add_do'),
    url(r'^communication/detail/$', 'maiziserver.website.admin.views_student.student_assistant_communication_detail', name='student_assistant_communication_detail'),
    url(r'^communication_all/$', 'maiziserver.website.admin.views_student.student_assistant_communication_all', name='student_assistant_communication_all'),

    url(r'^suspend/$','maiziserver.website.admin.views_student.student_assistant_suspend',name='student_assistant_suspend'),
    url(r'^suspend/add/$', 'maiziserver.website.admin.views_student.student_assistant_suspend_add',name='student_assistant_suspend_add'),
    url(r'^suspend/add/do/$','maiziserver.website.admin.views_student.student_assistant_suspend_add_do',name='student_assistant_suspend_add_do'),
    url(r'^suspend/detail/$','maiziserver.website.admin.views_student.student_assistant_suspend_detail',name='student_assistant_suspend_detail'),
    url(r'^suspend_all/$','maiziserver.website.admin.views_student.student_assistant_suspend_all',name='student_assistant_suspend_all'),


    url(r'^interview/$', 'maiziserver.website.admin.views_student.student_assistant_interview',name='student_assistant_interview'),
    url(r'^interview/add/$','maiziserver.website.admin.views_student.student_assistant_interview_add',name='student_assistant_interview_add'),
    url(r'^interview/add/do/$','maiziserver.website.admin.views_student.student_assistant_interview_add_do',name='student_assistant_interview_add_do'),
    url(r'^interview/update/$','maiziserver.website.admin.views_student.student_assistant_interview_update',name='student_assistant_interview_update'),
    url(r'^interview/update/do/$','maiziserver.website.admin.views_student.student_assistant_interview_update_do',name='student_assistant_interview_update_do'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# 学习活跃模块URL
urlpatterns += [
    url(r'^monitor_learn_activity/$', 'maiziserver.website.admin.views_monitor.learning_activity_index', name='learning_activity_index'),
    url(r'^active_points/$', 'maiziserver.website.admin.views_monitor.list_active_point_by_student', name='list_active_point_by_student')
]
