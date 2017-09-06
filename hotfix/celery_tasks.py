# -*- coding: utf-8 -*-
__author__ = 'qxoo'

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")

app = Celery('maiziedu')
app.config_from_object('django.conf:settings')

INSTALLED_APPS = ['mz_user.views',
                  'utils.sms_manager',
                  'mz_lps3.views_teacher_gt']
app.autodiscover_tasks(lambda: INSTALLED_APPS)