from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns("",
    url(r'^$', 'maiziserver.website.admin.views_user.user', name='user'),
    url(r'^start/$', 'maiziserver.website.admin.views_user.user_start', name='user_start'),
    url(r'^stop/$', 'maiziserver.website.admin.views_user.user_stop', name='user_stop'),
    url(r'^add/$', 'maiziserver.website.admin.views_user.user_add', name='user_add'),
    url(r'^add/do/$', 'maiziserver.website.admin.views_user.user_add_do', name='user_add_do'),
    url(r'^update/$', 'maiziserver.website.admin.views_user.user_update', name='user_update'),
    url(r'^update/do/$', 'maiziserver.website.admin.views_user.user_update_do', name='user_update_do'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
