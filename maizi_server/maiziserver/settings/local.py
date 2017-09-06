# -*- coding: utf-8 -*-

from .base import *

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + (
    "maiziserver.middleware.debug.DebugMiddleWare",)

# 新的数据库连接池管理需要的配置
MYSQL_HOST = "rm-bp1q9x0s7w5igdb75o.mysql.rds.aliyuncs.com"
MYSQL_PORT = 3306
MYSQL_USER = "dev"
MYSQL_PASSWORD = "65fg_weArd"
MYSQL_DB = "dev_account_center"
MYSQL_POOL_NAME = "db_pool"
MYSQL_POOL_SIZE = 1
MYSQL_POOL_WAIT_SECONDS = 3
MYSQL_POOL_OVERFLOW = 1

# SESSION_REDIS_HOST = '192.168.1.59'
SESSION_REDIS_HOST = '127.0.0.1'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0
# SESSION_REDIS_PASSWORD = ""
SESSION_REDIS_PREFIX = 'session'
SESSION_REDIS_SOCKET_TIMEOUT = 1

STATIC_ROOT = "/root/maiziserver/static/"

STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),)

UPLOAD_DOCUMENT_DIRS = (os.path.join(BASE_DIR, 'uploads/document/'))

MAIZISERVERDB = 'dev_account_center'
MAIZILPSDB = 'dev_lps_20170707'

# db for test only
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3'
    }
}
