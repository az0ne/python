#!/usr/bin/python
# -*- coding:utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns("mz_common.ajax",
                       url(r'^careerCatagoryName/$', 'list_career_catagory_name', name='careerCatagory_name'),
                       url(r'^courseTagName/$', 'courseTag_list_all', name='courseTagAll_name'),
                       url(r'^careerCourseName/$', 'get_career_course_name', name='careerCourse_name'),
                       url(r'^careerIntroduceName/$', 'get_career_introduce_name', name='careerIntroduce_name'),
                       url(r'^articleType/getAllName/$', 'get_all_article_type_name', name='get_all_articleTypeName'),
                       url(r'^articleType/getIsHomepageName/$', 'get_is_homepage_article_type_name',
                           name='get_is_homepage_articleTypeName'),
                       url(r'^course/getIsHomepageName/$', 'get_is_homepage_course_name',
                           name="get_is_homepage_courseName"),
                       url(r'questionnaireName/$', "questionnaire_get", name="get_questionnaireName"),

                       url(r'^careerIntroduce/validateUniqueId/$', 'validate_unique_career_page_id',
                           name='validateUnique_careerId'),
                       url(r'^task/taskDesc/validateUniqueId/$', 'validate_unique_free_task_desc_id',
                           name='validateUnique_taskId'),
                       url(r'^articleType/validateUniqueId/$', 'validate_unique_article_type_id',
                           name='validateUnique_articleTypeId'),

                       )
