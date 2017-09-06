# -*- coding:utf-8-*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic import RedirectView

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'home', name='home'),
                       # url(r'^blog/', include('blog.urls')),
                       url(r'^operation/', include('mz_operation.url', namespace='mz_operation')),
                       url(r'^lps4career/', include('mz_lps4.career.url', namespace='lps4career')),
                       # url(r'^tag/', include('mz_tag.urls', namespace='mz_tag')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^ads/', include('mz_ads.urls', namespace='mz_ads')),
                       url(r'^course/', include('mz_course.urls', namespace='mz_course')),
                       url(r'^seo/', include('mz_seo.urls', namespace='mz_seo')),
                       url(r'^wiki/', include('mz_wiki.url', namespace='mz_wiki')),
                       url(r'^backAdmin/', include('mz_back.urls', namespace='mz_back')),
                       url(r'^micro/', include('mz_micro.url', namespace='mz_micro')),
                       url(r'^article/', include('mz_article.urls', namespace='mz_article')),
                       url(r'^common/', include('mz_common.urls', namespace='mz_common')),
                       url(r'^homepage/', include('mz_homepage.urls', namespace='mz_homepage')),
                       url(r'^ajax/', include('mz_common.ajax_urls', namespace='ajax')),
                       url(r'^wechat/', include('mz_wechat.urls', namespace='mz_wechat')),
                       url(r'^lps4/', include('mz_lps4.urls', namespace='mz_lps4')),
                       )

urlpatterns += patterns('mz_common.views',

                        url(r'^home/cache_keys/$', 'cache_keys', name='cache_keys'),
                        url(r'^home/delete_cache/$', 'delete_cache', name='delete_cache'),
                        )

urlpatterns += patterns("mz_back.views",
                        url(r'^$', RedirectView.as_view(url='/home/'), name='admin_index'),
                        url(r'^login/$', 'admin_login', name='admin_login'),
                        url(r'^logout/$', 'admin_logout', name='admin_logout'),
                        url(r'^home/$', 'admin_home', name='admin_home'),
                        url(r'^upload/controller/$', 'upload_controller'),
                        )

urlpatterns += patterns("",
                        # url(r'^js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.JS_DIRS}),
                        # url(r'^css/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.CSS_DIRS}),
                        # url(r'^images/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.IMAGE_DIRS}),
                        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
                            {'document_root': settings.MEDIA_ROOT}),
                        )
urlpatterns += patterns("",
                        url(r'^fxsys/', include("mz_fxsys.urls", namespace="mz_fxsys")),
                        )

urlpatterns += patterns("",
                        url(r'^major/', include("mz_major.urls", namespace="mz_major")),
                        
)
