# -*- coding: utf-8 -*-

"""
@version: 2016/3/28
@author: Jackie
@contact: jackie@maiziedu.com
@file: local.py
@time: 2016/3/28 13:36
@note:  ??
"""

import os
import uuid
import time
import datetime
from django.conf import settings

MEDIA_ROOT = os.path.abspath(settings.MEDIA_ROOT)


def _make_subpath():
    """根据时间戳创建目录"""
    path = str(int(time.time() * 1000))
    path = "/".join((path[:3], path[3:6], path[6:]))
    return path


def upload(file_data, bucket="", use_original_filename=False):
    if use_original_filename:  # 用原始文件名
        furl = os.path.join(bucket, _make_subpath(), file_data.name)
    else:
        (root, ext) = os.path.splitext(file_data.name)
        root = uuid.uuid4().get_hex()
        #bucket+year+month+day+filename
        furl = os.path.join(
            bucket, datetime.datetime.now().date().isoformat().replace('-', '/'),
            root + ext).replace('\\', '/')

    fpath = os.path.join(MEDIA_ROOT, furl)
    fdir = os.path.dirname(fpath)
    if not os.path.exists(fdir):
        os.makedirs(os.path.dirname(fpath))
    _write2local(file_data, fpath)
    return furl


def _write2local(file_data, fpath):
    with open(fpath, 'wb') as f:
        while True:
            buff = file_data.read(1024 * 1024)
            if buff:
                f.write(buff)
            else:
                break
