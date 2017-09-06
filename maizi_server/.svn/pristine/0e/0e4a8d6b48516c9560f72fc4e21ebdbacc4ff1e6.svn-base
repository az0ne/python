from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns("",
  url(r'^$', 'maiziserver.website.admin.views_teacher.teacher', name='teacher'),
  url(r'^start/$', 'maiziserver.website.admin.views_teacher.teacher_start',name='teacher_start'),
  url(r'^stop/$', 'maiziserver.website.admin.views_teacher.teacher_stop',name='teacher_stop'),
  url(r'^add/$', 'maiziserver.website.admin.views_teacher.teacher_add',name='teacher_add'),
  url(r'^add/do/$', 'maiziserver.website.admin.views_teacher.teacher_add_do',name='teacher_add_do'),
  url(r'^update/$', 'maiziserver.website.admin.views_teacher.teacher_update',name='teacher_update'),
  url(r'^update/do/$', 'maiziserver.website.admin.views_teacher.teacher_update_do',name='teacher_update_do'),
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
