# -*- coding: utf-8 -*-
import urllib2
import urllib
import requests
import json
import string
import random
import time
import hashlib

from django.conf import settings

from utils.logger import logger as log
from db.api.apiutils import use_cache
from db.cores.cache import cache

class OAuth2(object):
    @staticmethod
    def get_url_result(url):
        req = urllib2.Request(url)
        resp = urllib2.urlopen(req)
        content = resp.read()
        try:
            import simplejson
            return simplejson.loads(content)
        except simplejson.JSONDecodeError:
            return content

    @staticmethod
    def get_nickname(userinfo_url, parmar={}):
        openid_url = '%s?%s' % (
            userinfo_url, urllib.urlencode(
                {
                    key: value
                    for key, value in parmar.items()
                }
            )
        )
        content = OAuth2.get_url_result(openid_url)
        try:
            name = content['nickname']
            return True, name
        except:
            return False, ''


class WeiXinAuth2(OAuth2):
    '''weixin oauth2'''

    weixin_page_url_get_code = settings.WEIXIN_PAGE_URL_GET_CODE
    weixin_page_url_get_token = settings.WEIXIN_PAGE_URL_GET_TOKEN
    weixin_page_url_get_userinfo = settings.WEIXIN_PAGE_URL_GET_USERINFO
    appid = settings.APPID
    secret = settings.SECRET
    weixin_get_token_url = settings.WEIXIN_ACCESS_TOKEN_URL
    weixin_get_ticket_url = settings.WEIXIN_JSAPI_TICKET

    @staticmethod
    def get_weixin_code(code_url, appid, callback,
                        scope='snsapi_login', response_type='code'):
        code_url = '%s?%s#wechat_redirect' % (
            code_url, urllib.urlencode(
                {
                    'appid': appid,
                    'redirect_uri': callback,
                    'response_type': response_type,
                    'scope': scope,
                }
            )
        )
        return code_url

    @staticmethod
    def get_weixin_page_code(callback, code_url=weixin_page_url_get_code, appid=appid,
                             scope='snsapi_userinfo', response_type='code'):
        """
        @brief 微信内网页获取用户授权code

        :param code_url:
        :param appid:
        :param callback:
        :param scope:
        :param response_type:
        :return:

        @note 注意区分与get_weixin_code. 前者用于首页,用户微信扫描登陆PC官网
        """
        code_url = '%s?%s#wechat_redirect' % (code_url, urllib.urlencode([('appid', appid),
                                                                          ('redirect_uri', callback),
                                                                          ('response_type', response_type),
                                                                          ('scope', scope)]))
        return code_url

    @staticmethod
    def get_weixin_page_token(code, token_url=weixin_page_url_get_token, appid=appid, secret=secret):
        """
        @brief 以用户授权码为依据, 取得用户的授权token 和 openid
        :param code:
        :param token_url:
        :param appid:
        :param secret:
        :return:
        """
        token_url = '%s?%s' % (token_url, urllib.urlencode([('appid', appid),
                                                            ('secret', secret),
                                                            ('code', code),
                                                            ('grant_type', 'authorization_code')]))
        try:
            result = requests.get(token_url)
        except requests.exceptions.Timeout as e:
            return False, None, None
        data = json.loads(result.content)
        if result.status_code == 200 and not data.get('errcode'):
            return True, data.get('access_token'), data.get('openid')
        return False, None, None

    @staticmethod
    def get_weixin_page_user_info(access_token, openid, user_info_url=weixin_page_url_get_userinfo, lang='zh_CN'):
        """
        @brief 获取用户的微信信息
        :param access_token:
        :param openid:
        :param userinfo_url:
        :param lang:
        :return:
        """
        user_info_url = '%s?%s' % (user_info_url, urllib.urlencode([('access_token', access_token),
                                                                  ('openid', openid),
                                                                  ('lang', lang)]))
        try:
            result = requests.get(user_info_url)
        except requests.exceptions.Timeout as e:
            return False, None, None
        data = json.loads(result.content)
        if result.status_code == 200 and not data.get('errcode'):
            return True, data.get('nickname'), data.get('headimgurl')
        return False, None, None

    @staticmethod
    def get_openid(openid_url, auth_token_url, appid, secret, code,
                   grant_type='authorization_code'):
        openid_url = '%s?%s' % (
            openid_url, urllib.urlencode(
                {
                    'appid': appid,
                    'secret': secret,
                    'code': code,
                    'grant_type': grant_type,
                }
            )
        )

        content = WeiXinAuth2.get_url_result(openid_url)
        openid = content['openid']
        token = content['access_token']

        auth_url = '%s?%s' % (
            auth_token_url, urllib.urlencode({
                'access_token': token,
                'openid': openid,
                }
            )
        )

        content = WeiXinAuth2.get_url_result(auth_url)
        if content['errmsg'] == 'ok':
            return True, openid, token
        else:
            return False, None, None

    @staticmethod
    def get_nicknameforweixin(userinfo_url, access_token, openid):
        return OAuth2.get_nickname(userinfo_url, {'access_token': access_token,
                                        'openid': openid})

    @staticmethod
    def get_weixin_token(url=weixin_get_token_url, appid=appid, secret=secret):
        """
        @brief 获取微信公众平台access_token,
        :param url:
        :param appid:
        :param secret:
        :param use_cache: 是否使用缓存，根据微信要求，强制使用缓存．开放该参数是为了强制刷新token的情况
        :return:
        @note 该值需要缓存
        """
        query_url = '%s?%s' % (url, urllib.urlencode([('grant_type', 'client_credential'),
                                                     ('appid', appid),
                                                     ('secret', secret)]))
        try:
            result = requests.get(query_url)
        except requests.exceptions.Timeout as e:
            log.error('get weixin token fail: %s' % str(e))
            return None
        data = json.loads(result.content)
        if result.status_code == 200 and not data.get('errcode'):
            return data.get('access_token')
        log.error('get weixin toke fail: %s' % data.get('errmsg'))
        return None

    @staticmethod
    def get_weixin_jsapi_ticket(access_token, url=weixin_get_ticket_url):
        """
        @brief
        :param access_token:
        :param url:
        :return:
        """
        query_url = '%s?%s' % (url, urllib.urlencode([('access_token', access_token),
                                                      ('type', 'jsapi')]))
        try:
            result = requests.get(query_url)
        except requests.exceptions.Timeout as e:
            log.error('get weixin jsapi_ticket fail: %s' % str(e))
            return None
        data = json.loads(result.content)
        if result.status_code == 200 and not data.get('errcode'):
            return data.get('ticket')
        log.error('get weixin jsapi_ticket fail: %s' % data.get('errmsg'))
        return None

    @staticmethod
    def generate_weixin_jaspi_signature(url):
        """
        @ brief 生成jsdk鉴权需要的signature
        :param url: 需要鉴权的url
        :return:　a dict with info required by wx.config
        """
        # access_token = use_cache('get_weixin_token', 5400)(WeiXinAuth2.get_weixin_token)()  # 强制缓存
        try:
            access_token = cache.get('get_weixin_token')  # 直接从缓存获取
        except Exception as e:
            return None
        if not access_token:  # 获取token失败，仅仅影响分享功能，主要业务将继续工作　
            return None
        # jsapi_ticket = use_cache('get_weixin_jsapi_ticket', 5400)(WeiXinAuth2.get_weixin_jsapi_ticket)(access_token)
        try:
            jsapi_ticket = cache.get('get_weixin_jsapi_ticket')
        except Exception as e:
            return None
        if not jsapi_ticket:
            return None

        once_str = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
        time_stampe = int(time.time())
        ret = dict(noncestr=once_str, jsapi_ticket=jsapi_ticket, timestamp=time_stampe, url=url)
        parameters = '&'.join(['%s=%s' % (key.lower(), ret[key]) for key in sorted(ret)])
        ret['app_id'], ret['signature'] = WeiXinAuth2.appid, hashlib.sha1(parameters).hexdigest()
        return ret

class QQAuth2(OAuth2):
    '''QQ oauth2'''

    @staticmethod
    def get_qq_token(auth_url, appid, callback, code='code'):
        auth_url = '%s?%s' % (
            auth_url, urllib.urlencode({
                'response_type': code,
                'client_id': appid,
                'redirect_uri': callback,
                # 'state': settings.SECRET_KEY,
            }
            )
        )
        return auth_url

    @staticmethod
    def get_openid(token_url, openid_url, appid, secret, code, callback):
        try:
            token_url = '%s?%s' % (
                token_url, urllib.urlencode({
                    'grant_type': 'authorization_code',
                    'client_id': appid,
                    'client_secret': secret,
                    'code': code,
                    'redirect_uri': callback,
                }))
            content = QQAuth2.get_url_result(token_url)
            token = urllib2.urlparse.parse_qs(content).get('access_token', [''])[0]

            openid_url = '%s?%s' % (
                openid_url, urllib.urlencode({
                    'access_token': token,
                })
            )
            content = QQAuth2.get_url_result(openid_url)
            import simplejson
            openid = simplejson.loads(content.split('callback(')[1].split(')')[0])['openid']

            return True, openid, token
        except Exception as e:
            return False, None, None

    @staticmethod
    def get_nicknameforqq(userinfo_url, access_token, openid, appid):
        return OAuth2.get_nickname(userinfo_url, {'access_token': access_token,
                                                       'oauth_consumer_key': appid,
                                                       'openid': openid})

