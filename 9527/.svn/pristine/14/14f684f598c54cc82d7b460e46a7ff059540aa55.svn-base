# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from mz_major import major_views,item_views,course_views,knowledge_views,major_course_views

urlpatterns = patterns('',

                       #major 的urls

                        url(r'major/add/$', major_views.add_major, name="add_major"),
                        url(r'major/update/$', major_views.update_major, name="update_major"),
                        # url(r'major/del/$', major_views.del_major, name="del_major"),
                        url(r'major/get/$', major_views.get_major, name="get_major"),

                       #item 的urls

                        url(r'item/add/$', item_views.add_item, name="add_item"),
                        url(r'item/update/$', item_views.update_item, name="update_item"),
                       # url(r'item/del/$', item_views.del_item, name="del_item"),
                        url(r'item/get/$', item_views.get_item, name="get_item"),

                       #knowledge 的urls

                        url(r'knowledge/add/$', knowledge_views.add_knowledge, name="add_knowledge"),
                        url(r'knowledge/update/$', knowledge_views.update_knowledge, name="update_knowledge"),
                        # url(r'knowledge/del/$', knowledge_views.del_knowledge, name="del_knowledge"),
                        url(r'knowledge/get/$', knowledge_views.get_knowledge, name="get_knowledge"),

                        #course 的urls

                        url(r'course/add/$', course_views.add_course, name="add_course"),
                        url(r'course/update/$', course_views.update_course, name="update_course"),
                        # url(r'major/del/$', major_views.del_major, name="del_major"),
                        url(r'course/get/$', course_views.get_course, name="get_course"),

                        #major_course 的urls

                        url(r'major_course/add/$', major_course_views.add_major_course, name="add_major_courses"),
                        url(r'major_course/update/$', major_course_views.update_major_course, name="update_major_course"),
                        # url(r'major_course/del/$', major_course_views.del_major_course, name="del_major_course"),
                        url(r'major_course/get/$', major_course_views.get_major_course, name="get_major_course"),

                       )
