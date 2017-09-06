# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from mz_ad.views import *

urlpatterns = patterns('',
                       url(r'^pm/$', pm, name="pm"),
                       url(r'^python/$', python, name="python"),
                       url(r'^ui/$', ui, name="ui"),
                       url(r'^web/$', web, name="web"),
                       url(r'^op/$', op, name="op"),
                       url(r'^ai/$', ai, name="ai"),
  )