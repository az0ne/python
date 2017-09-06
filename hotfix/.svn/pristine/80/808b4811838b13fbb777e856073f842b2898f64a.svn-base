# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', 'mz_eduadmin.classes.views.index', name='index'),
    url(r'^update_state/$', 'mz_eduadmin.classes.views.update_state', name='update_state'),
    url(r'^create_class/$', 'mz_eduadmin.classes.views.create_class', name='create_class'),
    url(r'^get_class_teachers/$', 'mz_eduadmin.classes.views.get_class_teachers', name='get_class_teachers'),
    url(r'^update_class_teachers/(?P<class_id>\d+)/$', 'mz_eduadmin.classes.views.update_class_teachers', name='update_class_teachers')
)
