# -*- coding: utf-8 -*-

__author__ = 'Jackie'


def load():
    import os
    import sys
    import django
    sys.path.append('/var/www/maiziedu.com/')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
    django.setup()
