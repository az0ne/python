# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # 统计_班级完成度
    url(r'^$', 'mz_eduadmin.stats.views.index',
        name='index'),
    # 问卷展示页面
    url(r'questionnaire/(?P<class_id>\d+)/$', 'mz_eduadmin.stats.views.get_questionnaire_det',
        name='get_questionnaire_det'),
    # 问卷提交
    url(r'questionnaire/submit/$', 'mz_eduadmin.stats.views.questionnaire_submit', name='questionnaire_submit'),
    # 统计_班级满意度
    url(r'satisfaction/$', 'mz_eduadmin.stats.views.tea_ques_rec', name='tea_ques_rec'),
    # 统计_班级满意度_详情
    url(r'satisfaction/(?P<class_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$',
        'mz_eduadmin.stats.views.class_stu_satisfy_record', name='class_stu_satisfy_record'),
    # 导出学生完成度
    url(r'export_info/(?P<class_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$',
        "mz_eduadmin.stats.views.export_excel_completion", name='export_excel_completion'),
    # 导出学生满意度
    url(r'export_satisfaction_info/(?P<eu_id>\d+)/(?P<year>\d+)/(?P<month>\d+)/$',
        "mz_eduadmin.stats.views.export_excel_satisfaction", name='export_excel_satisfaction'),
)
