# -*- coding: utf-8 -*-
import requests
import json
import unicodedata
from django.conf import settings
from db.cores.cache import cache
from utils.logger import logger as log
from db.api.mz_wechat.material import del_news, store_wechat_news, get_wechat_news
from db.api.mz_wechat.menu import list_wechat_menu


def get_wechat_access_token(is_invalid_token=False):
    token = None
    if not is_invalid_token:
        token = cache.get('wechat_token')
    if not token:
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
            settings.WECHAT_APPID, settings.WECHAT_SECRET)
        r = requests.get(url)
        token = json.loads(r.content)['access_token']
        cache.set('wechat_token', token, 6000)
    return token


def get_wechat_material_count(token):
    url = 'https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=%s' % token
    r = requests.get(url)
    data = json.loads(r.content)
    return data


def get_wechat_material(material_type, offset, token):
    page_dict = {
        "type": material_type,
        "offset": offset,
        "count": 20
    }
    url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s' % token
    r = requests.post(url, data=json.dumps(page_dict))
    data = json.loads(r.content)
    return data


def save_wechat_news(is_invalid_token=False):
    result = del_news()
    if result.is_error():
        raise Exception('del_news')
    token = get_wechat_access_token(is_invalid_token)
    db_news_count = 0
    for page in range(5):
        db_list = []
        data = get_wechat_material('news', db_news_count, token)
        news_list = []
        db_news_count += 20
        if 'errcode' not in data:
            news_list = data['item']
        elif data['errcode'] in (40001, 40014, 42001):
            save_wechat_news(is_invalid_token=True)
        else:
            log.warn(
                'get_wechat_news_from_wechat with errcode %s' % data['errcode'])
            raise Exception(data['errcode'])
        for new in news_list:
            news_dict = dict(
                content=new['media_id'],
                news_info={
                    'list': []
                })
            for item in new['content']['news_item']:
                new_dict = dict(
                    title=item['title'],
                    digest=item['digest'],
                    cover_url=item['thumb_url'],
                    content_url=item['url']
                )
                news_dict['news_info']['list'].append(new_dict)
            db_list.append(json.dumps(news_dict))
        print page
        store_wechat_news(db_list)
    return True


def get_news(page, content):
    result = get_wechat_news(int(page), 10, content)
    data = result.result()
    for news in data['news_list']:
        item = news['content']
        new_dict = json.loads(item)
        news.update(
            data=item,
            titles={ni['title']: ni['content_url'] for ni in new_dict['news_info']['list']}
        )
    return data


def get_voice_or_video_from_wechat(material_type, is_invalid_token=False):
    token = get_wechat_access_token(is_invalid_token)
    data = get_wechat_material_count(token)
    count = 0
    if 'errcode' not in data:
        count = data[material_type+'_count']
    elif data['errcode'] in (40001, 40014, 42001):
        get_voice_or_video_from_wechat(material_type, is_invalid_token=True)
    else:
        log.warn(
            'get_wechat_voice_or_video_count_from_wechat with errcode %s' % data['errcode'])
        raise Exception(data['errcode'])
    pages = count / 20
    if count % 20 != 0:
        pages += 1
    result = []
    offset = 0
    for page in range(pages):
        data = get_wechat_material(material_type, offset, token)
        material_list = []
        offset += 20
        if 'errcode' not in data:
            material_list = data['item']
        elif data['errcode'] in (40001, 40014, 42001):
            get_voice_or_video_from_wechat(material_type, is_invalid_token=True)
        else:
            log.warn(
                'get_wechat_voice_or_video_from_wechat with errcode %s' % data['errcode'])
            raise Exception(data['errcode'])
        for material in material_list:
            result.append(dict(
                data=material['media_id'],
                title=material['name']
            ))
    return result


def has_chinese(text):
    if not isinstance(text, unicode):
        text = text.decode('utf-8')
    result = False
    for ch in text:
        if isinstance(ch, unicode):
            if unicodedata.east_asian_width(ch) != 'Na':
                result = True
                break
            else:
                continue
    return result


def upload_img(img, is_invalid_token=False):
    if has_chinese(img.name):
        return False, u'图片名不能含有中文'
    token = get_wechat_access_token(is_invalid_token)
    url = 'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=image' % token
    r = requests.post(url, files={"media": img})
    data = json.loads(r.content)
    if 'errcode' not in data:
        media_id = data['media_id']
        return True, media_id
    elif data['errcode'] in (40001, 40014, 42001):
        upload_img(img, is_invalid_token=True)
    else:
        return False, data['errmsg']


def update_wechat_menu(is_invalid_token=False):
    token = get_wechat_access_token(is_invalid_token)
    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s' % token
    data = {'button': []}
    result = list_wechat_menu()
    result = result.result()
    button = {}
    for menu in result:
        if menu['type'] == 3:
            if button:
                data['button'].append(button)
                button = {}
            button['name'] = menu['name'].encode('utf-8')
            button['sub_button'] = []
        elif menu['location_y'] == 0 and menu['type'] != 3:
            if button:
                data['button'].append(button)
                button = {}
            button['name'] = menu['name'].encode('utf-8')
            if menu['type'] == 1:
                button['type'] = 'view'
                button['url'] = menu['key'].encode('utf-8')
            else:
                button['type'] = 'click'
                button['key'] = menu['key'].encode('utf-8')
        else:
            sub_button = {}
            sub_button['name'] = menu['name'].encode('utf-8')
            if menu['type'] == 1:
                sub_button['type'] = 'view'
                sub_button['url'] = menu['key'].encode('utf-8')
            else:
                sub_button['type'] = 'click'
                sub_button['key'] = menu['key'].encode('utf-8')
            button['sub_button'].append(sub_button)
    if button:
        data['button'].append(button)

    r = requests.post(url, data=json.dumps(data, ensure_ascii=False, encoding="utf-8"))
    data = json.loads(r.content)
    if data['errcode'] == 0:
        return True, ''
    elif data['errcode'] in (40001, 40014, 42001):
        update_wechat_menu(is_invalid_token=True)
    else:
        return False, data['errmsg']


def get_material_by_id(m_id, is_invalid_token=False):
    """
    根据微信素材id获取素材详细
    :param m_id: 素材id
    :param is_invalid_token:
    :return:
    """

    url = 'https://api.weixin.qq.com/cgi-bin/material/get_material?access_token={0}'
    token = get_wechat_access_token(is_invalid_token)

    r = requests.post(url.format(token), data=json.dumps({'media_id': m_id}))
    try:
        data = json.loads(r.content)
    except:     # 图片，语音直接返回的文件数据
        return True, r.content

    if 'errcode' not in data:
        return True, data
    elif data['errcode'] in (40001, 40014, 42001):
        get_material_by_id(m_id, is_invalid_token=True)
    else:
        return False, data['errmsg']


def get_rules(is_invalid_token=False):
    """
    获取微信公众号规则
    :param is_invalid_token:
    :return:
    """

    url = 'https://api.weixin.qq.com/cgi-bin/get_current_autoreply_info?access_token={0}'
    token = get_wechat_access_token(is_invalid_token)

    r = requests.post(url.format(token))

    data = json.loads(r.content)

    if 'errcode' not in data:
        return True, data
    elif data['errcode'] in (40001, 40014, 42001):
        get_rules(is_invalid_token=True)
    else:
        return False, data['errmsg']
