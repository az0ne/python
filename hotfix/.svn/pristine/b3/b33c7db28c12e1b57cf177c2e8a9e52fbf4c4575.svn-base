# -*- coding: utf-8 -*-
import json

import requests
from django.conf import settings

from utils.logger import logger as log


class SensitiveWord(object):
    FAIL = 0
    PASS = 1
    SERVER_ERROR = 2

    def __init__(self, url):
        self.url = url

    def filter(self, content):
        try:
            res = requests.post(self.url, json={'content': content})
            result = json.loads(res.content)
            if result.get('error', True):
                log.warn(result.get('msg'))
            else:
                return self.FAIL if result.get('word') else self.PASS

        except Exception as e:
            log.warn('SensitiveWord server error. detail: {}'.format(e))

        return self.SERVER_ERROR


sensitive_word = SensitiveWord(settings.SENSITIVE_WORD_FILTER_URL)
