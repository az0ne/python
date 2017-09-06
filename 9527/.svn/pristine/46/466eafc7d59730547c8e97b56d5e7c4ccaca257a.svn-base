from django.conf.urls import patterns, url

urlpatterns = patterns("mz_operation.views",
                       url(r'^operation/list/$', "query_userclass", name="query_userclass"),
                       url(r'^operation/stage/$', "class_stage", name="class_stage"),
                       url(r'^operation/change/$', "change_stage", name="change_stage"),
                       url(r'^operation/deadline/$', "classdeadline", name="classdeadline"),
                       url(r'^operation/updeadline/$', "updeadline", name="updeadline"),
                       url(r'^charts/bar_charts/$', "charts", {'chart_type': 'bar'}, name="bar_charts"),
                       url(r'^charts/line_charts/$', "charts", {'chart_type': 'line'}, name="line_charts"),
                       url(r'^charts/data/$', "get_charts_data", name="get_charts_data"),
                       url(r'^charts/line_charts/equation_options/$', "equation_options", name="equation_options"),
                       url(r'^charts/excel_import/$', "execl_import", name="execl_import"),
                       url(r'^new_student/list/$', "new_student_render", name="new_student_list"),
                       url(r'^charts/funnel_charts/', "test_funnel_charts", name="funnel_charts"),
                       url(r'^charts/sale_line_charts/', "sale_line_chart", name="sale_line_charts"),
                       url(r'^charts/funnel_chart_ajax/', "funnel_chart_ajax", name="funnel_chart_ajax"),
                       url(r'^charts/user_chart_ajax/', "user_chart_ajax", name="user_chart_ajax"),
                       )
