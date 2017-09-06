from django.conf.urls import patterns, url

urlpatterns = patterns("mz_back.role",
                        url(r'^role/save/$', 'role_save', name='role_save'),
                        url(r'^role/edit/$', 'role_edit', name='role_edit'),
                        url(r'^role/list/$', 'role_list', name='role_list'),
                        url(r'^role/role_menu_save/$', 'role_menu_save', name='role_menu_save'),
                        url(r'^role/isHaveTheName/', 'role_isHaveTheName', name='role_isHaveTheName'),
                        url(r'^role/role_menus/$', 'get_had_menus_by_role_id', name='had_menus_list'),
                        )

urlpatterns += patterns("mz_back.menu",
                        url(r'^menu/save/$', 'menu_save', name='menu_save'),
                        url(r'^menu/edit/$', 'menu_edit', name='menu_edit'),
                        url(r'^menu/list/$', 'menu_list', name='menu_list'),
                        )

urlpatterns += patterns("mz_back.views",
                        # url(r'^AdminUsr/login/$', 'admin_login', name='admin_login'),
                        # url(r'^AdminUsr/logout/$', 'admin_logout', name='admin_logout'),
                        url(r'^AdminUsr/save/$', 'admin_save', name='admin_save'),
                        url(r'^AdminUsr/edit/$', 'admin_edit', name='admin_edit'),
                        url(r'^AdminUsr/list/$', 'admin_list', name='admin_list'),
                        url(r'^AdminUsr/admin_role_save/$', 'admin_role_save', name='admin_role_save'),
                        # url(r'^AdminUsr/is_had_user/$', 'is_had_the_user', name='is_had_the_user'),
                        )

urlpatterns += patterns("mz_back.employ_teacher",
                        url(r'^employ_teacher/list/$', 'employ_teacher', name="employteacher"),
                        url(r'^employ_teacher/show/$', 'employ_teacher_edit', name='employ_teacher_edit'),
                        )

urlpatterns += patterns("mz_back.try_learn_views",
                        url(r'^try_learn/list/$', 'try_learn_list', name="try_learn_list"),
                        url(r'^try_learn/detail/$', 'try_learn_detail', name='try_learn_detail'),
                        )


