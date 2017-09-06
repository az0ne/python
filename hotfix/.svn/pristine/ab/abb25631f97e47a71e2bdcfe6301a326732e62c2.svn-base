# -*- coding: utf-8 -*-
"""
if you want see settings in old version, please see ./bak_settings.py
"""

import socket
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# Build paths inside the project like this: os.path.join(PROJECT_ROOT, ...)

import os

PROJECT_ROOT = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.pardir, os.pardir).replace('\\', '/')

# app and lib settings
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'extra_apps'))
sys.path.insert(0, os.path.join(PROJECT_ROOT, 'libs'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_r&eypnc%rp1f5slops98fwqayc0!ze_nb^06g55%2^9)hq049'

ALLOWED_HOSTS = ['*']

MAINTENANCE_MODE = False

# template setting
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates').replace('\\', '/'),
)


# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captcha',
    'corsheaders',
    'xadmin',
    'crispy_forms',
    'reversion',
    'mz_user',
    'mz_pay',
    'mz_common',
    'mz_course',
    'mz_lps',
    'aca_course',
    'mz_lps2',
    'mz_lps3',    
    'fps_interface',
    'rest_framework',
    'mz_eduadmin',
    'mz_eduadmin.stats',    
    'mz_service',
    'geetest',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'mz_common.middleware.SyncLoginMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'maintenancemode.middleware.MaintenanceModeMiddleware',
)

# 共用上下文处理器定义
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'mz_common.views.common_context',
)


REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',),
    'PAGINATE_BY': 20
}


CORS_ORIGIN_WHITELIST = ('localhost:8000', 'localhost:8081')

ROOT_URLCONF = 'maiziedu_website.urls'

WSGI_APPLICATION = 'maiziedu_website.wsgi.application'


# Internationalization

LANGUAGE_CODE = 'zh-cn'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False
DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i'
TIME_FORMAT = 'H:i'

# 静态文件地址映射
STATIC_URL = '/static/'

IS_MOBILE = bool(os.getenv("IS_MOBILE", False))

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')

JS_DIRS = os.path.join(PROJECT_ROOT, 'js').replace('\\', '/')
JSNEW_DIRS = os.path.join(PROJECT_ROOT, '2016').replace('\\', '/')
CSS_DIRS = os.path.join(PROJECT_ROOT, 'css').replace('\\', '/')
IMAGE_DIRS = os.path.join(PROJECT_ROOT, 'images').replace('\\', '/')


STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static').replace('\\', '/'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# 媒体地址映射
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'uploads').replace('\\', '/')

PAGES_DIRS = os.path.join(PROJECT_ROOT, 'pages').replace('\\', '/')

# IMAGEKIT缩略图路径
IMAGEKIT_CACHEFILE_DIR = 'avatar/thumbnall'

# 用户Model设置
AUTH_USER_MODEL = 'mz_user.UserProfile'

# 自定义登录验证
AUTHENTICATION_BACKENDS = (
    'mz_user.auth.CustomBackend',
)

# 邮件配置
EMAIL_HOST = "smtp.exmail.qq.com"
EMAIL_PORT = 25
EMAIL_HOST_USER = "admin@maiziedu.com"
EMAIL_HOST_PASSWORD = "85ecbH0H"
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = "[麦子学院]"
EMAIL_FROM = "maiziedu<admin@maiziedu.com>"
EMAIL_COUNT = 50  # 同IP一天内最大邮件发送条数
# 管理员站点
SERVER_EMAIL = 'admin@maiziedu.com'  # The email address that error messages come from, such as those sent to ADMINS and MANAGERS.

# 全文检索api_url
SEARCH_API_URL = 'http://100.114.117.0/search/'
SEARCH_KEYWORD_LENGTH = 64

#wap端落地页数据
WAP_AD_URL = "http://www.maiziedu.com/pages/adwap/"

SITE_URL = "http://www.maiziedu.com"  # 站点URL
BBS_SITE_URL = "http://www.maiziedu.com:8800"  # 论坛URL
OLD_SITE_URL = "http://182.140.231.108"  # 老网站的URL地址
QC_FOLDER = 'qrcodes/'

# 手机站点域名
MOBILE_SITE = 'http://m.maiziedu.com'

# 验证码设置
CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
CAPTCHA_OUTPUT_FORMAT = u'%(text_field)s %(hidden_field)s &nbsp;%(image)s'
CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_arcs', 'captcha.helpers.noise_dots')
CAPTCHA_BACKGROUND_COLOR = '#ffffff'
CAPTCHA_LENGTH = 6


# 常用正则表达式
REGEX_EMAIL = "[^\._-][\w\.-]*@(?:[A-Za-z0-9]+\.)+[A-Za-z]+$"  # Email正则表达式
REGEX_MOBILE = "^1[3578]\d{9}$|^14[57]\d{8}$"  # 手机号正则表达式
REGEX_QQ = "^\d{5,12}$"

# 常用分页大小设置
COURSE_LIST_PAGESIZE = 16
# 全局分页大小设置
GLOBAL_PAGESIZE = 8
# 搜索结果分页
SEARCH_PAGESIZE = 10
# 排行分页大小设置
RANKING_PAGESIZE = 10
# 评论分页大小设置
COMMENT_PAGESIZE = 10
# 我的消息分页大小设置
MYMESSAGE_PAGESIZE = 10
# 独立课程的默认颜色
DEFAULT_COLOR = "red"

# 文件上传设置
AVATAR_SIZE_LIMIT = 1024  # KB,头像上传大小限制
AVATAR_SUFFIX_LIMIT = "*.gif; *.jpg; *.jpeg; *.png; *.bmp;"     #头像上传格式后缀限制

JOB_SUFFIX_LIMIT = "*.zip; *.rar;"
JOB_SIZE_LIMIT = 51200

# app客户端下载地址配置
ANDROID_DOWN_URL = "http://old.maiziedu.com/app/download.php"
IOS_DOWN_URL = "https://itunes.apple.com/cn/app/mai-zi-xue-yuan-it-zai-xian/id914713849?mt=8"
WINPHONE_DOWN_URL = "http://www.windowsphone.com/zh-cn/store/app/%E9%BA%A6%E5%AD%90%E5%AD%A6%E9%99%A2-it%E5%9C%A8%E7%BA%BF%E6%95%99%E8%82%B2%E5%AD%A6%E4%B9%A0%E5%B9%B3%E5%8F%B0/7c8e2267-8d1a-43c1-af32-153528266d77"
IPAD_DOWN_URL = "https://itunes.apple.com/cn/app/mai-zi-xue-yuanhd-it-zai-xian/id939932392?mt=8"

# 课程相关参数配置
VIDEO_EXAM_COMPLETE = 0.95  # 视频完成度开始考试
DEFAULT_HOMEWORK = "这是默认的课后作业，赶快帮老师课堂讲的代码做一遍提交上来吧"  # 默认课后作业文案

# LPS相关设置项
LESSON_EXAM_RATE = 0.1  # 随堂测验占总分比例
COURSE_EXAM_RATE = 0.1  # 课程总测验占总分比例
PROJECT_EXAM_RATE = 0.8  # 项目占总分比例
NOPROJECT_LESSON_EXAM_RATE = 0.5  # 随堂测验占总分比例
NOPROJECT_COURSE_EXAM_RATE = 0.5  # 课程总测验占总分比例

HAS_2_EXAM_RATE = 0.5  # 只有2个测验项的各自比重
HAS_1_EXAM_RATE = 1  # 只有1个测验项的各自比重



########### 正在审核中的版本号 开始  #########
IPADVERSION = '2.0.0'
IOSVERSION = '3'
########### 正在审核中的版本号 结束  #########

########### 最新android app名称 开始 ############
NEWEST_ANDROID_APP = 'Maiziedu_release_v2.0.0_official.apk'
########### 最新android app名称 结束 ############


# 在线编程url(1:python, 2:php)
ONLINE_CODE_URL = {1: 'http://192.168.1.142:8000/course/onlinecode/',
                   2: 'http://192.168.1.142:22201/course/onlinecode/'}



# 缓存保存时间
CACHE_TIME = 1

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {

            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


FPS_SWITCH = False
FPS_HOST = "http://q.142.com/"
FPS_API = FPS_HOST + "group/common/interface/"
FPS_CENTER = FPS_HOST + "group/common/dynmsg/"

# 麦子学院接口
MAIZI_KEY = 'f5slops9'
KEY_EXPIRE_SECONDS = 60 * 60 * 1

DISCUZZ_PROVIDER = "LPS"


# 要使用log时直接从此处调用
from mz_platform.utils.log_tool import SYSLOGGER, BIZLOGGER, ACSLOGGER
sys_logger = SYSLOGGER
biz_logger = BIZLOGGER
acs_logger = ACSLOGGER

GUIDE_TASK_ID = 1278

DISABALED_SMS_LIST = []


import dotenv
dotenv.load("/var/www/maiziedu.com/maiziedu_website/settings/deploy_env")
db_default_name = os.environ.get("DB_DEFAULT_NAME", "")
db_default_user = os.environ.get("DB_DEFAULT_USER", "")
db_default_password = os.environ.get("DB_DEFAULT_PASSWORD", "")
db_default_host = os.environ.get("DB_DEFAULT_HOST", "")
db_default_port = os.environ.get("DB_DEFAULT_PORT", "3306")


db_fps_dbname = os.environ.get("DB_FPS_NAME", "")
db_fps_user = os.environ.get("DB_FPS_USER", "")
db_fps_password = os.environ.get("DB_FPS_PASSWORD", "")
db_fps_host = os.environ.get("DB_FPS_HOST", "")
db_fps_port = os.environ.get("DB_FPS_PORT", "3306")

rds_host = os.environ.get("RDS_HOST", "")
rds_port = os.environ.get("RDS_PORT", "6379")
rds_password = os.environ.get("RDS_PASSWORD", None)
mongodb_host = os.environ.get("MONGODB_HOST", "")
mongodb_port = os.environ.get("MONGODB_PORT", "27017")
mongodb_password = os.environ.get("MONGODB_PASSWORD", None)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db_default_name,
        'USER': db_default_user,
        'PASSWORD': db_default_password,
        'HOST': db_default_host,
        'PORT': db_default_port,
        },
    'fps': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': db_fps_dbname,
        'USER': db_fps_user,
        'PASSWORD': db_fps_password,
        'HOST': db_fps_host,
        'PORT': db_fps_port
    },
}
