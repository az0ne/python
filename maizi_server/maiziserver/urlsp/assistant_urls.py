from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns("",
    url(r'^$', 'maiziserver.website.admin.views_assistant.assistant', name='assistant'),
    url(r'^start/$', 'maiziserver.website.admin.views_assistant.assistant_start', name='assistant_start'),
    url(r'^stop/$', 'maiziserver.website.admin.views_assistant.assistant_stop', name='assistant_stop'),
    url(r'^add/$', 'maiziserver.website.admin.views_assistant.assistant_add', name='assistant_add'),
    url(r'^add/do/$', 'maiziserver.website.admin.views_assistant.assistant_add_do', name='assistant_add_do'),
    url(r'^update/$', 'maiziserver.website.admin.views_assistant.assistant_update', name='assistant_update'),
    url(r'^update/do/$', 'maiziserver.website.admin.views_assistant.assistant_update_do', name='assistant_update_do'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
