from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns("",
    url(r'^$', 'maiziserver.website.admin.views_item.item', name='item_vedio'),
    url(r'^vedio/$', 'maiziserver.website.admin.views_vedio.item_vedio', name='item_vedio'),
    url(r'^vedio/add/$', 'maiziserver.website.admin.views_vedio.item_vedio_add', name='item_vedio_add'),
    url(r'^vedio/add/do/$', 'maiziserver.website.admin.views_vedio.item_vedio_add_do', name='item_vedio_add_do'),
    url(r'^vedio/update/$', 'maiziserver.website.admin.views_vedio.item_vedio_update', name='item_vedio_update'),
    url(r'^vedio/update/do/$', 'maiziserver.website.admin.views_vedio.item_vedio_update_do', name='item_vedio_update_do'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
