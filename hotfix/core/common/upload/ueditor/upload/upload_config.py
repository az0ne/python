# -*- coding: UTF-8 -*-
from datetime import datetime

__author__ = 'lee'


class UploadConfig(object):
    now = datetime.now()
    now_path = '{y}/{m}/{d}/'.format(y=now.year, m=now.month, d=now.day)

    UPLOAD_CONFIG_PATH = 'core/common/upload/ueditor/config/upload.json'
    UPLOAD_IMG_PATH = 'uploads/ueditor/img/' + now_path
    UPLOAD_FILE_PATH = 'uploads/ueditor/file/' + now_path
    UPLOAD_VIDEO_PATH = 'uploads/ueditor/video/' + now_path
