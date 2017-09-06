# -*- coding: utf-8 -*

import datetime, urllib, urllib2, json
from utils.tool import generate_random
from django.conf import settings


def create_onevone_live_room(teacher_name):

    """
    HTTP创建1v1直播课堂
    :param teacher_name:
    :return:
    """
    url = settings.LIVE_ROOM_CREATE_API
    values = {
        'loginName': settings.LIVE_ROOM_USERNAME,
        'password': settings.LIVE_ROOM_PASSWORD,
        'sec': 'true',
        'subject': '%s(%s)' % ('1v1直播', datetime.datetime.now()),
        'startDate': datetime.datetime.now(),
        'scene': 0,
        'speakerInfo': teacher_name,
        'scheduleInfo': '',
        'studentToken': generate_random(6, 0),
        'description': '这里是1v1直播课堂，欢迎加入课堂',
        'realtime': True,
    }

    data = urllib.urlencode(values)  # 解析成key=value?key=value
    req = urllib2.Request(url, data)  # 发送的地址和数据
    response = urllib2.urlopen(req)  # 发送请求
    result = json.loads(response.read())  # 取出数据

    result_data = dict()
    if result['code'] == '0':
        result_data['live_id'] = result['id']
        result_data['live_code'] = result['number']
        result_data['assistant_token'] = result['assistantToken']
        result_data['student_token'] = result['studentToken']
        result_data['teacher_token'] = result['teacherToken']
        result_data['student_client_token'] = result['studentClientToken']
        result_data['student_join_url'] = result['studentJoinUrl']
        result_data['teacher_join_url'] = result['teacherJoinUrl']
        return True, result_data
    else:
        return False, result_data
