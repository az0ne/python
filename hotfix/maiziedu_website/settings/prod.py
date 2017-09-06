# -*- coding: utf-8 -*-

from .base import *
from .third_party_settings import *

DEBUG = False
TEMPLATE_DEBUG = False

CORS_ORIGIN_WHITELIST = ('q.maiziedu.com','tongji.baidu.com','baidu.com','google.com')
X_FRAME_OPTIONS = 'ALLOW-FROM http://tongji.baidu.com/'

SESSION_COOKIE_DOMAIN = '.maiziedu.com'
SESSION_COOKIE_NAME = 'maiziedu'
CSRF_COOKIE_DOMAIN = '.maiziedu.com'
CORS_ALLOW_CREDENTIALS = True

SITE_URL = "http://www.maiziedu.com"  # 站点URL
BBS_SITE_URL = "http://forum.maiziedu.com"  #论坛URL
OLD_SITE_URL = "http://old.maiziedu.com"  #老网站的URL地址

ADMINS = (
    ('bobby', 'bobby@maiziedu.com'),
    ('steve.yi', 'steve.yi@maiziedu.com')
)

#app客户端下载地址配置
ANDROID_DOWN_URL = "http://www.maiziedu.com/app/download/"
IOS_DOWN_URL = "https://itunes.apple.com/cn/app/mai-zi-xue-yuan-it-zai-xian/id914713849?mt=8"
WINPHONE_DOWN_URL = "http://www.windowsphone.com/zh-cn/store/app/%E9%BA%A6%E5%AD%90%E5%AD%A6%E9%99%A2-it%E5%9C%A8%E7%BA%BF%E6%95%99%E8%82%B2%E5%AD%A6%E4%B9%A0%E5%B9%B3%E5%8F%B0/7c8e2267-8d1a-43c1-af32-153528266d77"
IPAD_DOWN_URL = "https://itunes.apple.com/cn/app/mai-zi-xue-yuanhd-it-zai-xian/id939932392?mt=8"

NEWEST_ANDROID_APP = 'Maiziedu_release_v4.3.1.apk'

# app推送开关
IS_SEND_MESSAGE = True
SEND_SMS_URL = 'http://100.114.69.8/'  # 信息系统推送地址
# MOBILE_WHITELIST = ['18109050401', '18202828236', '18612982027', '17710000011', '15608071871', '13980530592', '13880367011']  # 短信白名单

# ios审核
IS_IOS_CHECK = True
IOS_CHECK_VERSION = '12'

FPS_SWITCH = True
FPS_HOST = "http://q.maiziedu.com/"
FPS_API = FPS_HOST + "common/interface/"
FPS_CENTER = FPS_HOST + "common/dynmsg/"

############# lps2.0 日志设置 ######################
CLASS_STU_LOG_ROOT = '/var/www/maiziedu.com/log/class_stu_log/'
CALC_VIEW_LOG_PATH = '/var/www/maiziedu.com/log/calc_views.log'
CLASS_MEETING_TASK = '/var/www/maiziedu.com/log/class_meeting_task.log'
BACKEND_CALC_3S_PATH = '/var/www/maiziedu.com/log/tornado_per_3s.log'
BACKEND_CALC_3M_PATH = '/var/www/maiziedu.com/log/tornado_per_3m.log'
BACKEND_CALC_30M_PATH = '/var/www/maiziedu.com/log/tornado_per_30m.log'

#在线编程url(1:python, 2:php)
ONLINE_CODE_URL = {1: 'http://123.56.136.227:22200/course/onlinecode/',
                   2: 'http://123.56.136.227:22201/course/onlinecode/'}


######### 么分期相关参数设置 开始 #############
MIME_PAY_URL = "https://wap.memedai.cn/merchantApp/merchant/open/submitOrder/maizi"
MIME_PAY_APPID = 'ff2c461eed9a504f97081059190ee33a'
MIME_PAY_KEY = '858b329e68c0f5174d91994e18e521184b38fc88959462e33da8d4e2f9c4edd1'

GUIDE_TASK_ID = 2

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}  #日志格式
    },
    'filters': {
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/www/maiziedu.com/log/all.log',     #日志输出文件
            'maxBytes': 1024*1024*5,                  #文件大小
            'backupCount': 5,                         #备份份数
            'formatter':'standard',                   #使用哪种formatters日志格式
        },
        'error': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/www/maiziedu.com/log/error.log',
            'maxBytes':1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
            },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/www/maiziedu.com/log/script.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
            },
        'scprits_handler': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'/var/www/maiziedu.com/log/script.log',
            'maxBytes': 1024*1024*5,
            'backupCount': 5,
            'formatter':'standard',
            }
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'DEBUG',
            'propagate': False,
            },
        'scripts': {
            'handlers': ['scprits_handler'],
            'level': 'INFO',
            'propagate': False
        },
        'mz_common.views': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': True
        },
        'mz_course.views': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': True
        },
        'mz_lps.views': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': True
        },
	'mz_lps2.views': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': True
        },
        'mz_pay.views': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': True
        },
        'mz_user.views': {
            'handlers': ['default', 'error'],
            'level': 'ERROR',
            'propagate': True
        },
	'mz_service.views': {
            'handlers': ['default', 'error'],
            'level': 'ERROR',
            'propagate': True
        },
        'mz_backend.views': {
            'handlers': ['default', 'error'],
            'level': 'ERROR',
            'propagate': True
        },
        'mz_lps2.teacher_views': {
            'handlers': ['default', 'error'],
            'level': 'DEBUG',
            'propagate': True
        },
        'utils.tool': {
            'handlers': ['default', 'error'],
            'level': 'ERROR',
            'propagate': True
        },
        'mz_lps2.signal_view': {
            'handlers': ['default', 'error'],
            'level': 'ERROR',
            'propagate': True
        },
        'mz_user.signal_view': {
            'handlers': ['default', 'error'],
            'level': 'ERROR',
            'propagate': True
        },
    }
}


MZ_LOG_TO_MONGODB={
    "host": "127.0.0.1",
    "port": 27017,
    "username": "admin",
    "password": "maiziedu0922",
    "database": "maiziedu_log",
    "collection":'log',
    "level": 'INFO'
}

import logging
logging.basicConfig(format='%(asctime)s %(message)s ---------- %(pathname)s:%(module)s.%(funcName)s Line:%(lineno)d',
                    datefmt='%Y-%m-%d %H:%M:%S', level=logging.WARNING)



## redis配置
BROKER_URL = 'redis://:da5IF2dvmC97r@ae3e57c88d3b43d0.m.cnhza.kvstore.aliyuncs.com:6379/14'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
## celery
import djcelery
djcelery.setup_loader()


CACHE_TIME = 3600

# 定义缓存
CACHES = {
"default": {
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": "redis://:da5IF2dvmC97r@ae3e57c88d3b43d0.m.cnhza.kvstore.aliyuncs.com:6379/0",
    "OPTIONS": {
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
    }
},
"queue": {
    "BACKEND": "django_redis.cache.RedisCache",
    "LOCATION": "redis://:da5IF2dvmC97r@ae3e57c88d3b43d0.m.cnhza.kvstore.aliyuncs.com:6379/14",
    "OPTIONS": {
        "CLIENT_CLASS": "django_redis.client.DefaultClient",
    }
}
}

# 新的数据库连接池管理需要的配置
MYSQL_HOST = DATABASES['default']['HOST']
MYSQL_PORT = int(DATABASES['default']['PORT'])
MYSQL_USER = DATABASES['default']['USER']
MYSQL_PASSWORD = DATABASES['default']['PASSWORD']
MYSQL_DB = DATABASES['default']['NAME']
MYSQL_POOL_NAME = "db_pool"
MYSQL_POOL_SIZE = 1
MYSQL_POOL_WAIT_SECONDS = 4
MYSQL_POOL_OVERFLOW = 1

REDIS_HOST = rds_host
REDIS_PORT = int(rds_port)
REDIS_CACHE_PREFIX = "cache"
REDIS_POOL_SIZE = 1
REDIS_PASSWORD = rds_password
CACHE_PREFIX = "db_cache"
ENABLE_DATA_CACHE = True

MONGO_HOST = mongodb_host
MONGO_PORT = int(mongodb_port)

# mq
MQ_ADDR = "http://100.114.117.161/"
QUEUE_NAME = "mainqueue"

SENSITIVE_WORD_FILTER_URL = 'http://100.114.69.178/filter/'
SNAP_SERVICE_ADDR = "http://100.114.116.146"

PROJECT_DOWN_DOMAIN = "https://download.maiziedu.com/download/"
