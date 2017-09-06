# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView
from mz_pay import views

urlpatterns = patterns('',
                       url(r'^go/(?P<careercourse_id>[\d]+)/(?P<pay_type>[\d]{1})/(?P<class_coding>[^/]*)/(?P<service_provider>[\d]{1,2})/(?P<other>[\w]+)/(?P<has_discount>[\d]{1})/$', views.goto_pay, name="goto_pay"),

                       url(r'^alipay/return/$', views.alipay_return,name="alipay_return"),
                       url(r'^alipay/notify/$', views.alipay_notify,name="alipay_notify"),
                       url(r'^alipay/appnotify/$', views.alipay_app_notify,name="alipay_app_notify"),

                       url(r'^$', views.pay_view, name='pay_view'),
                       url(r'^get/class/list/$', views.get_class_list_by_career_id, name='get_class_list_by_career_id'),

                       url(r'^wechat/pay/return/$', views.wechat_pay,name="wechat_pay"),
                       url(r'^wechat/(?P<order_no>[\d]+)/$', views.generate_qrcode,name="wechat_pay_qrcode"),
                       url(r'^wechat/order_status/(?P<order_no>[\d]+)/$', views.query_trade_status,name="wechat_order_status"),
                       url(r'^wechat/paysuccess/(?P<order_no>[\d]+)/$', views.render_success_view,name="wechat_pay_success"),

                       url(r'^goto_onepay/$', views.goto_onepay,name="goto_onepay"),
                       url(r'^view/$', views.pay_view3, name='pay_view2'),

                       url(r'^mime/contract/$', TemplateView.as_view(template_name="mz_pay/agreement.html"), name="mime_contract"),
                       url(r'^memedai/notify/$', views.mimepay_notify, name="mimepay_notify"),

                       url(r'^union/return/$', views.union_return, name="union_return"),
                       url(r'^union/notify/$', views.union_notify, name="union_notify"),

                       url(r'^fql/return/$', views.fen_qi_le_return, name="fen_qi_le_return"),
                       url(r'^fql/notify/$', views.fen_qi_le_notify, name="fen_qi_le_notify"),

                       url(r'^yee/return/$', views.yee_pay_return, name="yee_pay_return"),
                       url(r'^yee/notify/$', views.yee_pay_notify, name="yee_pay_notify"),

                       url(r'^uubee/return/$', views.uubee_pay_return, name="uubee_pay_return"),
                       url(r'^uubee/notify/$', views.uubee_pay_notify, name="uubee_pay_notify"),
					   
					   # WAP端支付需要的URL
                       url(r'^alipay/wap_return/(?P<career_course_short_name>.*?)/$', views.wap_alipay_return, name="wap_alipay_return"),

)