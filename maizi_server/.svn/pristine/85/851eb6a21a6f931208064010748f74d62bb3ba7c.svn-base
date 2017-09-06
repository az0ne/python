from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns("",
    url(r'^$', 'maiziserver.website.admin.views_course.course', name='course'),
    url(r'^add/$', 'maiziserver.website.admin.views_course.course_add', name='course_add'),
    url(r'^add/do/$', 'maiziserver.website.admin.views_course.course_add_do', name='course_add_do'),
    url(r'^update/$', 'maiziserver.website.admin.views_course.course_update', name='course_update'),
    url(r'^update/do/$', 'maiziserver.website.admin.views_course.course_update_do', name='course_update_do'),
    url(r'^set/$', 'maiziserver.website.admin.views_course.course_set', name='course_set'),

    url(r'^knowledge/$', 'maiziserver.website.admin.views_course.course_knowledge', name='course_knowledge'),
    url(r'^knowledge/add/$', 'maiziserver.website.admin.views_course.course_knowledge_add', name='course_knowledge_add'),
    url(r'^knowledge/add/do/$', 'maiziserver.website.admin.views_course.course_knowledge_add_do', name='course_knowledge_add_do'),
    url(r'^knowledge/update/$', 'maiziserver.website.admin.views_course.course_knowledge_update', name='course_knowledge_update'),
    url(r'^knowledge/update/do/$', 'maiziserver.website.admin.views_course.course_knowledge_update_do', name='course_knowledge_update_do'),
    url(r'^knowledge/set/$', 'maiziserver.website.admin.views_course.course_knowledge_set', name='course_knowledge_set'),

    url(r'^knowledge/item/$', 'maiziserver.website.admin.views_course.course_knowledge_item', name='course_knowledge_item'),
    url(r'^knowledge/item/update/$', 'maiziserver.website.admin.views_course.course_knowledge_item_update', name='course_knowledge_item_update'),
    url(r'^knowledge/item/update/do/$', 'maiziserver.website.admin.views_course.course_knowledge_item_update_do', name='course_knowledge_item_update_do'),
    url(r'^knowledge/item/add/$', 'maiziserver.website.admin.views_course.course_knowledge_item_add', name='course_knowledge_item_add'),
    url(r'^knowledge/item/add/do/$', 'maiziserver.website.admin.views_course.course_knowledge_item_add_do', name='course_knowledge_item_add_do'),
    url(r'^knowledge/item/set/$', 'maiziserver.website.admin.views_course.course_knowledge_item_set', name='course_knowledge_item_set'),

)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
