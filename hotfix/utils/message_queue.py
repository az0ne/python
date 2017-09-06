# -*- coding: utf-8 -*-
import json
import requests
from django.conf import settings


class MQService(object):
    RECEIVE = 'receive/'
    DELETE = 'delete/'
    PUBLISH = 'publish/'

    def __init__(self, addr, queue_name):
        self.addr = addr
        self.queue_name = queue_name

    def publish(self, data):
        assert isinstance(data, dict), 'data must be dict.'
        param = {'queue_name': self.queue_name, 'body': data}
        response = requests.post(self.addr+self.PUBLISH, json=param)

        try:
            data = json.loads(response.content)
        except Exception:
            return {"error": True,
                    "msg": 'mq server error.'}

        return data

mq_service = MQService(settings.MQ_ADDR, settings.QUEUE_NAME)
