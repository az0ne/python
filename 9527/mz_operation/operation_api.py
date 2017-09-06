# -*- coding: utf8 -*-
import json

import requests
from django.conf import settings

from utils import tool
from utils.logger import logger as log


class OperationAPI(object):
    # 渠道api
    channel_api = settings.OPERATION_API_HOST + '/api/data/channel/'
    # 汇总数据api
    channel_summarized_api = settings.OPERATION_API_HOST + '/api/data/channel/summarized/'
    # 汇总数据api
    global_summarized_api = settings.OPERATION_API_HOST + '/api/data/global/summarized/'
    # 转换比例api
    mixed_api = settings.OPERATION_API_HOST + '/api/data/global/mixed/'
    # 走势图api
    timeline_api = settings.OPERATION_API_HOST + '/api/data/channel/timeline/'
    # 计算用的走势图api
    calc_api = settings.OPERATION_API_HOST + '/api/data/global/timeline/'
    # 销售统计数据上传api
    up_volume_api = settings.OPERATION_API_HOST + '/collector/volume_info/'
    # 客户数据上传api
    up_customer_api = settings.OPERATION_API_HOST + '/collector/customer_info/'
    # sem数据上传api
    up_sem_api = settings.OPERATION_API_HOST + '/collector/sem_info/'

    @staticmethod
    def get(url, params=None):
        res = requests.get(url, params)
        return json.loads(res.content)

    @staticmethod
    def json_post(url, data):
        res = requests.post(url, data=json.dumps(data, cls=tool.JsonCommonEncoder))
        return json.loads(res.content)

    @staticmethod
    def failed(e, msg=None):
        return {"success": False, "msg": msg if msg else u"运营系统异常。",
                "debug_msg": u"运营系统异常。msg: {0}".format(e),
                "code": 500}

    def get_channels(self, params=None):
        try:
            res_data = self.get(self.channel_api, params)
        except Exception as e:
            log.warn('get global timeline failed. msg: {0}'.format(e))
            return []

        return res_data

    def channel_name(self, short):
        channels = self.get_channels()
        return {c[0]: c[1] for c in channels}[short]

    def get_variable_btns(self):
        params = {'from': '20160912', 'to': '20160913', 'channel': 'all'}
        try:
            res_data = self.get(self.calc_api, params)
        except Exception as e:
            log.warn('get global timeline failed. msg: {0}'.format(e))
            return {}

        if res_data.get('error', True):
            return {}

        return res_data['result']['mapping']

    def get_summarized(self, params=None, channel=False):
        if channel:
            api = self.channel_summarized_api
            try:
                legend = self.channel_name(params['channel'])
            except:
                legend = "销售漏斗原始数据"
        else:
            api = self.global_summarized_api
            legend = "销售漏斗原始数据"

        base_data = {
            "success": True,
            "title": {
                "text": "概要" + ("(分渠道)" if channel else ""),
                "subtext": "{0} <= 时间 < {1}".format(params['from'], params['to'])
            },
            "legend": [legend],
        }

        try:
            res_data = self.get(api, params)
        except Exception as e:
            log.warn('get total failed. msg: {0}'.format(e))
            return self.failed(e)

        if res_data.get('error', True):
            return self.failed(res_data["msg"])

        mapping = res_data['result']['mapping']
        data = res_data['result']['data']
        data = data.items()
        data.sort(key=lambda x: x[1])

        base_data['y_axis_data'] = [mapping[y[0]] for y in data]

        base_data['series_data'] = [
            {
                "name": legend,
                "type": "bar",
                "data": [y[1] for y in data]
            }
        ]

        return base_data

    def get_mixed(self, params=None):
        base_data = {
            "success": True,
            "title": {
                "text": "转换比例",
                "subtext": "{0} <= 时间 < {1}".format(params['from'], params['to'])
            },
            "legend": ["各种分析数据"]
        }
        try:
            res_data = self.get(self.mixed_api, params)
        except Exception as e:
            log.warn('get mixedin failed. msg: {0}'.format(e))
            return self.failed(e)

        if res_data.get('error', True):
            return self.failed(res_data["msg"])

        mapping = res_data['result']['mapping']
        data = res_data['result']['data']
        data = data.items()
        data.sort(key=lambda x: x[1])

        base_data['y_axis_data'] = [mapping[y[0]] for y in data]

        base_data['series_data'] = [
            {
                "name": "各种分析数据",
                "type": "bar",
                "data": [round(y[1]) for y in data]
            }
        ]

        return base_data

    def get_timeline(self, params=None):
        base_data = {
            "success": True,
            "title": {
                "text": "走势图",
                "subtext": "{0} <= 时间 < {1}".format(params['from'], params['to'])
            },
            "legend": ["各种分析数据"]
        }

        try:
            res_data = self.get(self.timeline_api, params)
        except Exception as e:
            log.warn('get channel timeline failed. msg: {0}'.format(e))
            return self.failed(e)

        if not res_data.get('result'):
            return self.failed(u'', u'无数据')

        if res_data.get('error', True):
            return self.failed(res_data["msg"])

        mapping = res_data['result']['mapping']
        data = res_data['result']['data']

        legend = mapping.items()
        legend.sort(key=lambda a: a[0])

        base_data['legend'] = [l[1] for l in legend]
        keys = [l[0] for l in legend]

        x_axis_data = data.keys()
        x_axis_data.sort()
        base_data['x_axis_data'] = x_axis_data

        base_data['series_data'] = []

        for key in keys:
            base_data['series_data'].append(
                {
                    "name": mapping[key],
                    "type": "line",
                    "data": [data[x][key] for x in x_axis_data]
                }
            )

        return base_data

    def get_calc(self, params=None):
        base_data = {
            "success": True,
            "title": {
                "text": "走势图",
                "subtext": "{0} <= 时间 < {1}".format(params['from'], params['to'])
            }
        }

        try:
            res_data = self.get(self.calc_api, params)
        except Exception as e:
            log.warn('get global timeline failed. msg: {0}'.format(e))
            return self.failed(e)

        if res_data.get('error', True):
            return self.failed(res_data["msg"])

        mapping = res_data['result']['mapping']
        data = res_data['result']['data']

        x_axis_data = data.keys()
        x_axis_data.sort()
        base_data['x_axis_data'] = x_axis_data

        series_data = {var: [] for var in mapping.keys()}

        for x_axis in x_axis_data:
            dt = data[x_axis]
            for k, v in dt.items():
                series_data[k].append(v if v else 0)

        base_data['series_data'] = [series_data]

        return base_data

    def upload_volume_info(self, data):
        try:
            res_data = self.json_post(self.up_volume_api, data)
        except Exception as e:
            log.warn('upload volume info failed. msg: {0}'.format(e))
            return self.failed(e)

        if res_data.get('error', True):
            return self.failed(res_data["msg"])
        return {'success': True}

    def upload_customer_info(self, data):
        try:
            res_data = self.json_post(self.up_customer_api, data)
        except Exception as e:
            log.warn('upload volume info failed. msg: {0}'.format(e))
            return self.failed(e)

        if res_data.get('error', True):
            return self.failed(res_data["msg"])
        return {'success': True}

    def upload_sem_info(self, data):
        try:
            res_data = self.json_post(self.up_sem_api, data)
        except Exception as e:
            log.warn('upload volume info failed. msg: {0}'.format(e))
            return self.failed(e)

        if res_data.get('error', True):
            return self.failed(res_data["msg"])
        return {'success': True}


operation_api = OperationAPI()
