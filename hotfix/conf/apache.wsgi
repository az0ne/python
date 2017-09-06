import os, sys
os.environ["PYTHON_EGG_CACHE"] = "/tmp"
sys.path.append('/home/maiziedu/Code/20150611')
os.environ['DJANGO_SETTINGS_MODULE'] = 'maiziedu_website.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
