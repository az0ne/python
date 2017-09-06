# -*- coding: utf-8 -*-

"""
@version: 2016/3/29
@author: Jackie
@contact: jackie@maiziedu.com
@file: interface.py
@time: 2016/3/29 15:23
@note:  ??
"""
from HTMLParser import HTMLParser
import re
from django.conf import settings
import db.api.common.app


# emoji code 转换
def emoji_to_img(content):
    emoji_re = re.compile(r'\\U[0-9A-Fa-f]{8}')
    emoji_codes = emoji_re.findall(content)
    for emoji_code in emoji_codes:
        if emoji_dict.has_key(emoji_code):
            text = ''.join(('<img ', 'src="', settings.FPS_HOST,
                            'static/ueditor/dialogs/emoji/images/emoji_00',
                            emoji_dict[emoji_code], '.gif" _src="', settings.FPS_HOST,
                            'static/ueditor/dialogs/emoji/images/emoji_00',
                            emoji_dict[emoji_code], '.gif">'))
            content = content.replace(emoji_code, text)
    return content


emoji_dict = {'\U0001F60A': '01', '\U0001F603': '02', '\U0001F61E': '03', '\U0001F620': '04', '\U0001F61C': '05',
              '\U0001F60D': '06', '\U0001F613': '07', '\U0001F625': '08', '\U0001F60F': '09', '\U0001F614': '10',
              '\U0001F601': '11', '\U0001F609': '12', '\U0001F623': '13', '\U0001F616': '14', '\U0001F62A': '15',
              '\U0001F61D': '16', '\U0001F60C': '17', '\U0001F628': '18', '\U0001F637': '19', '\U0001F633': '20',
              '\U0001F612': '21', '\U0001F630': '22', '\U0001F632': '23', '\U0001F62D': '24', '\U0001F602': '25',
              '\U0001F622': '26', '\U0000263A': '27', '\U0001F604': '28', '\U0001F621': '29', '\U0001F61A': '30',
              '\U0001F618': '31', '\U0001F631': '32', '\U0001F47F': '33', '\U0001F431': '34', '\U0001F42F': '35',
              '\U0001F43B': '36', '\U0001F436': '37', '\U0001F435': '38', '\U0001F437': '39', '\U0001F47D': '40',
              '\U0001F4A9': '41', '\U0001F44D': '42', '\U0001F44E': '43', '\U0001F44C': '44', '\U0001F44F': '45',
              '\U0001F446': '46', '\U0001F447': '47', '\U0001F448': '48', '\U0001F449': '49', '\U00002764': '50',
              '\U0001F494': '51', '\U0001F389': '52', '\U00002197': '53', '\U00002196': '54', '\U00002198': '55',
              '\U00002199': '56'
              }

app_emoji_dict = {"\U0001F60A": "\ue056", "\U0001F603": "\ue057", "\U0001F61E": "\ue058", "\U0001F620": "\ue059",
                  "\U0001F61C": "\ue105", "\U0001F60D": "\ue106", "\U0001F613": "\ue108", "\U0001F625": "\ue401",
                  "\U0001F60F": "\ue402", "\U0001F614": "\ue403", "\U0001F601": "\ue404", "\U0001F609": "\ue405",
                  "\U0001F623": "\ue406", "\U0001F616": "\ue407", "\U0001F62A": "\ue408", "\U0001F61D": "\ue409",
                  "\U0001F60C": "\ue40a", "\U0001F628": "\ue40b", "\U0001F637": "\ue40c", "\U0001F633": "\ue40d",
                  "\U0001F612": "\ue40e", "\U0001F630": "\ue40f", "\U0001F632": "\ue410", "\U0001F62D": "\ue411",
                  "\U0001F602": "\ue412", "\U0001F622": "\ue413", "\U0000263A": "\ue414", "\U0001F604": "\ue415",
                  "\U0001F621": "\ue416", "\U0001F61A": "\ue417", "\U0001F618": "\ue418", "\U0001F631": "\ue107",
                  "\U0001F47F": "\ue11a", "\U0001F431": "\ue04f", "\U0001F42F": "\ue050", "\U0001F43B": "\ue051",
                  "\U0001F436": "\ue052", "\U0001F435": "\ue109", "\U0001F437": "\ue10b", "\U0001F47D": "\ue10c",
                  "\U0001F4A9": "\ue05a", "\U0001F44D": "\ue00e", "\U0001F44E": "\ue421", "\U0001F44C": "\ue420",
                  "\U0001F44F": "\ue41f", "\U0001F446": "\ue22e", "\U0001F447": "\ue22f", "\U0001F448": "\ue230",
                  "\U0001F449": "\ue231", "\U00002764": "\ue022", "\U0001F494": "\ue023", "\U0001F389": "\ue312",
                  "\U00002197": "\ue236", "\U00002196": "\ue237", "\U00002198": "\ue238", "\U00002199": "\ue239"}


def emoji_to_app(content):
    emoji_re = re.compile(r'\\U[0-9A-Fa-f]{8}')
    emoji_codes = emoji_re.findall(content)
    for emoji_code in emoji_codes:
        if emoji_dict.has_key(emoji_code):
            content = content.replace(emoji_code, app_emoji_dict[emoji_code])
    return content


# 去除html标签
class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


# 把表情变成字符串
def filter_emoji(desstr,restr=''):
    '''
    过滤表情
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)


# IOS审核版本校验
def is_ios_check(request):
    client = request.POST.get('client')
    version = request.POST.get('vno')
    if client == 'ios':
        result = db.api.common.app.ios_version(_enable_cache=True)
        if result.is_error():
            return False
        version_list = result.result()
        if version_list:
            if version_list[0]['is_check'] and int(version) == int(version_list[0]['vno']):
                return True
    return False