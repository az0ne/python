# -*- coding: utf-8 -*-

import os
from .base import *
from .third_party_settings import *


DEBUG = True
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [
    # wangqi vpn
    "47.89.185.208",
    # 公司ip
    "182.150.24.249"]

DISABALED_SMS_LIST = ['classmeeting_notify','classmeeting_absence','student_deadline_quit','studying_reminder']

SESSION_COOKIE_DOMAIN = '.microoh.com'
SESSION_COOKIE_NAME = 'microoh'
CSRF_COOKIE_DOMAIN = '.microoh.com'

SITE_URL = "http://dev.microoh.com:99"  # 站点URL

# 手机站点域名
MOBILE_SITE = 'http://m.microoh.com:99'

IS_SEND_MESSAGE = True
IS_IOS_CHECK = False
IOS_CHECK_VERSION = '11'
SEND_SMS_URL = 'http://10.117.185.66:39000/'  # 信息系统推送地址
MOBILE_WHITELIST = ['18010539905', '18109050401', '18202828236', '18612982027', '17710000011',
                    '18215559962', '18380284010', '15982827609', '13880367011', '18780268772', '13980672006',  # 短信白名单
                    '13881973240']  # 短信白名单

########### mongodb日志工具配置
MZ_LOG_TO_MONGODB={
    "host": "127.0.0.1",
    "port": 27017,
    #"username": "admin",
    #"password": "maiziedu0922",
    "username": "",
    "password": "",
    "database": "maiziedu_log",
    "collection":'log',
    "level": 'INFO'
}


# redis配置
BROKER_URL = 'redis://127.0.0.1:6379/14'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
# celery
import djcelery

djcelery.setup_loader()


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
MQ_ADDR = "http://10.117.185.66:37001/"
QUEUE_NAME = "devmainqueue"

SENSITIVE_WORD_FILTER_URL = 'http://10.117.185.66:35000/filter/'
SNAP_SERVICE_ADDR = "http://10.117.185.66:34000"

PROJECT_DOWN_DOMAIN = "http://121.41.96.44:33000/download/"
