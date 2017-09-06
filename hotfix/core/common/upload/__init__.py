# -*- coding: utf-8 -*-

__author__ = 'Jackie'

from django.conf import settings

_method = getattr(settings, 'UPLOAD_BACKEND', 'LOCAL')

if _method == 'ALI_OSS':
    from local import upload
else:
    from ali_oss import upload
