# -*- coding: utf-8 -*-

from .base import *
from .third_party_settings import *


ALLOWED_HOSTS = ['*']
# 站点URL
SITE_URL = "http://192.168.1.142"

# SESSION_COOKIE_DOMAIN = '.test.com'
SESSION_COOKIE_NAME = 'test'
# CSRF_COOKIE_DOMAIN = '.test.com'

DEBUG = True
TEMPLATE_DEBUG = True

DISABALED_SMS_LIST = ['classmeeting_notify','classmeeting_absence','student_deadline_quit','studying_reminder']

# 缓存保存时间
CACHE_TIME = 1

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.1.142:6379/0",
        "OPTIONS": {

            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dev_lps_20170820a',
        'USER': 'dev',
        'PASSWORD': '65fg_weArd',
        'HOST': 'rm-bp1q9x0s7w5igdb75o.mysql.rds.aliyuncs.com',
        'PORT': '',
    },

    'fps': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fps_20160505',
        'USER': 'maizi',
        'PASSWORD': 'maizi123',
        "HOST": '192.168.1.142',
    },
}

# mongodb日志工具配置
MZ_LOG_TO_MONGODB = {
    "host": '192.168.1.142',
    "port": 27017,
    "username": "admin",
    "password": "maiziedu0922",
    "database": "maiziedu_log",
    "collection": 'log',
    "level": 'INFO'
}


# 新的数据库连接池管理需要的配置
MYSQL_HOST = DATABASES['default']['HOST']
MYSQL_PORT = 3306
MYSQL_USER = DATABASES['default']['USER']
MYSQL_PASSWORD = DATABASES['default']['PASSWORD']
MYSQL_DB = DATABASES['default']['NAME']
MYSQL_POOL_NAME = "db_pool"
MYSQL_POOL_SIZE = 1
MYSQL_POOL_WAIT_SECONDS = 4
MYSQL_POOL_OVERFLOW = 1

REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_CACHE_PREFIX = "cache"
REDIS_POOL_SIZE = 8
REDIS_PASSWORD = None

CACHE_PREFIX = "db_cache"
ENABLE_DATA_CACHE = True

MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017

del STATIC_ROOT

MEDIA_URL = 'http://www.maiziedu.com/uploads/'
# STATIC_URL = 'http://www.maiziedu.com/static/'

SEND_SMS_URL = 'http://121.41.96.44:39000/'  # 信息系统推送地址
MOBILE_WHITELIST = ['18010539905', '18109050401', '18202828236', '18612982027',
                    '17710000011', '18780268772', '15982827609']  # 短信黑名单
IS_SEND_MESSAGE = True

# mq
MQ_ADDR = "http://115.28.92.81:8000/"
QUEUE_NAME = "devmainqueue"
SENSITIVE_WORD_FILTER_URL = 'http://121.41.96.44:8888/filter/'

SNAP_SERVICE_ADDR = "http://121.41.96.44:34000"