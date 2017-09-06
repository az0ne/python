from django.conf.urls import patterns, url



urlpatterns = patterns("mz_wiki.wiki_course_type",
                        url(r'^wikiCourseType/save/$', 'wikiCourseType_save', name='wikiCourseType_save'),
                        url(r'^wikiCourseType/edit/$', 'wikiCourseType_edit', name='wikiCourseType_edit'),
                        url(r'^wikiCourseType/list/$', 'wikiCourseType_list', name='wikiCourseType_list'),
                        url(r'^wikiCourseType/isHaveShortName/$', 'wikiCourseType_isHaveTheShortName', name='wikiCourseType_isHaveTheShortName'),
                        )

urlpatterns += patterns("mz_wiki.wiki_course",
                        url(r'^wikiCourse/save/$', 'wikiCourse_save', name='wikiCourse_save'),
                        url(r'^wikiCourse/edit/$', 'wikiCourse_edit', name='wikiCourse_edit'),
                        url(r'^wikiCourse/list/$', 'wikiCourse_list', name='wikiCourse_list'),
                        url(r'^wikiCourse/isHaveShortName/$', 'wikiCourse_isHaveTheShortName', name='wikiCourse_isHaveTheShortName'),
                        )

urlpatterns += patterns("mz_wiki.wiki_chapter",
                        url(r'^wikiCourse/wikiChapter_save/$', 'wikiChapter_save', name='wikiChapter_save'),
                        url(r'^wikiCourse/wikiChapter_edit/$', 'wikiChapter_edit', name='wikiChapter_edit'),
                        url(r'^wikiCourse/wikiChapter_list/$', 'wikiChapter_list', name='wikiChapter_list'),
                        )

urlpatterns += patterns("mz_wiki.wiki_item",
                        url(r'^wikiCourse/wikiItem_save/$', 'wikiItem_save', name='wikiItem_save'),
                        url(r'^wikiCourse/wikiItem_edit/$', 'wikiItem_edit', name='wikiItem_edit'),
                        url(r'^wikiCourse/wikiItem_list/$', 'wikiItem_list', name='wikiItem_list'),
                        url(r'^wikiCourse/wikiItem_contentSave/$', 'wikiItem_content_save', name='wikiItem_content_save'),
                        url(r'^wikiCourse/wikiItem_isHaveShortName/$', 'wikiItem_isHaveTheShortName', name='wikiItem_isHaveTheShortName'),
                        )

urlpatterns += patterns("mz_wiki.wiki_seo",
                        url(r'^wikiCourse/wikiSEO_save/$', 'wiki_SEO_save', name='wikiSEO_save'),
                        url(r'^wikiCourse/wikiSEO_edit/$', 'wiki_SEO_edit', name='wikiSEO_edit'),
                        )