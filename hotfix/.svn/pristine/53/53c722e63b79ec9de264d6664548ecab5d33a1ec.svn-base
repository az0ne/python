try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

urlpatterns = patterns(
    'geetest.views',
    url(r'getcaptcha/(?P<geetest_type>[\w]+)/$', 'getcaptcha', name='getcaptcha'),
    url(r'getcaptcha/$', 'getcaptcha', name='getcaptcha'),
    url(r'validate/$', 'validate', name='validate'),
)