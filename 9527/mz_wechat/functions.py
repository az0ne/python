# -*- coding: utf8 -*-
import json

from django.http.response import Http404

import db.api.mz_wechat.message
from mz_wechat import constants
from mz_wechat.interface import upload_img, get_material_by_id
from utils.logger import logger as log
from mz_wechat.constants import ReplyType


def get_reply_data(request, data_source, reply_type):
    if reply_type == ReplyType.TEXT:
        return data_source.get('content', '')

    elif reply_type == ReplyType.IMAGE:
        result = upload_img(request.FILES.get('image', None))
        if not result[0]:
            raise Exception(result[1])
        return result[1]

    elif reply_type == ReplyType.VIDEO:
        return data_source.get('video', '')

    elif reply_type == ReplyType.VOICE:
        return data_source.get('voice', '')

    elif reply_type == ReplyType.NEWS:
        return data_source.get('news', '')

    else:
        raise ValueError('无此回复类型')


def get_rules(m_id):
    rules = db.api.mz_wechat.message.get_rules(m_id)
    if rules.is_error():
        log.warn('get rules failed. message id: {0}'.format(m_id))
        raise Http404()
    else:
        rules = rules.result()

    rules['message_type_name'] = constants.MessageType.map[rules['message_type']]
    rules['match_type_name'] = constants.MatchType.map[rules['match_type']]
    rules['reply_type_name'] = constants.ReplyType.map[rules['reply_type']]

    if rules['reply_type'] == ReplyType.NEWS:
        content = json.loads(rules['content'])
        rules['titles'] = {ni['title']: ni['content_url'] for ni in content['news_info']['list']}

    # elif rules['reply_type'] != ReplyType.TEXT:
    #     material = get_material_by_id(rules['content'])
    #     if material[0]:
    #         rules['material'] = material[1]

    return rules
