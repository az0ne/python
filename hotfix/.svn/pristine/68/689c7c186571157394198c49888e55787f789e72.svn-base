# -*- coding: utf-8 -*-
"""
@version: 2016/5/24
@author: zhangyunrui
@contact: david.zhang@maiziedu.com
@file: log_dict.py.py
@time: 2016/5/24 15:49
@note:  ??
"""
import platform

VERSION = 1
# 生产环境请确保DEBUG=False, 此时只需要发syslog
DEBUG = True
PLATFORM = platform.platform()

# 根据情况生成handler组合
mz_sys_log_hds = ['mz_sys_log_hd']
mz_biz_log_hds = ['mz_biz_log_hd']
mz_acs_log_hds = ['mz_acs_log_hd']

if not DEBUG:
    pass
else:
    mz_sys_log_hds.append('console')
    mz_biz_log_hds.append('console')
    mz_acs_log_hds.append('console')
    # 在debug下如有其它需求,如:在windows下写log到文件,请打开下列注释,并配置路径
    # if PLATFORM.startswith('Windows'):
    #     mz_sys_log_hds.append('deb_mz_sys_log_file_hd')
    #     mz_biz_log_hds.append('deb_mz_biz_log_file_hd')
    #     mz_acs_log_hds.append('deb_mz_acs_log_file_hd')
    # else:
    #     pass

LOGGING = {
    'version': VERSION,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(name)s]' + '[v-%s]' % VERSION + '[%(levelname)s]%(asctime)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        # 如果是在windows下debug,请打开下列注释,并配置路径
        # 'deb_mz_sys_log_file_hd': {
        #     'level': 'ERROR',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     # 文件路径请根据需要自定义
        #     'filename': 'log/sys.log',
        #     'maxBytes': 1024 * 1024 * 5,
        #     'backupCount': 5,
        #     'formatter': 'standard',
        # },
        # 'deb_mz_biz_log_file_hd': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     # 文件路径请根据需要自定义
        #     'filename': 'log/biz.log',
        #     'maxBytes': 1024 * 1024 * 5,
        #     'backupCount': 5,
        #     'formatter': 'standard',
        # },
        # 'deb_mz_acs_log_file_hd': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     # 文件路径请根据需要自定义
        #     'filename': 'log/acs.log',
        #     'maxBytes': 1024 * 1024 * 5,
        #     'backupCount': 5,
        #     'formatter': 'standard',
        # },
        'mz_sys_log_hd': {
            'level': 'ERROR',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'standard',
            'facility': 'local4',
        },
        'mz_biz_log_hd': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'standard',
            'facility': 'local5',
        },
        'mz_acs_log_hd': {
            'level': 'INFO',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'standard',
            'facility': 'local6',
        },
    },
    'loggers': {
        'mz_sys_log': {
            'handlers': mz_sys_log_hds,
            'level': 'ERROR',
            'propagate': True,
        },
        'mz_biz_log': {
            'handlers': mz_biz_log_hds,
            'level': 'DEBUG',
            'propagate': True,
        },
        'mz_acs_log': {
            'handlers': mz_acs_log_hds,
            'level': 'INFO',
            'propagate': True,
        },
        '': {
            'handlers': mz_sys_log_hds,
            'level': 'INFO',
            'propagate': True,
        },
    }
}
