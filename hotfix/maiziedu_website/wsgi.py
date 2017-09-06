"""
WSGI config for maiziedu_website project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os

env = os.environ.get("ENV", "local")

if env == "prod":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
elif env == "staging":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
elif env == "local":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "maiziedu_website.settings")
else:
    raise Exception("error environ: ENV=%s" % env)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
