from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns("",
    url(r'^$', 'maiziserver.website.admin.views_career.career', name='career'),
    url(r'^start/$', 'maiziserver.website.admin.views_career.career_start', name='career_start'),
    url(r'^stop/$', 'maiziserver.website.admin.views_career.career_stop', name='career_stop'),
    url(r'^add/$', 'maiziserver.website.admin.views_career.career_add', name='career_add'),
    url(r'^add/do/$', 'maiziserver.website.admin.views_career.career_add_do', name='career_add_do'),
    url(r'^update/$', 'maiziserver.website.admin.views_career.career_update', name='career_update'),
    url(r'^update/do/$', 'maiziserver.website.admin.views_career.career_update_do', name='career_update_do'),

    url(r'^author/$', 'maiziserver.website.admin.views_author.author', name='author'),
    url(r'^author/add/$', 'maiziserver.website.admin.views_author.author_add', name='author_add'),
    url(r'^author/add/do/$', 'maiziserver.website.admin.views_author.author_add_do', name='author_add_do'),
    url(r'^author/update/$', 'maiziserver.website.admin.views_author.author_update', name='author_update'),
    url(r'^author/update/do/$', 'maiziserver.website.admin.views_author.author_update_do', name='author_update_do'),

    url(r'^course/$', 'maiziserver.website.admin.views_course.course', name='course'),
    url(r'^course/add/$', 'maiziserver.website.admin.views_course.course_add', name='course_add'),
    url(r'^course/add/do/$', 'maiziserver.website.admin.views_course.course_add_do', name='course_add_do'),
    url(r'^course/update/$', 'maiziserver.website.admin.views_course.course_update', name='course_update'),
    url(r'^course/update/do/$', 'maiziserver.website.admin.views_course.course_update_do', name='course_update_do'),
    url(r'^course/set/$', 'maiziserver.website.admin.views_course.course_set', name='course_set'),

    url(r'^course/knowledge/$', 'maiziserver.website.admin.views_knowledge.course_knowledge', name='course_knowledge'),
    url(r'^course/knowledge/add/$', 'maiziserver.website.admin.views_knowledge.course_knowledge_add', name='course_knowledge_add'),
    url(r'^course/knowledge/add/do/$', 'maiziserver.website.admin.views_knowledge.course_knowledge_add_do', name='course_knowledge_add_do'),
    url(r'^course/knowledge/update/$', 'maiziserver.website.admin.views_knowledge.course_knowledge_update', name='course_knowledge_update'),
    url(r'^course/knowledge/update/do/$', 'maiziserver.website.admin.views_knowledge.course_knowledge_update_do', name='course_knowledge_update_do'),
    url(r'^course/knowledge/set/$', 'maiziserver.website.admin.views_knowledge.course_knowledge_set', name='course_knowledge_set'),

    url(r'^course/knowledge/item/$', 'maiziserver.website.admin.views_item.course_knowledge_item', name='course_knowledge_item'),
    url(r'^course/knowledge/item/update/$', 'maiziserver.website.admin.views_item.course_knowledge_item_update', name='course_knowledge_item_update'),
    url(r'^course/knowledge/item/update/do/$', 'maiziserver.website.admin.views_item.course_knowledge_item_update_do', name='course_knowledge_item_update_do'),
    url(r'^course/knowledge/item/add/$', 'maiziserver.website.admin.views_item.course_knowledge_item_add', name='course_knowledge_item_add'),
    url(r'^course/knowledge/item/add/do/$', 'maiziserver.website.admin.views_item.course_knowledge_item_add_do', name='course_knowledge_item_add_do'),
    url(r'^course/knowledge/item/set/$', 'maiziserver.website.admin.views_item.course_knowledge_item_set', name='course_knowledge_item_set'),

    url(r'^item/$', 'maiziserver.website.admin.views_item.item', name='item_vedio'),
    url(r'^item/vedio/$', 'maiziserver.website.admin.views_vedio.item_vedio', name='item_vedio'),
    url(r'^item/vedio/add/$', 'maiziserver.website.admin.views_vedio.item_vedio_add', name='item_vedio_add'),
    url(r'^item/vedio/add/do/$', 'maiziserver.website.admin.views_vedio.item_vedio_add_do', name='item_vedio_add_do'),
    url(r'^item/vedio/update/$', 'maiziserver.website.admin.views_vedio.item_vedio_update', name='item_vedio_update'),
    url(r'^item/vedio/update/do/$', 'maiziserver.website.admin.views_vedio.item_vedio_update_do', name='item_vedio_update_do'),

    url(r'^land/$', 'maiziserver.website.admin.views_land.land', name='land'),
    url(r'^land/add/$', 'maiziserver.website.admin.views_land.land_add', name='land_add'),
    url(r'^land/add/do/$', 'maiziserver.website.admin.views_land.land_add_do', name='land_add_do'),
    url(r'^land/update/$', 'maiziserver.website.admin.views_land.land_update', name='land_update'),
    url(r'^land/update/do/$', 'maiziserver.website.admin.views_land.land_update_do', name='land_update_do'),
    url(r'^land/state/$', 'maiziserver.website.admin.views_land.land_state', name='land_state'),
    url(r'^land/course/$', 'maiziserver.website.admin.views_land.land_course', name='land_course'),
    url(r'^land/course/add/$', 'maiziserver.website.admin.views_land.land_course_add', name='land_course_add'),
    url(r'^land/course/add/do/$', 'maiziserver.website.admin.views_land.land_course_add_do', name='land_course_add_do'),
    url(r'^land/course/update/$', 'maiziserver.website.admin.views_land.land_course_update', name='land_course_update'),
    url(r'^land/course/update/do/$', 'maiziserver.website.admin.views_land.land_course_update_do', name='land_course_update_do'),

    url(r'^project/$', 'maiziserver.website.admin.views_project.project', name='project'),
    url(r'^item/project/add/$', 'maiziserver.website.admin.views_project.project_add', name='project_add'),
    url(r'^item/project/add/do/$', 'maiziserver.website.admin.views_project.project_add_do', name='project_add_do'),
    url(r'^item/project/update/$', 'maiziserver.website.admin.views_project.project_update', name='project_update'),
    url(r'^item/project/update/do/$', 'maiziserver.website.admin.views_project.project_update_do', name='project_update_do'),

    url(r'^note/$', 'maiziserver.website.admin.views_note.note', name='note'),
    url(r'^item/note/$', 'maiziserver.website.admin.views_note.item_note', name='item_note'),
    url(r'^item/note/add/$', 'maiziserver.website.admin.views_note.item_note_add', name='note_add'),
    url(r'^item/note/add/do/$', 'maiziserver.website.admin.views_note.item_note_add_do', name='note_add_do'),
    url(r'^item/note/update/$', 'maiziserver.website.admin.views_note.item_note_update', name='item_note_update'),
    url(r'^item/note/update/do/$', 'maiziserver.website.admin.views_note.item_note_update_do', name='item_note_update_do'),

    url(r'^book/$', 'maiziserver.website.admin.views_book.book', name='book'),
    url(r'^book/add/$', 'maiziserver.website.admin.views_book.book_add', name='book_add'),
    url(r'^book/add/do/$', 'maiziserver.website.admin.views_book.book_add_do', name='book_add_do'),

)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
