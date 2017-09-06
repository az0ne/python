from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns("",
    url(r'^$', 'maiziserver.website.admin.views_student.student_sailer', name='student_sailer'),
    url(r'^add/$', 'maiziserver.website.admin.views_student.student_sailer_add', name='student_sailer_add'),
    url(r'^add/do/$', 'maiziserver.website.admin.views_student.student_sailer_add_do', name='student_sailer_add_do'),
    url(r'^update/$', 'maiziserver.website.admin.views_student.student_sailer_update', name='student_sailer_update'),
    url(r'^update/do/$', 'maiziserver.website.admin.views_student.student_sailer_update_do',name='student_sailer_update_do'),

) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
