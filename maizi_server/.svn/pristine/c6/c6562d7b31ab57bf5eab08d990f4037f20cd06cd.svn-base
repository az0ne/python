from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns("",
    url(r'^$', 'maiziserver.website.admin.views_land.land', name='land'),
    url(r'^add/$', 'maiziserver.website.admin.views_land.land_add', name='land_add'),
    url(r'^add/do/$', 'maiziserver.website.admin.views_land.land_add_do', name='land_add_do'),
    url(r'^update/$', 'maiziserver.website.admin.views_land.land_update', name='land_update'),
    url(r'^update/do/$', 'maiziserver.website.admin.views_land.land_update_do', name='land_update_do'),
    url(r'^state/$', 'maiziserver.website.admin.views_land.land_state', name='land_state'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
