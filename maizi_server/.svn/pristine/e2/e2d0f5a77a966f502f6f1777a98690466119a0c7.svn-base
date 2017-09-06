from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns("",
    url(r'^$', 'maiziserver.website.admin.views_author.author', name='author'),
    url(r'^add/$', 'maiziserver.website.admin.views_author.author_add', name='author_add'),
    url(r'^add/do/$', 'maiziserver.website.admin.views_author.author_add_do', name='author_add_do'),
    url(r'^update/$', 'maiziserver.website.admin.views_author.author_update', name='author_update'),
    url(r'^update/do/$', 'maiziserver.website.admin.views_author.author_update_do', name='author_update_do'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
