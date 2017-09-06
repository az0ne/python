# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from mz_fxsys import user_views, order_views, payments_views, total_revenue_views, db_tools

# user_urls
urlpatterns = patterns('',
                       url(r'user/add/$', user_views.add_user, name="add_user"),
                       url(r'user/update/$', user_views.update_user, name="edit_user"),
                       url(r'user/del/$', user_views.del_user, name="del_user"),
                       url(r'user/list/$', user_views.get_user_list, name="get_user"),
                       url(r'user/activate/ajax/$', user_views.update_activate, name="update_activate"),
                       url(r'user/get_all/ajax/$', user_views.get_all_user, name="get_all_user_ajax"),
                       url(r'user/validate_exist/ajax/$', user_views.validate_user_exist_by_username,
                           name="validate_user_exist"),
                       )
# order_urls
urlpatterns += patterns('',
                        url(r'order/list/$', order_views.get_order_list, name="get_order"),
                        url(r'order/update/$', order_views.update_order, name="edit_order"),
                        url(r'order/add/$', order_views.add_order, name="add_order"),
                        url(r'order/del/$', order_views.del_order, name="del_order"),
                        url(r'order/validate_exist/ajax/$', order_views.validate_order_No_exist,
                            name="validate_order_No_exist"),
                        url(r'order/all_orderNo/ajax/$', order_views.get_order_all, name="get_order_all"),
                        )
# payments_urls
urlpatterns += patterns('',
                        url(r'payments/list/$', payments_views.get_payments_list, name="get_payments"),
                        url(r'payments/add/$', payments_views.add_payments, name="add_payments"),
                        # url(r'payments/update/$', payments_views.update_payments, name="edit_payments"),
                        url(r'payments/del/$', payments_views.del_payments, name="del_payments"),
                        )

# total_revenue_urls
urlpatterns += patterns('',
                        url(r'totalRevenue/list/$', total_revenue_views.get_total_revenue_list, name="get_total_revenue"),
                        url(r'totalRevenue/add/$', total_revenue_views.add_total_revenue, name="add_total_revenue"),
                        url(r'totalRevenue/del/$', total_revenue_views.del_total_revenue, name="del_total_revenue"),
                        )
# rebate_type_urls
urlpatterns += patterns('mz_fxsys.rebate_type_views',
                        url(r'rebate_type/list/$', 'get_rebate_type_list', name="get_rebate_type_list"),
                        url(r'rebate_type/add/$', 'rebate_type_add', name="rebate_type_add"),
                        url(r'rebate_type/edit/(?P<rebate_type_id>\d+)/$', 'rebate_type_edit', name="rebate_type_edit"),
                        url(r'rebate_type/del/$', 'rebate_type_del', name="rebate_type_del"),
                        )
